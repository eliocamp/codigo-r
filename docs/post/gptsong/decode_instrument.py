def decode_instrument(instrument_name):
    # create a dictionary mapping instrument names to their values
    instrument_values = {
        "Acoustic Grand Piano": 0,
        "Bright Acoustic Piano": 1,
        "Electric Grand Piano": 2,
        "Honky-tonk Piano": 3,
        "Electric Piano 1": 4,
        "Electric Piano 2": 5,
        "Harpsichord": 6,
        "Clavi": 7,
        "Celesta": 8,
        "Glockenspiel": 9,
        "Music Box": 10,
        "Vibraphone": 11,
        "Marimba": 12,
        "Xylophone": 13,
        "Tubular Bells": 14,
        "Dulcimer": 15,
        "Drawbar Organ": 16,
        "Percussive Organ": 17,
        "Rock Organ": 18,
        "Church Organ": 19,
        "Reed Organ": 20,
        "Accordion": 21,
        "Harmonica": 22,
        "Tango Accordion": 23
    }

    # return the value corresponding to the given instrument name
    return instrument_values[instrument_name]

