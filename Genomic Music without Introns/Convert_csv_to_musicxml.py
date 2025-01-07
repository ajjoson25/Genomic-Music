import csv
from music21 import converter, midi, stream, meter, instrument, pitch, note, articulations, chord as m21_chord

species_instrument_map = {
    "Sequence1": instrument.Piano(),
    "Sequence2": instrument.Piano(),
    "Sequence3": instrument.Piano(),
    "Sequence4": instrument.Piano(),
    "Sequence5": instrument.Piano(),
    "Sequence6": instrument.Piano(),
    "Sequence7": instrument.Piano(),
    "Sequence8": instrument.Piano(),
    "SequenceX": instrument.Piano(),
}

default_instrument = instrument.Piano()

# Define chords for each amino acid category
non_polar_amino_acids = ['A', 'V', 'L', 'I', 'M', 'F', 'W', 'P', 'G']
polar_amino_acids = ['S', 'T', 'C', 'Y', 'N', 'Q']
basic_amino_acids = ['K', 'R', 'H']
acidic_amino_acids = ['D', 'E']

# Assign chords to each amino acid
amino_acid_to_chord = {}

# Non-polar amino acids: Major chords around the circle of 5ths starting from C
major_chords = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'D-', 'A-']
for aa, chord in zip(non_polar_amino_acids, major_chords):
    amino_acid_to_chord[aa] = f"{chord}"

# Polar amino acids: Minor chords around the circle of 5ths starting from A minor
minor_chords = ['A', 'E', 'B', 'F#', 'C#', 'G#']
for aa, chord in zip(polar_amino_acids, minor_chords):
    amino_acid_to_chord[aa] = f"{chord}m"

# Basic amino acids: Diminished chords
diminished_chords = ['B', 'F#', 'C#']
for aa, chord in zip(basic_amino_acids, diminished_chords):
    amino_acid_to_chord[aa] = f"{chord}dim"

# Acidic amino acids: Augmented chords
augmented_chords = ['D', 'E']
for aa, chord in zip(acidic_amino_acids, augmented_chords):
    amino_acid_to_chord[aa] = f"{chord}aug"

def convert_to_music21(note_string):
    if not note_string:
        return note.Rest()  # Use note.Rest() directly
    try:
        pitch_string, octave_string = note_string[:-1], note_string[-1]
        if not pitch_string or not octave_string.isdigit():
            return note.Rest()
        return note.Note(pitch.Pitch(pitch_string + octave_string))
    except Exception as e:
        print(f"Error converting note_string '{note_string}': {e}")
        return note.Rest()

score = stream.Score()
meter_obj = meter.TimeSignature('3/8')
score.insert(0, meter_obj)

# Initialize a dictionary to store parts for each instrument
instrument_parts = {}

# Read the CSV file
with open("OG0002459_codon_with_chords.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        current_species = row["header"]
        instrument_obj = species_instrument_map.get(current_species, default_instrument)

        # Create or retrieve the part for the current instrument
        part = instrument_parts.get(current_species)
        if part is None:
            part = stream.Part()
            part.insert(0, instrument_obj)
            instrument_parts[current_species] = part
            score.append(part)

        # Handle SequenceX to create chords
        if current_species == "SequenceX":
            # Create a triad based on the root note from the pitch column
            root_note = row["pitch"]
            amino_acid = row["codons"].strip()
            chord_type = amino_acid_to_chord.get(amino_acid, "")
            if root_note:
                try:
                    # Define triad notes based on the root, all within the same octave
                    if "m" in chord_type:
                        third_interval = 3  # Minor third
                    elif "dim" in chord_type:
                        third_interval = 3  # Minor third for diminished
                    elif "aug" in chord_type:
                        third_interval = 4  # Major third for augmented
                    else:
                        third_interval = 4  # Major third for major triad

                    if "dim" in chord_type:
                        fifth_interval = 6  # Diminished fifth
                    elif "aug" in chord_type:
                        fifth_interval = 8  # Augmented fifth
                    else:
                        fifth_interval = 7  # Perfect fifth for major and minor triads

                    triad_notes = [
                        root_note,
                        pitch.Pitch(root_note).transpose(third_interval).nameWithOctave,  # Third in the same octave
                        pitch.Pitch(root_note).transpose(fifth_interval).nameWithOctave   # Fifth in the same octave
                    ]
                    chord_obj = m21_chord.Chord(triad_notes)
                    chord_obj.duration.quarterLength = 1.5  # Set duration to eighth note
                    # Add accent if specified in the CSV
                    if row["accent"].strip().lower() == "accent":
                        accent_articulation = articulations.Accent()
                        chord_obj.articulations.append(accent_articulation)
                    part.append(chord_obj)
                except ValueError:
                    print(f"Invalid pitch value in row: {row}")
                    continue
        else:
            # Parse each note and set duration
            try:
                note_obj = convert_to_music21(row["pitch"])
                note_obj.duration.quarterLength = 0.5  # Set duration to eighth note
            except ValueError:
                print(f"Invalid duration value in row: {row}")
                continue

            # Add accent if specified in the CSV
            if row["accent"].strip().lower() == "accent":
                accent_articulation = articulations.Accent()
                note_obj.articulations.append(accent_articulation)

            part.append(note_obj)

# Export score to MusicXML
score.write('musicxml', fp='OG0002459_codon_with_chords_test.musicxml')
