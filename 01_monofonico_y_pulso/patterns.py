from mido import MidiFile


MidiFile.ticks_per_beat = 480

r = MidiFile.ticks_per_beat * 4
b = MidiFile.ticks_per_beat * 2
n = MidiFile.ticks_per_beat
c = MidiFile.ticks_per_beat // 2
s = MidiFile.ticks_per_beat // 4
f = MidiFile.ticks_per_beat // 8


REST = 0
G2 = 43
C3 = 48
E3 = 52
F3 = 53
Fs3 = 54
G3 = 55
A3 = 57
Bb3 = 58
B3 = 59
C4 = 60
D4 = 62
E4 = 64
F4 = 65
Fs4 = 66
G4 = 67
A4 = 69
B4 = 71

patterns = [
    # 0
    [
        (s, C4),
        (s, REST)
    ],
    [
        (f, C3),
        (n - f, E3),
        (f, C3),
        (n - f, E3),
        (f, C3),
        (n - f, E3),
    ],
    [
        (f, C3),
        (c - f, E3),
        (c, F3),
        (n, E3),
    ],
    [
        (c, REST),
        (c, E3),
        (c, F3),
        (c, E3),
    ],
    [
        (c, REST),
        (c, E3),
        (c, F3),
        (c, G3),
    ],
    [
        (c, E3),
        (c, F3),
        (c, G3),
        (c, REST),
    ],
    [
        (r * 2, C4),
    ],
    [
        (n * 3 + c, REST),
        (s, C3),
        (s, C3),
        (c, C3),
        (n * 4 + c, REST),
    ],
    [
        (r + b, G3),
        (r * 2, F3),
    ],
    [
        (s, B3),
        (s, G3),
        (n * 3 + c, REST),
    ],
    # 10
    [
        (s, B3),
        (s, G3),
    ],
    [
        (s, F3),
        (s, G3),
        (s, B3),
        (s, G3),
        (s, B3),
        (s, G3),
    ],
    [
        (c, F3),
        (c, G3),
        (r, B3),
        (n, C4),
    ],
    [
        (s, B3),
        (s + c, G3),
        (s, G3),
        (s, F3),
        (c, G3),
        (s + c, REST),
        (s + n * 3, G3),
    ],
    [
        (r, C4),
        (r, B3),
        (r, G3),
        (r, Fs3),
    ],
    [
        (s, G3),
        (r - s, REST),
    ],
    [
        (s, G3),
        (s, B3),
        (s, C4),
        (s, B3),
    ],
    [
        (s, B3),
        (s, C4),
        (s, B3),
        (s, C4),
        (s, B3),
        (s, REST),
    ],
    [
        (s, E3),
        (s, Fs3),
        (s, E3),
        (s, Fs3),
        (s * 3, E3),
        (s, E3),
    ],
    [
        (c * 3, REST),
        (c * 3, G4),
    ],
    # 20
    [
        (s, E3),
        (s, Fs3),
        (s, E3),
        (s, Fs3),
        (s * 3, G2),
        (s, E3),
        (s, Fs3),
        (s, E3),
        (s, Fs3),
        (s, E3),
    ],
    [
        (n * 3, Fs3),
    ],
    [
        (c * 3, E3),
        (c * 3, E3),
        (c * 3, E3),
        (c * 3, E3),
        (c * 3, E3),
        (c * 3, Fs3),
        (c * 3, G3),
        (c * 3, A3),
        (c, B3),
    ],
    [
        (c, E3),
        (c * 3, Fs3),
        (c * 3, Fs3),
        (c * 3, Fs3),
        (c * 3, Fs3),
        (c * 3, Fs3),
        (c * 3, G3),
        (c * 3, A3),
        (n, B3),
    ],
    [
        (c, E3),
        (c, Fs3),
        (c * 3, G3),
        (c * 3, G3),
        (c * 3, G3),
        (c * 3, G3),
        (c * 3, G3),
        (c * 3, A3),
        (c, B3),
    ],
    [
        (c, E3),
        (c, Fs3),
        (c, G3),
        (c * 3, A3),
        (c * 3, A3),
        (c * 3, A3),
        (c * 3, A3),
        (c * 3, A3),
        (c * 3, B3),
    ],
    [
        (c, E3),
        (c, Fs3),
        (c, G3),
        (c, A3),
        (c * 3, B3),
        (c * 3, B3),
        (c * 3, B3),
        (c * 3, B3),
        (c * 3, B3),
    ],
    [
        (s, E3),
        (s, Fs3),
        (s, E3),
        (s, Fs3),
        (c, G3),
        (s, E3),
        (s, G3),
        (s, Fs3),
        (s, E3),
        (s, Fs3),
        (s, E3),
    ],
    [
        (s, E3),
        (s, Fs3),
        (s, E3),
        (s, Fs3),
        (s + c, E3),
        (s, E3),
    ],
    [
        (n * 3, E3),
        (n * 3, G3),
        (n * 3, C4),
    ],
    # 30
    [
        (b * 3, C4),
    ],
    [
        (s, G3),
        (s, F3),
        (s, G3),
        (s, B3),
        (s, G3),
        (s, B3),
    ],
    [
        (s, F3),
        (s, G3),
        (s, F3),
        (s, G3),
        (s, B3),
        (s + b, F3),
        (c * 3, G3),
    ],
    [
        (s, G3),
        (s, F3),
        (c, REST),
    ],
    [
        (s, G3),
        (s, F3),
    ],
    [
        (s, F3),
        (s, G3),
        (s, B3),
        (s, G3),
        (s, B3),
        (s, G3),
        (s, B3),
        (s, G3),
        (s, B3),
        (s, G3),
        (c, REST),
        (n, REST),
        (n, REST),
        (n, REST),
        (n, Bb3),
        (n * 3, G4),
        (c, A4),
        (n, G4),
        (c, B4),
        (c * 3, A4),
        (c, G4),
        (n * 3, E4),
        (c, G4),
        (c + n * 3, Fs4),
        (n, REST),
        (n, REST),
        (c, REST),
        (c + b, E4),
        (b * 3, F4),
    ],
    [
        (s, F3),
        (s, G3),
        (s, B3),
        (s, G3),
        (s, B3),
        (s, G3),
    ],
    [
        (s, F3),
        (s, G3),
    ],
    [
        (s, F3),
        (s, G3),
        (s, B3),
    ],
    [
        (s, B3),
        (s, G3),
        (s, F3),
        (s, G3),
        (s, B3),
        (s, C4),
    ],
    # 40
    [
        (s, B3),
        (s, F3),
    ],
    [
        (s, B3),
        (s, G3),
    ],
    [
        (r, C4),
        (r, B3),
        (r, A3),
        (r, C4),
    ],
    [
        (s, F4),
        (s, E4),
        (s, F4),
        (s, E4),
        (c, E4),
        (c, E4),
        (c, E4),
        (s, F4),
        (s, E4),
    ],
    [
        (c, F4),
        (n, E4),
        (c, E4),
        (n, C4),
    ],
    [
        (n, D4),
        (n, D4),
        (n, G3),
    ],
    [
        (s, G3),
        (s, D4),
        (s, E4),
        (s, D4),
        (c, REST),
        (c, G3),
        (c, REST),
        (c, G3),
        (c, REST),
        (c, G3),
        (s, G3),
        (s, D4),
        (s, E4),
        (s, D4),
    ],
    [
        (s, D4),
        (s, E4),
        (c, D4),
    ],
    [
        (b * 3, G3),
        (r, G3),
        (r + n, F3),
    ],
    [
        (s, F3),
        (s, G3),
        (s, Bb3),
        (s, G3),
        (s, Bb3),
        (s, G3),
    ],
    # 50
    [
        (s, F3),
        (s, G3),
    ],
    [
        (s, F3),
        (s, G3),
        (s, Bb3),
    ],
    [
        (s, G3),
        (s, Bb3),
    ],
    [
        (s, Bb3),
        (s, G3),
    ],
]
