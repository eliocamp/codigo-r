from midiutil.MidiFile import MIDIFile

# create the MIDIFile object with 1 track
midi = MIDIFile(1)

# add the track name and tempo
midi.addTrackName(0, 0, "My Simple Tune")
midi.addTempo(0, 0, 120)

# create a list of notes, durations, and volumes to add to the track
notes = [60, 62, 64, 65, 67, 69, 71]
durations = [1, 0.5, 0.25, 1, 0.75, 0.5, 2]
volumes = [100, 80, 60, 50, 40, 30, 20]

# initialize a variable to keep track of the total time elapsed
total_time = 0

# use a for loop to add each note to the track
for i, (note, duration, volume) in enumerate(zip(notes, durations, volumes)):
    # add the note with the specified duration and volume starting at the current total time
    midi.addNote(0, 0, note, total_time, duration, volume)
    # increment the total time by the duration of the current note
    total_time += duration

# write the MIDIFile to a file
with open("tune2.mid", "wb") as output_file:
    midi.writeFile(output_file)
