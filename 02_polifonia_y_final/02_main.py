# In Python
# V 2.0

# Hacemos el sistema multi instrumentos
# Alargamos las piezas para que acaben más o menos a la vez
# Intercalamos las entradas de los instrumentos
# Selección de instrumentos General MIDI un poco mejor pensada
# Añadimos un poco de panorama estereo
# Añadimos un poco de "Humanize" a la velocidad y a la duración de la nota

from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from patterns import patterns, r, b
import random


def create_score(num_tracks, instruments, bpm=120):
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
    return int(2 * sum(msg.time for msg in track) / MidiFile.ticks_per_beat)


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

score = create_score(NUM_PLAYERS, [0, 4, 6, 9, 12, 16, 18, 21, 24, 27, 29, 10], BPM)
max_dur = 0

# reservamos la última pista para El Pulso
for track_index in range(NUM_PLAYERS - 1):

    track = score.tracks[track_index]
    # Cada track empieza tras una pausa de una redonda y entre 0 y 8 blancas
    offset = r + random.randint(0, 9) * b

    for i in range(1, len(patterns)):
        for rep in range(random.randint(3, 6)):
            offset = add_pattern_to_score(
                track,
                pattern_index=i,
                octave_shift=12,
                start_time=offset,
                channel=track_index,
            )
    max_dur = max(max_dur, get_track_duration(track))

for track_index in range(NUM_PLAYERS - 1):
    # print(f"Duración de la pista {track_index}: {get_track_duration(score.tracks[track_index])} corcheas")
    offset = 0
    while get_track_duration(score.tracks[track_index]) < max_dur:
        offset = add_pattern_to_score(
            score.tracks[track_index],
            pattern_index=len(patterns) - 1,
            octave_shift=12,
            start_time=offset,
            channel=track_index,
        )
    # print(f"   {get_track_duration(score.tracks[track_index])} corcheas")

print(f"Duración máxima: {max_dur} corcheas")

# El Pulso
track = score.tracks[NUM_PLAYERS - 1]
offset = 0
for i in range(max_dur):
    offset = add_pattern_to_score(
        track,
        pattern_index=0,
        octave_shift=12,
        start_time=offset,
        channel=NUM_PLAYERS - 1,
        velocity=64,
    )
save_score_to_midi(score, "in_python_v02.mid")
