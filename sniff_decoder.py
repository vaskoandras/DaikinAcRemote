import re

nibbles = list()

with open('daikin_codes.txt', 'r') as f:
    file_content = f.read()
    lines = file_content.splitlines()

    p = re.compile(r'(?P<type>(space)|(pulse)) (?P<num>[0-9]+)')

    for line in lines:
        m = p.match(line)
        if m:
            num = int(m.group('num'))
            if m.group('type') == 'pulse':
                if num > 360 and num < 602:
                    #print('pulse L')
                    nibbles.append('p')
                elif num > 3400 and num < 3560:
                    #print('pulse H')
                    nibbles.append('P')
                else:
                    print("pulse ERROR - %s" % m.group('num'))
            if m.group('type') == 'space':
                if num > 265 and num < 510:
                    #print('space L')
                    nibbles.append('s')
                elif num > 1139 and num < 1360:
                    #print('space H')
                    nibbles.append('S')
                elif num > 1650 and num < 1850:
                    #print('space HH')
                    nibbles.append('1')
                elif num > 24500 and num < 25500:
                    #print('space HHH')
                    nibbles.append('2')
                elif num > 34500 and num < 35500:
                    #print('space HHHH')
                    nibbles.append('3')
                elif num > 200000:
                    #print('---\n')
                    nibbles.append('4')
                else:
                    print("space ERROR - %s" % m.group('num'))

index = 0
output = ''

while len(nibbles):
    index = index + 1
    nibble = nibbles.pop(0)

    if nibble == 'p':
        if len(nibbles) == 0:
            break
        nibble_2 = nibbles.pop(0)
        if nibble_2 == 's':
            output = output + '0'

        elif nibble_2 == 'S':
            output = output + '1'

        elif nibble_2 == '2':
            nibble_3 = nibbles.pop(0)
            if nibble_3 != 'P':
                raise Exception('break syntax: no P after 2')
            nibble_3 = nibbles.pop(0)
            if nibble_3 != '1':
                raise Exception('break syntax: no HH after 2P')
            output = output + '\n'

        elif nibble_2 == '3':
            nibble_3 = nibbles.pop(0)
            if nibble_3 != 'P':
                raise Exception('break syntax: no P after 2')
            nibble_3 = nibbles.pop(0)
            if nibble_3 != '1':
                raise Exception('break syntax: no HH after 2P')
            output = output + '\n'

        if nibble_2 == '4':
            output = output + '\n\n'



output2 = ''
for line in output.splitlines():
    newline = ''
    num = 0
    for i,c in enumerate(line):
        if c == '1':
            #num = num + 2**(7 - (i % 8))
            num = num + 2**(i % 8)
        if i % 8 == 7:
            newline = newline + "%02X" % num
            #print("%02X" % num)
            num = 0
    output2 = output2 + newline + '\n'

print(output)

for line in output.splitlines():
    newline = ''
    for i, c in enumerate(line):
        if i % 8 == 7:
            newline = newline + line[i:] + ' '
    #print(newline)

for line in output.splitlines():
    newline = ''
    for i, c in enumerate(line):
        newline = newline + c + ';'
    print(newline)

print(output2)
