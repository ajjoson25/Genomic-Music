import csv

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

# Polar amino acids: Minor 6 chords around the circle of 5ths starting from A minor
minor_chords = ['A', 'E', 'B', 'F#', 'C#', 'G#']
for aa, chord in zip(polar_amino_acids, minor_chords):
    amino_acid_to_chord[aa] = f"{chord}m"

# Basic amino acids: Fully diminished 7th chords
diminished_chords = ['B', 'F#', 'C#']
for aa, chord in zip(basic_amino_acids, diminished_chords):
    amino_acid_to_chord[aa] = f"{chord}dim"

# Acidic amino acids: Minor 7th chords
augmented_chords = ['D', 'E']
for aa, chord in zip(acidic_amino_acids, augmented_chords):
    amino_acid_to_chord[aa] = f"{chord}aug"

# Define pitch mapping for each DNA base using the new intervals (C D E B) within the same octave
chord_to_pitch_mapping = {
    "C": {"A": "C4", "T": "D4", "C": "E4", "G": "B3"},
    "G": {"A": "G4", "T": "A4", "C": "B3", "G": "D4"},
    "D": {"A": "D4", "T": "E4", "C": "F#4", "G": "B3"},
    "A": {"A": "A4", "T": "B3", "C": "C#4", "G": "E4"},
    "E": {"A": "E4", "T": "F#4", "C": "G#4", "G": "B3"},
    "B": {"A": "B4", "T": "C#4", "C": "D#4", "G": "E4"},
    "F#": {"A": "F#4", "T": "G#4", "C": "A#4", "G": "B3"},
    "D-": {"A": "D-4", "T": "E-4", "C": "F4", "G": "B-3"},
    "A-": {"A": "A-4", "T": "B-3", "C": "C4", "G": "D4"},
    "Am": {"A": "A4", "T": "B3", "C": "C4", "G": "D4"},
    "Em": {"A": "E4", "T": "F#4", "C": "G4", "G": "B3"},
    "Bm": {"A": "B4", "T": "C#4", "C": "D4", "G": "E4"},
    "F#m": {"A": "F#4", "T": "G#4", "C": "A4", "G": "B3"},
    "C#m": {"A": "C#4", "T": "D#4", "C": "E4", "G": "B3"},
    "G#m": {"A": "G#4", "T": "A#4", "C": "B4", "G": "D4"},
    "Bdim": {"A": "B4", "T": "D4", "C": "F4", "G": "B-3"},
    "F#dim": {"A": "F#4", "T": "A4", "C": "C4", "G": "B3"},
    "C#dim": {"A": "C#4", "T": "E4", "C": "G4", "G": "B-3"},
    "Daug": {"A": "D4", "T": "F#4", "C": "A#4", "G": "B3"},
    "Eaug": {"A": "E4", "T": "G#4", "C": "C4", "G": "B3"}
}

# Define pitch mapping for intron segments (A, T, C, G)
intron_pitch_mapping = {
    "A": "A4",
    "T": "E4",
    "C": "C4",
    "G": "G4"
}

# Read the input CSV and add new rows for the amino acid chords as a new instrument
input_file = "extracted_sequences.csv"
output_file = "extracted_sequences_updated.csv"

with open(input_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ["pitch", "amino_acid_chord", "accent"]

    original_rows = list(reader)
    new_rows = []

    # Update original rows to add pitch column, amino acid chord, and accent for each sequence
    for row in original_rows:
        amino_acid = row["codons"].strip()
        chord = amino_acid_to_chord.get(amino_acid, "")
        if chord in chord_to_pitch_mapping:
            pitch = chord_to_pitch_mapping[chord].get(row["sequence"].upper(), "")
        else:
            pitch = ""

        # Assign pitch for intron segments if type is intron
        if row["type"].strip().lower() == "intron":
            pitch = intron_pitch_mapping.get(row["sequence"].upper(), "")

        row["pitch"] = pitch
        row["amino_acid_chord"] = chord
        row["accent"] = ""

    # Create new rows for the amino acid chord instrument using only Sequence2, and only for exon type
    for row in original_rows:
        if row["header"] == "Sequence2" and row["codons"].strip() and row["type"].strip().lower() == "exon":
            amino_acid = row["codons"].strip()
            chord = amino_acid_to_chord.get(amino_acid, "")
            root_note = chord.rstrip('m').rstrip('dim').rstrip('aug')  # Remove chord suffixes correctly
            pitch = root_note + "2" if root_note else ""
            new_row = {
                "header": "SequenceX",
                "position": row["position"],
                "sequence": row["sequence"],
                "type": row["type"],
                "codons": row["codons"],
                "pitch": pitch,
                "amino_acid_chord": chord,
                "accent": ""
            }
            new_rows.append(new_row)
        elif row["header"] == "Sequence2" and row["type"].strip().lower() == "intron":
            # Add an empty row for intron type in SequenceX
            new_row = {
                "header": "SequenceX",
                "position": row["position"],
                "sequence": row["sequence"],
                "type": row["type"],
                "codons": row["codons"],
                "pitch": "",
                "amino_acid_chord": "",
                "accent": ""
            }
            new_rows.append(new_row)

# Write the updated rows to the new CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(original_rows + new_rows)
