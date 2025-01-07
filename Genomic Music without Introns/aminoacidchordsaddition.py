import csv

# Define chords for each amino acid category
non_polar_amino_acids = ['A', 'V', 'L', 'I', 'M', 'F', 'W', 'P', 'G']
polar_amino_acids = ['S', 'T', 'C', 'Y', 'N', 'Q']
basic_amino_acids = ['K', 'R', 'H']
acidic_amino_acids = ['D', 'E']

# Assign chords to each amino acid using specified scales
amino_acid_to_chord = {}

# Non-polar amino acids: Blues scale
blues_scale_chords = ['C7', 'E-7', 'F7', 'G7', 'B-7', 'A7', 'D7', 'G-7', 'B7']
for aa, chord in zip(non_polar_amino_acids, blues_scale_chords):
    amino_acid_to_chord[aa] = chord

# Polar amino acids: Pentatonic scale
pentatonic_scale_chords = ['A', 'C', 'D', 'E', 'G', 'B']
for aa, chord in zip(polar_amino_acids, pentatonic_scale_chords):
    amino_acid_to_chord[aa] = chord

# Basic amino acids: Mixolydian mode scale
mixolydian_scale_chords = ['C7', 'D7', 'E7']
for aa, chord in zip(basic_amino_acids, mixolydian_scale_chords):
    amino_acid_to_chord[aa] = chord

# Acidic amino acids: Bebop scale
bebop_scale_chords = ['D9', 'G13']
for aa, chord in zip(acidic_amino_acids, bebop_scale_chords):
    amino_acid_to_chord[aa] = chord

# Define pitch mapping for each DNA base within a scale based on the scale type
chord_to_pitch_mapping = {
    # Blues scale chords
    "C7": {"A": "C4", "T": "E-4", "C": "F4", "G": "G4"},
    "E-7": {"A": "E4", "T": "G4", "C": "A4", "G": "B4"},
    "F7": {"A": "F4", "T": "A4", "C": "B4", "G": "C4"},
    "G7": {"A": "G4", "T": "B4", "C": "C4", "G": "D4"},
    "B-7": {"A": "B4", "T": "D4", "C": "E4", "G": "F4"},
    "A7": {"A": "A4", "T": "C#4", "C": "D4", "G": "E4"},
    "D7": {"A": "D4", "T": "F#4", "C": "G4", "G": "A4"},
    "G-7": {"A": "G4", "T": "B4", "C": "C4", "G": "D4"},
    "B7": {"A": "B4", "T": "D#4", "C": "E4", "G": "F#4"},

    # Pentatonic scale chords (A Pentatonic: A, B, C#, E)
    "A": {"A": "A4", "T": "B4", "C": "C#4", "G": "E4"},
    "C": {"A": "C4", "T": "D4", "C": "E4", "G": "G4"},
    "D": {"A": "D4", "T": "E4", "C": "F#4", "G": "A4"},
    "E": {"A": "E4", "T": "F#4", "C": "G#4", "G": "B4"},
    "G": {"A": "G4", "T": "A4", "C": "B4", "G": "D4"},
    "B": {"A": "B4", "T": "C#4", "C": "D#4", "G": "F#4"},

    # Mixolydian scale chords (C Mixolydian: C, D, E, F)
    "C7": {"A": "C4", "T": "D4", "C": "E4", "G": "F4"},
    "D7": {"A": "D4", "T": "E4", "C": "F#4", "G": "G4"},
    "E7": {"A": "E4", "T": "F#4", "C": "G#4", "G": "A4"},

    # Bebop scale chords (D Bebop: D, E, F, G)
    "D9": {"A": "D4", "T": "E4", "C": "F4", "G": "G4"},
    "G13": {"A": "G4", "T": "A4", "C": "B4", "G": "C4"}
}


# Read the input CSV and add new rows for the amino acid chords as a new instrument
input_file = "OG0002459_codon.csv"
output_file = "OG0002459_codon_with_chords.csv"

with open(input_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ["pitch", "amino_acid_chord", "scale_type"]

    original_rows = list(reader)
    new_rows = []

    # Update original rows to add pitch column, amino acid chord, and scale type for each sequence
    for row in original_rows:
        amino_acid = row["codons"].strip()
        chord = amino_acid_to_chord.get(amino_acid, "")
        scale_type = ""
        if amino_acid in non_polar_amino_acids:
            scale_type = "blues"
        elif amino_acid in polar_amino_acids:
            scale_type = "pentatonic"
        elif amino_acid in basic_amino_acids:
            scale_type = "mixolydian"
        elif amino_acid in acidic_amino_acids:
            scale_type = "bebop"

        if chord in chord_to_pitch_mapping:
            pitch = chord_to_pitch_mapping[chord].get(row["sequence"].upper(), "")
        else:
            pitch = ""
        row["pitch"] = pitch
        row["amino_acid_chord"] = chord
        row["scale_type"] = scale_type

    # Create new rows for the amino acid chord instrument using only Sequence1
    for row in original_rows:
        if row["header"] == "Sequence1":
            amino_acid = row["codons"].strip()
            chord = amino_acid_to_chord.get(amino_acid, "")
            scale_type = ""
            if amino_acid in non_polar_amino_acids:
                scale_type = "blues"
            elif amino_acid in polar_amino_acids:
                scale_type = "pentatonic"
            elif amino_acid in basic_amino_acids:
                scale_type = "mixolydian"
            elif amino_acid in acidic_amino_acids:
                scale_type = "bebop"

            # Strip all chord qualities from the chord
            base_note = chord.replace("7", "").replace("13", "").replace("-", "").replace("9", "") if chord else ""

            new_row = {
                "header": "SequenceX",
                "duration": row["duration"],
                "accent": row["accent"],
                "sequence": row["sequence"],
                "codons": row["codons"],
                "pitch": base_note + "4" if base_note else "",
                "amino_acid_chord": chord,
                "scale_type": scale_type
            }
            new_rows.append(new_row)

# Write the updated rows to the new CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(original_rows + new_rows)
