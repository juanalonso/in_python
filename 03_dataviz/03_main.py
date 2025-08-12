# In Python
# V 3.0

# Desbaratamos para reorganizar y poder calcular mejor
# en el futuro lo lejos que está un instrumentista de otro.

from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from patterns import patterns, r, b, n, c
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
# import numpy as np


def create_midi_score(num_tracks, instruments, bpm=120):
    mid = MidiFile()
    pan_positions = set_pan_positions(num_tracks)

    for i in range(num_tracks):

        track = MidiTrack()

        # Solo necesitamos indicar el tempo una vez
        if i == 0:
            track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))

        instrument = instruments[i] if i < len(instruments) else 1
        track.append(Message("program_change", program=instrument, channel=i, time=0))

        # Aplicar posición de panorámico
        track.append(
            Message(
                "control_change", control=10, value=pan_positions[i], channel=i, time=0
            )
        )

        mid.tracks.append(track)

    return mid


def add_pattern_to_score(
    track, pattern_index, octave_shift=0, start_time=0, channel=0, velocity=100
):

    def add_note(note_num, velocity, time, on=True):
        msg_type = "note_on" if on else "note_off"
        track.append(
            Message(
                msg_type, note=note_num, velocity=velocity, channel=channel, time=time
            )
        )

    pattern = patterns[pattern_index]
    delta_time = start_time  # por si arrastramos silencios al final de un patrón

    for duration, note in pattern:
        if note == 0:  # Silencio
            delta_time += duration
        else:
            shifted_note = note + octave_shift
            human_vel = humanize_velocity(velocity)
            human_dur = humanize_duration(duration)
            human_start = humanize_timing(0)
            add_note(shifted_note, human_vel, delta_time + human_start, True)  # Note on
            add_note(
                shifted_note, 0, human_dur - human_start, False
            )  # Note off con velocity 0
            delta_time = duration - human_dur  # Cosas del MIDI

    return delta_time


def save_score_to_midi(midi_file, filename="output.mid"):

    midi_file.save(filename)


def get_track_duration(track):
    return track[-1][1] + track[-1][2]


def get_pattern_duration(pattern):
    return sum(duration for duration, _ in pattern)


def set_pan_positions(num_tracks, left=24, right=104):
    if num_tracks == 1:
        return [64]  # Centro
    else:
        return [
            left + int((i / (num_tracks - 1)) * (right - left))
            for i in range(num_tracks)
        ]


def humanize_velocity(base_vel, variation_percent=20, min_vel=20, max_vel=127):
    std_dev = base_vel * variation_percent / 100 / 3
    # /2, más en la media, /4, más disperso
    randomized_vel = int(random.normalvariate(base_vel, std_dev))
    return max(min_vel, min(max_vel, randomized_vel))


def humanize_duration(base_duration, variation_percent=10, min_duration_pct=70):
    std_dev = base_duration * variation_percent / 100 / 3
    randomized_duration = int(random.normalvariate(base_duration, std_dev))
    min_duration = int(base_duration * min_duration_pct / 100)
    return max(min_duration, min(base_duration, randomized_duration))


def humanize_timing(base_time, max_delay_percent=5):
    """
    Humaniza el timing del note_on añadiendo solo retrasos
    base_time: tiempo base (siempre será 0 para note_on en este contexto)
    max_delay_percent: porcentaje máximo de retraso respecto a la duración de una corchea
    """
    # Usamos una distribución exponencial para que los retrasos pequeños sean más comunes
    max_delay = int(240 * max_delay_percent / 100)  # 240 = corchea en ticks
    delay = int(
        random.expovariate(3) * max_delay
    )  # Lambda=3 para retrasos pequeños más frecuentes
    return min(delay, max_delay)  # Asegurar que no exceda el máximo


NUM_PLAYERS = 12
BPM = 120

midi_score = create_midi_score(
    NUM_PLAYERS, [0, 4, 6, 9, 12, 16, 18, 21, 24, 27, 29, 10], BPM
)
max_dur = 0


# PARTITURA
score = []
for track_index in range(NUM_PLAYERS - 1):
    score.append([])
    offset = r + random.randint(0, 9) * b
    # -1 para indicar que es un fragmento vacío
    # aunque luego no usamos este -1
    score[track_index].append((-1, 0, offset))

    for i in range(1, len(patterns)):
        for rep in range(random.randint(4, 10)):
            pattern_duration = get_pattern_duration(patterns[i])
            score[track_index].append((i, offset, pattern_duration))
            offset += pattern_duration

    max_dur = max(max_dur, get_track_duration(score[track_index]))


# SINCRONIZAMOS FINALES
last_pattern_index = len(patterns) - 1
last_pattern_duration = get_pattern_duration(patterns[last_pattern_index])
for track_index in range(NUM_PLAYERS - 1):
    offset = get_track_duration(score[track_index])
    while get_track_duration(score[track_index]) < max_dur:
        score[track_index].append((last_pattern_index, offset, last_pattern_duration))
        offset += last_pattern_duration

# PULSO
score.append([])
offset = 0
pattern_duration = get_pattern_duration(patterns[0])
while offset < max_dur:
    score[NUM_PLAYERS - 1].append((0, offset, pattern_duration))
    offset += pattern_duration


# PARTITURA A MIDI
for track_index in range(NUM_PLAYERS):
    midi_track = midi_score.tracks[track_index]
    # Este lío es porque el primer elemento de score[track_index]
    # es un silencio, salvo en el pulso, que empieza directamente
    offset = (
        score[track_index][0][1]
        if track_index == NUM_PLAYERS - 1
        else score[track_index][0][2]
    )

    for i, _, _ in score[track_index][1:]:
        offset = add_pattern_to_score(
            midi_track,
            pattern_index=i,
            octave_shift=12,
            start_time=offset,
            channel=track_index,
        )


save_score_to_midi(midi_score, "in_python_v03.mid")

resolution = n
drift = []
for position in range(0, max_dur, resolution):
    pattern_high = -1
    pattern_low = 999
    for track_index in range(NUM_PLAYERS - 1):
        for pattern_id, offset, duration in score[track_index]:
            if offset <= position < offset + duration:
                pattern_high = max(pattern_high, pattern_id if pattern_id != -1 else 0)
                pattern_low = min(pattern_low, pattern_id if pattern_id != -1 else 0)
    # print(
    #     f"{position:>6} |",
    #     f"{pattern_high - pattern_low}"
    # )
    drift.append(pattern_high - pattern_low)

colors = ["green" if v <= 3 else ("orange" if v <= 5 else "red") for v in drift]

plt.figure(figsize=(12, 3))
plt.grid(True, color='#ddd', linestyle='-', linewidth=0.5, zorder=0)  # Grid más visible y detrás
plt.scatter(range(len(drift)), drift, c=colors, marker="o", s=10, zorder=2)  # Puntos encima
plt.title("Separación entre intérpretes")
plt.xlabel("Tiempo (en negras)")
plt.ylabel("Distancia")
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

# Mostrar gráfico
plt.show()
