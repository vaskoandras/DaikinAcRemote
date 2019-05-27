l1 = '11DA2700C50000D7'
l2 = '11DA270042000054'
l3 = '11DA2700000C2E00A00000C6030000C18000F6'

l1 = {0x11, 0xDA, 0x27, 0x00, 0xC5, 0x00, 0x00, 0xD7}
l2 = {0x11, 0xDA, 0x27, 0x00, 0x42, 0x00, 0x00, 0x54}
l3 = {0x11, 0xDA, 0x27, 0x00, 0x00, 0x0C, 0x2E, 0x00, 0xA0, 0x00, 0x00, 0xC6, 0x03, 0x00, 0x00, 0xC1, 0x80, 0x00, 0xF6}

preamble = {0x11, 0xDA, 0x27, 0x00}

cmd1 = {0xC5, 0x00, 0x00}
cmd2 = {0x42, 0x00, 0x00}
cmd3 = {0x00, 0x0C, 0x2E, 0x00, 0xA0, 0x00, 0x00, 0xC6, 0x03, 0x00, 0x00, 0xC1, 0x80, 0x00}


def reverse_byte(num):
    result = 0
    for i in range(8):
        if num & (1 << i):
            result = result + (1 << (7 - i))
    return result


def get_chksum(cmd):
    cksum = 0
    for c in preamble:
        cksum = cksum + c
    for c in cmd:
        cksum = cksum + c

    return cksum % 256

from enum import Enum
class AcModes(Enum):
    Auto = 0
    Dry = 2
    Cool = 3
    Heat = 4
    Fan = 6

class FanModes(Enum):
    Level1 = 1,
    Level2 = 2,
    Level3 = 3,
    Level4 = 4,
    Level5 = 5,
    Auto = 6,
    Silent = 7

def get_ac_command(is_ac_on, mode, temperature, is_swing_in, fan_mode, is_economy, is_powerful, is_on_timer_on, is_off_timer_on):
    ret = [0] * 14

    ret[1] = ret[1] + 0x08
    if is_ac_on:
        ret[1] = ret[1] + 0x01
    print("%02x" % mode.value)
    print("%02x" % (mode.value << 4))
    ret[1] = ret[1] + ((mode.value << 4) & 0xf0)


    return ret

#print("%02X" % get_chksum(cmd1))
#print("%02X" % get_chksum(cmd2))
#print("%02X" % get_chksum(cmd3))


r = get_ac_command(1, AcModes.Dry, 22, 0, 0, 0, 0, 0, 0)
for c in r:
    print("%02X " % c, end = ' ')
print('\n')
for c in r:
    print("%02X " % reverse_byte(c), end = ' ')
