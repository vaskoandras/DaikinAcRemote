from enum import Enum
import pigpio
import time
import argparse

PULSE_SHORT = 482
PULSE_LONG = 3486
GAP_SHORT = 388
GAP_LONG = 1257
GAP_LEADING = 1698


def get_chksum(cmd):
    cksum = 0
    for c in cmd:
        cksum = cksum + c

    return cksum % 256


class AcModes(Enum):
    auto = 0
    dry = 2
    cool = 3
    heat = 4
    fan = 6


class FanModes(Enum):
    undefined = 0
    l1 = 0x3
    l2 = 0x4
    l3 = 0x5
    l4 = 0x6
    l5 = 0x7
    auto = 0xA
    silent = 0xB


def get_ac_command(is_ac_on, mode, temperature, is_swing_on, fan_mode, is_economy, is_powerful, on_timer, off_timer):
    preamble = [0x11, 0xDA, 0x27, 0x00]
    ret = [0] * 14
    # byte 1 = 0
    ret[1] = ret[1] + 0x08
    
    # AC on
    ret[1] = ret[1] + (0x01 * is_ac_on)
    # Mode
    ret[1] = ret[1] + ((mode.value << 4) & 0xf0)
    # Temperature
    ret[2] = temperature * 2
    # byte 3 = 0
    # Swing 
    ret[4] = 0x0f * is_swing_on
    ret[4] = ret[4] + (fan_mode.value << 4)
    # byte 5 = 0 
    # byte 6 = 0 # TODO: tOn/tOff
    if on_timer:
        if on_timer > 12:
            on_timer = 12
        on_timer = on_timer * 15
        ret[6] = (on_timer & 0x3f) << 2
        ret[7] = (on_timer & 0xa0) >> 6
        ret[1] = ret[1] + 0x02
    else:
        ret[7] = 0x06

    if off_timer:
        if off_timer > 9:
            off_timer = 9
        off_timer = off_timer * 15
        ret[7] = ret[7] | (off_timer & 0x03) << 6
        ret[8] = (off_timer & 0xfc) >> 2
        ret[1] = ret[1] + 0x04
    else:
        ret[8] = 0x60
    ret[9] = 0x01 * is_powerful
    ret[11] = 0xC1
    ret[12] = 0x80 + 0x4 * is_economy
    ret = preamble + ret
    cksum = get_chksum(ret)
    return ret + [cksum]

def get_raw_values(cmd):
    raw_values = []
    raw_values.append(PULSE_LONG)
    raw_values.append(GAP_LEADING)

    for c in cmd:
        for i in range(8):
            if c & (1 << i):
                raw_values.append(PULSE_SHORT)
                raw_values.append(GAP_LONG)
            else:
                raw_values.append(PULSE_SHORT)
                raw_values.append(GAP_SHORT)
    raw_values.append(PULSE_SHORT)

    return raw_values


def carrier(gpio, frequency, micros):
    """
    Generate carrier square wave.
    """
    wf = []
    cycle = 1000.0 / frequency
    cycles = int(round(micros/cycle))
    on = int(round(cycle / 2.0))
    sofar = 0
    for c in range(cycles):
        target = int(round((c+1)*cycle))
        sofar += on
        off = target - sofar
        sofar += off
        wf.append(pigpio.pulse(1<<gpio, 0, on))
        wf.append(pigpio.pulse(0, 1<<gpio, off))
    return wf


pi = pigpio.pi()

def ir_transmit(code):
    GPIO = 18
    FREQ = 38.0
    GAP_S = 100/1000

    pi.set_mode(GPIO, pigpio.OUTPUT)  # IR TX connected to this GPIO.

    pi.wave_add_new()

    emit_time = time.time()


    # Create wave
    marks_wid = {}
    spaces_wid = {}

    wave = [0] * len(code)

    for i in range(0, len(code)):
        ci = code[i]
        if i & 1:  # Space
            if ci not in spaces_wid:
                pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                spaces_wid[ci] = pi.wave_create()
            wave[i] = spaces_wid[ci]
        else:  # Mark
            if ci not in marks_wid:
                wf = carrier(GPIO, FREQ, ci)
                pi.wave_add_generic(wf)
                marks_wid[ci] = pi.wave_create()
            wave[i] = marks_wid[ci]

    delay = emit_time - time.time()

    if delay > 0.0:
        time.sleep(delay)

    pi.wave_chain(wave)

    while pi.wave_tx_busy():
        time.sleep(0.002)

    emit_time = time.time() + GAP_S

    for i in marks_wid:
        pi.wave_delete(marks_wid[i])

    marks_wid = {}

    for i in spaces_wid:
        pi.wave_delete(spaces_wid[i])

    spaces_wid = {}


p = argparse.ArgumentParser()

p.add_argument("on", help="AC on [0,1]", type=int)
p.add_argument("mode", help="mode [auto, cool, dry, heat, fan]", type=str)
p.add_argument("temperature", help="temperature[18-30]", type=int)
p.add_argument("swing", help="swing [0,1]", type=int)
p.add_argument("fan", help="fan mode [l1-l5,auto,silent]", type=str)
p.add_argument("economy", help="economy mode [0,1]", type=int)
p.add_argument("power", help="power mode [0,1]", type=int)
p.add_argument("on_timer", help="on timer [0-12]", type=int)
p.add_argument("off_timer", help="off timer [0-9]", type=int)

args = p.parse_args()

on = args.on
mode = AcModes[args.mode.lower()]
temp = args.temperature
swing = args.swing
fan = FanModes[args.fan.lower()]
economy = args.economy
power = args.power
on_timer = args.on_timer
off_timer = args.off_timer


print("AC on: %d" % on)
print("Mode: %s" % mode)
print("Temperature: %d" % temp)
print("Swing: %d" % swing)
print("Fan: %s" % fan)
print("Economy mode: %d" % economy)
print("Power mode: %d" % power)
print("On timer: %d" % on_timer)
print("Off timer: %d" % off_timer)

cmd1 = (0x11, 0xDA, 0x27, 0x00, 0xC5, 0x00, 0x00, 0xD7)
cmd2 = (0x11, 0xDA, 0x27, 0x00, 0x42, 0x00, 0x00, 0x54)

cmd3 = get_ac_command(on, mode, temp, swing, fan, economy, power, on_timer, off_timer)

raw_values = get_raw_values(cmd1)
#ir_transmit(raw_values)

raw_values = get_raw_values(cmd2)
#ir_transmit(raw_values)

raw_values = get_raw_values(cmd3)
for c in cmd3:
    print("%02X" % c, end=' ')

print()
#ir_transmit(raw_values)




