from enum import Enum

l1 = '11DA2700C50000D7'
l2 = '11DA270042000054'
l3 = '11DA2700000C2E00A00000C6030000C18000F6'

l1 = {0x11, 0xDA, 0x27, 0x00, 0xC5, 0x00, 0x00, 0xD7}
l2 = {0x11, 0xDA, 0x27, 0x00, 0x42, 0x00, 0x00, 0x54}
l3 = {0x11, 0xDA, 0x27, 0x00, 0x00, 0x0C, 0x2E, 0x00, 0xA0, 0x00, 0x00, 0xC6, 0x03, 0x00, 0x00, 0xC1, 0x80, 0x00, 0xF6}

preamble = [0x11, 0xDA, 0x27, 0x00]

cmd1 = {0xC5, 0x00, 0x00}
cmd2 = {0x42, 0x00, 0x00}
cmd3 = {0x00, 0x0C, 0x2E, 0x00, 0xA0, 0x00, 0x00, 0xC6, 0x03, 0x00, 0x00, 0xC1, 0x80, 0x00}

PULSE_SHORT = 482
PULSE_LONG = 3486
GAP_SHORT = 388
GAP_LONG = 1257
GAP_LEADING = 1698

def reverse_byte(num):
    result = 0
    for i in range(8):
        if num & (1 << i):
            result = result + (1 << (7 - i))
    return result


def get_chksum(cmd):
    cksum = 0
    for c in cmd:
        cksum = cksum + c

    return cksum % 256

class AcModes(Enum):
    Auto = 0
    Dry = 2
    Cool = 3
    Heat = 4
    Fan = 6

class FanModes(Enum):
    undefined = 0
    Level1 = 0x3
    Level2 = 0x4
    Level3 = 0x5
    Level4 = 0x6
    Level5 = 0x7
    Auto = 0xA
    Silent = 0xB

def get_ac_command(is_ac_on, mode, temperature, is_swing_on, fan_mode, is_economy, is_powerful, is_on_timer_on, is_off_timer_on):
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
    ret[7] = 0x06
    ret[8] = 0x60
    ret[9] = 0x01 * is_powerful
    ret[11] = 0xC1
    ret[12] = 0x80 + 0x4 * is_economy
    ret = preamble + ret
    cksum = get_chksum(ret)
    return ret + [cksum]

def create_lirc_conf(cmd):
    content = ''
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
    
    content = content + "begin remote\n\n"
    content = content + "  name DaikinXXX\n"
    content = content + "  flags RAW_CODES\n"
    content = content + "  begin raw_codes\n\n"
    
    content = content + "    name cmd\n"
    
    content = content + "    "
    for raw_value in raw_values:
        content = content + "%d " % raw_value
    content = content + "\n\n"
    content = content + "  end raw_codes\n\n"
    content = content + "end remote\n"
    
    return content

r = get_ac_command(0, AcModes.Auto, 22, 1, FanModes.Silent, 0, 0, 0, 0)
for c in r:
    print("%02X " % c, end = ' ')
print()

print(create_lirc_conf(r))