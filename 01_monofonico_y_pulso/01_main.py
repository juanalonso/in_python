# In Python
# V 1.0

# El pulso
# Añadimos el pulso a la partitura

from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from patterns import patterns, r
import random


def create_score(num_tracks, instruments, bpm=120):
    mid = MidiFile()
    for i in range(num_tracks):

        track = MidiTrack()

        # Solo necesitamos indicar el tempo una vez
        if i == 0:
            track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))

        instrument = instruments[i] if i < len(instruments) else 1
        track.append(Message("program_change", program=instrument, channel=i, time=0))

        mid.tracks.append(track)

    return mid


def add_pattern_to_score(
    track, pattern_index, octave_shift=0, start_time=0, channel=0, vel=64
):

    def add_note(note_num, vel, time, on=True):
        msg_type = "note_on" if on else "note_off"
        track.append(
            Message(msg_type, note=note_num, velocity=vel, channel=channel, time=time)
        )

    pattern = patterns[pattern_index]
    delta_time = start_time  # por si arrastramos silencios al final de un patrón

    for duration, note in pattern:
        if note == 0:  # Silencio
            delta_time += duration
        else:
            shifted_note = note + octave_shift
            add_note(shifted_note, vel, delta_time, True)  # Note on
            add_note(shifted_note, vel, duration, False)  # Note off
            delta_time = 0  # Cosas del MIDI

    return delta_time


def save_score_to_midi(midi_file, filename="output.mid"):

    midi_file.save(filename)


def get_track_duration(track):
    return int(2 * sum(msg.time for msg in track) / MidiFile.ticks_per_beat)


score = create_score(2, [0, 10], 130)  # 2 tracks, piano y glockenspiel, 130 BPM

track_0 = score.tracks[0]
offset = r

for i in range(1, len(patterns)):
    for rep in range(random.randint(2, 5)):
        offset = add_pattern_to_score(
            track_0, pattern_index=i, octave_shift=0, start_time=offset, channel=0
        )
track_0_dur = get_track_duration(track_0)

print(f"Duración del track 0: {track_0_dur} corcheas")

track_1 = score.tracks[1]
offset = 0
for i in range(track_0_dur):
    offset = add_pattern_to_score(
        track_1, pattern_index=0, octave_shift=12, start_time=offset, channel=1, vel=32
    )
save_score_to_midi(score, "in_python_v01.mid")
