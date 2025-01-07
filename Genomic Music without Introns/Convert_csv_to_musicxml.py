import csv
from music21 import converter, stream, meter, instrument, note, chord, pitch, articulations

# Define the instrument mapping for each sequence
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

# Function to parse pitch and create a note object
def convert_to_music21(note_string):
    if not note_string:
        return note.Rest()  # Return a rest if pitch is empty
    try:
        return note.Note(note_string)
    except Exception as e:
        print(f"Error parsing note: {note_string} - {e}")
        return note.Rest()

# Initialize the score
score = stream.Score()
meter_obj = meter.TimeSignature('3/8')
score.append(meter_obj)

# Initialize a dictionary to store parts for each instrument
instrument_parts = {}

# Read the CSV file
input_file = "OG0002459_codon_with_chords.csv"

with open(input_file, "r") as csvfile:
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

        # Process chords for SequenceX
        if current_species == "SequenceX" and row["accent"].strip().lower() == "accent":
            root_note = row["pitch"]
            amino_acid_chord = row["amino_acid_chord"]
            scale_type = row["scale_type"].strip().lower()

            if root_note and amino_acid_chord and scale_type:
                try:
                    # Define the chord based on scale_type and amino_acid_chord
                    created_chord = chord.Chord()

                    if scale_type == "blues":
                        # Blues scale chord creation (dominant seventh chord)
                        created_chord.pitches = [
                            root_note,
                            pitch.Pitch(root_note).transpose(3).nameWithOctave,  # Minor third
                            pitch.Pitch(root_note).transpose(7).nameWithOctave,  # Perfect fifth
                            pitch.Pitch(root_note).transpose(10).nameWithOctave  # Minor seventh
                        ]
                    elif scale_type == "pentatonic":
                        # Pentatonic scale chord creation
                        created_chord.pitches = [
                            root_note,
                            pitch.Pitch(root_note).transpose(4).nameWithOctave,  # Major third
                            pitch.Pitch(root_note).transpose(7).nameWithOctave   # Perfect fifth
                        ]
                    elif scale_type == "mixolydian":
                        # Mixolydian mode chord creation (dominant seventh structure)
                        created_chord.pitches = [
                            root_note,
                            pitch.Pitch(root_note).transpose(4).nameWithOctave,  # Major third
                            pitch.Pitch(root_note).transpose(7).nameWithOctave,  # Perfect fifth
                            pitch.Pitch(root_note).transpose(10).nameWithOctave  # Minor seventh
                        ]
                    elif scale_type == "bebop":
                        # Bebop scale chord creation (extended chord with ninth)
                        created_chord.pitches = [
                            root_note,
                            pitch.Pitch(root_note).transpose(4).nameWithOctave,  # Major third
                            pitch.Pitch(root_note).transpose(7).nameWithOctave,  # Perfect fifth
                            pitch.Pitch(root_note).transpose(14).nameWithOctave  # Ninth
                        ]

                    created_chord.quarterLength = 1.5  # Dotted quarter note duration

                    # Add accent articulation
                    created_chord.articulations.append(articulations.Accent())

                    part.append(created_chord)
                except Exception as e:
                    print(f"Error creating chord for row: {row} - {e}")
        elif current_species != "SequenceX":
            # Handle individual notes for other sequences
            pitch_string = row["pitch"]
            note_obj = convert_to_music21(pitch_string)
            note_obj.quarterLength = 0.5

            if row["accent"].strip().lower() == "accent":
                note_obj.articulations.append(articulations.Accent())

            part.append(note_obj)

# Save the score to a MusicXML file
output_file = "OG0002459_codon_with_chords_test.musicxml"
score.write("musicxml", fp=output_file)
