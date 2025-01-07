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

# Define pitch mapping for each DNA base within a chord interval based on the chord
chord_to_pitch_mapping = {
    "C": {"A": "C4", "T": "E4", "C": "G4", "G": "B4"},
    "G": {"A": "G4", "T": "B4", "C": "D5", "G": "F#5"},
    "D": {"A": "D4", "T": "F#4", "C": "A4", "G": "C#5"},
    "A": {"A": "A4", "T": "C#5", "C": "E5", "G": "G#5"},
    "E": {"A": "E4", "T": "G#4", "C": "B4", "G": "F4"},
    "B": {"A": "B4", "T": "D#5", "C": "F#5", "G": "A#5"},
    "F#": {"A": "F#4", "T": "A#4", "C": "C#5", "G": "E5"},
    "D-": {"A": "D-4", "T": "F4", "C": "A-4", "G": "C5"},
    "A-": {"A": "A-4", "T": "C5", "C": "E-5", "G": "G5"},
    "Am": {"A": "A4", "T": "C5", "C": "E5", "G": "G5"},
    "Em": {"A": "E4", "T": "G4", "C": "B4", "G": "D5"},
    "Bm": {"A": "B4", "T": "D5", "C": "F#5", "G": "A5"},
    "F#m": {"A": "F#4", "T": "A4", "C": "C#5", "G": "E5"},
    "C#m": {"A": "C#4", "T": "E4", "C": "G#4", "G": "B4"},
    "G#m": {"A": "G#4", "T": "B4", "C": "D#5", "G": "F#5"},
    "Bdim": {"A": "B4", "T": "D5", "C": "F5", "G": "A-5"},
    "F#dim": {"A": "F#4", "T": "A4", "C": "C5", "G": "E-5"},
    "C#dim": {"A": "C#4", "T": "E4", "C": "G4", "G": "B-4"},
    "Daug": {"A": "D4", "T": "F#4", "C": "A#4", "G": "C#5"},
    "Eaug": {"A": "E4", "T": "G#4", "C": "C5", "G": "D#5"}
}

# Read the input CSV and add new rows for the amino acid chords as a new instrument
input_file = "OG0002459_codon.csv"
output_file = "OG0002459_codon_with_chords.csv"

with open(input_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ["pitch", "amino_acid_chord"]

    original_rows = list(reader)
    new_rows = []

    # Update original rows to add pitch column and amino acid chord for each sequence
    for row in original_rows:
        amino_acid = row["codons"].strip() 
        chord = amino_acid_to_chord.get(amino_acid, "")
        if chord in chord_to_pitch_mapping:
            pitch = chord_to_pitch_mapping[chord].get(row["sequence"].upper(), "")
        else:
            pitch = ""
        row["pitch"] = pitch
        row["amino_acid_chord"] = chord

    # Create new rows for the amino acid chord instrument using only Sequence1
    for row in original_rows:
        if row["header"] == "Sequence1":
            amino_acid = row["codons"].strip()
            chord = amino_acid_to_chord.get(amino_acid, "")

            # Strip all chord qualities from the chord
            base_note = chord.replace("dim", "").replace("m", "").replace("aug", "") if chord else ""


            new_row = {
                "header": "SequenceX",
                "duration": row["duration"],
                "accent": row["accent"],
                "sequence": row["sequence"],
                "codons": row["codons"],
                "pitch": base_note + "4" if base_note else "",
                "amino_acid_chord": chord
            }
            new_rows.append(new_row)

# Write the updated rows to the new CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(original_rows + new_rows)
