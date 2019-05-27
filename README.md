# DaikinAcRemote

- p - short pulse
- g - short gap
- G - long gap
- L - leading pulse
- l - leading gap

Bit description:
[short pulse][short gap] - 0
[short pulse][long gap] - 1

byte = [bit]*8

Command format:
[leading pulse][loading gap][byte]*n[checksum]



Bit order: LSB first


