from midiutil.MidiFile import MIDIFile

# import the decode_instrument function
from decode_instrument import decode_instrument

# create the MIDIFile object with 2 tracks
midi = MIDIFile(2)

# add the track names and tempo
midi.addTrackName(0, 0, "Right Hand")
midi.addTrackName(1, 0, "Left Hand")
midi.addTempo(0, 0, 120)

# load the notes, durations, volumes, and instruments from the song.py file
from song import right_notes, right_durations, right_volumes, right_instrument
from song import left_notes, left_durations, left_volumes, left_instrument

# set the instrument for each track using the decode_instrument function
midi.addProgramChange(0, 0, 0, decode_instrument(right_instrument))
midi.addProgramChange(1, 0, 0, decode_instrument(left_instrument))

# initialize a variable to keep track of the total time elapsed
total_time = 0

# use a for loop to add each note to the right hand track
for i, (note, duration, volume) in enumerate(zip(right_notes, right_durations, right_volumes)):
    # add the note with the specified duration and volume starting at the current total time
    midi.addNote(0, 0, note, total_time, duration, volume)
    # increment the total time by the duration of the current note
    total_time += duration

# reset the total time to 0 for the left hand track
total_time = 0

# use a for loop to add each note to the left hand track
for i, (note, duration, volume) in enumerate(zip(left_notes, left_durations, left_volumes)):
    # add the note with the specified duration and volume starting at the current total time
    midi.addNote(1, 0, note, total_time, duration, volume)
    # increment the total time by the duration of the current note
    total_time += duration

# write the MIDIFile to a file
with open("piano_song.mid", "wb") as output_file:
    midi.writeFile(output_file)
