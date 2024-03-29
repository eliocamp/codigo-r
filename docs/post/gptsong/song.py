# create a list of notes, durations, and volumes for the right hand part (first verse)
right_notes_1 = [
    62, 65, 69, 72,  # D major
    57, 60, 64, 67,  # A major
    59, 62, 66, 69,  # B minor
    54, 57, 61, 64,  # F# minor
    55, 58, 62, 65,  # G major
    62, 65, 69, 72,  # D major
    55, 58, 62, 65,  # G major
    57, 60, 64, 67   # A major
]
right_durations_1 = [1, 1, 1, 1] * 8  # each note is 1 beat
right_volumes_1 = [100, 90, 80, 70] * 8  # each note has a different volume

# create a list of notes, durations, and volumes for the right hand part (second verse)
right_notes_2 = [
    62, 63, 65, 66, 67, 69, 70, 72,  # D major
    57, 58, 60, 61, 62, 64, 65, 67,  # A major
    59, 60, 62, 63, 64, 66, 67, 69,  # B minor
    54, 55, 57, 58, 59, 61, 62, 64,  # F# minor
    55, 56, 58, 59, 60, 62, 63, 65,  # G major
    62, 63, 65, 66, 67, 69, 70, 72,  # D major
    55, 56, 58, 59, 60, 62, 63, 65,  # G major
    57, 58, 60, 61, 62, 64, 65, 67   # A major
]
right_durations_2 = [0.5, 0.5, 0.5, 0.5] * 32  # each note is 1/4 beat
right_volumes_2 = [100, 90, 80, 70] * 32  # each note has a different volume



# create a list of notes, durations, and volumes for the right hand part (second verse)
right_notes_2 = [
    62, 63, 65, 66, 67, 69, 70, 72,  # D major
    62, 63, 65, 66, 67, 69, 70, 72,  # D major
    57, 58, 60, 61, 62, 64, 65, 67,  # A major
    57, 58, 60, 61, 62, 64, 65, 67,  # A major
    59, 60, 62, 63, 64, 66, 67, 69,  # B minor
    59, 60, 62, 63, 64, 66, 67, 69,  # B minor
    54, 55, 57, 58, 59, 61, 62, 64,  # F# minor
    54, 55, 57, 58, 59, 61, 62, 64,  # F# minor
    55, 56, 58, 59, 60, 62, 63, 65,  # G major
    55, 56, 58, 59, 60, 62, 63, 65,  # G major
    62, 63, 65, 66, 67, 69, 70, 72,  # D major
    62, 63, 65, 66, 67, 69, 70, 72,  # D major
    55, 56, 58, 59, 60, 62, 63, 65,  # G major
    55, 56, 58, 59, 60, 62, 63, 65,  # G major
    57, 58, 60, 61, 62, 64, 65, 67,   # A major
    57, 58, 60, 61, 62, 64, 65, 67   # A major
]
right_durations_2 = [0.25, 0.25, 0.25, 0.25] * 32  # each note is 1/4 beat
right_volumes_2 = [100, 90, 80, 70] * 32  # each note has a different volume



# combine the notes, durations, and volumes of the first and second verses
right_notes = right_notes_1 + right_notes_2
right_durations = right_durations_1 + right_durations_2
right_volumes = right_volumes_1 + right_volumes_2

# create a list of notes, durations, and volumes for the left hand part
left_notes = [
    50, 45, 47, 42, 43, 50, 43, 45  # D major, A major, B minor, F# minor, G major, D major, G major, A major
] * 2
left_durations = [4, 4, 4, 4, 4, 4, 4, 4] * 2  # each note is a whole note
left_volumes = [100, 100, 100, 100, 100, 100, 100, 100] * 2  # each note has the same volume


# set the instrument for each track
right_instrument = "Acoustic Grand Piano"
left_instrument = "Acoustic Grand Piano"

