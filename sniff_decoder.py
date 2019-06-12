import re

pulses = list()

pulses_short_list = []
pulses_long_list = []
spaces_short = []
spaces_long = []
spaces_leading = []
filename = 'mycode.txt'
with open(filename, 'r') as f:
    file_content = f.read()
    lines = file_content.splitlines()

    p = re.compile(r'(?P<type>(space)|(pulse)) (?P<num>[0-9]+)')

    for line in lines:
        m = p.match(line)
        if m:
            num = int(m.group('num'))
            if m.group('type') == 'pulse':
                if num > 360 and num < 602:
                    pulses.append('p')
                    pulses_short_list.append(num)
                elif num > 3400 and num < 3560:
                    pulses.append('P')
                    pulses_long_list.append(num)
                else:
                    print("pulse ERROR - %s" % m.group('num'))
            if m.group('type') == 'space':
                if num > 265 and num < 510:
                    pulses.append('s')
                    spaces_short.append(num)
                elif num > 1139 and num < 1360:
                    pulses.append('S')
                    spaces_long.append(num)
                elif num > 1650 and num < 1850:
                    pulses.append('L')
                    spaces_leading.append(num)
                elif num > 24500:
                    pulses.append('G')
                else:
                    print("space ERROR - %s" % m.group('num'))

index = 0
output = ''

while len(pulses):
    index = index + 1
    pulse = pulses.pop(0)

    if pulse == 'p':
        if len(pulses) == 0:
            break
        pulse_2 = pulses.pop(0)
        if pulse_2 == 's':
            output = output + '0'

        elif pulse_2 == 'S':
            output = output + '1'

        if pulse_2 == 'G':
            output = output + '\n'
            
    elif pulse == 'P': # leading long pulse + gap
        if len(pulses) == 0:
            break
        pulse_2 = pulses.pop(0)
        if pulse_2 == 'L':
            pass
        else:
            raise Exception('Leading pulse-space error')



print('Response in binary')
print(output)

print('Response in binary with delimiters')
for line in output.splitlines():
    newline = ''
    for i, c in enumerate(line):
        newline = newline + c + ';'
    print(newline)


output2 = ''
for line in output.splitlines():
    newline = str()
    num = 0
    for i,c in enumerate(line):
        if c == '1':
            num = num + 2**(i % 8)
        if i % 8 == 7:
            newline = newline + "%02X" % num
            num = 0
    if (i % 8 != 7):
        newline = newline + "??"
    output2 = output2 + newline + '\n'


print('Response in hex')
print(output2)

print("Short pulse length: %d" % int(round(sum(pulses_short_list)/len(pulses_short_list))))
print("Long pulse length: %d" % int(round(sum(pulses_long_list)/len(pulses_long_list))))
print("Short gap length: %d" % int(round(sum(spaces_short)/len(spaces_short))))
print("Long gap length: %d" % int(round(sum(spaces_long)/len(spaces_long))))
print("Leading gap length: %d" % int(round(sum(spaces_leading)/len(spaces_leading))))

