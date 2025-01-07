import csv

# Codon to amino acid mapping
dna_to_amino_acid = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',  # Start codon (M)
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': 'Stop', 'TAG': 'Stop',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': 'Stop', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

# Read sequences from FASTA file
sequences = []

with open("OG0002459_codon.fasta", "r") as f:
    current_sequence = ""
    for line in f:
        if line.startswith(">"):
            if current_sequence:
                sequences.append(current_sequence)
                current_sequence = ""
        else:
            stripped_line = line.strip()
            current_sequence += stripped_line
    if current_sequence:
        sequences.append(current_sequence)

# The first sequence is the reference with introns
reference_sequence = sequences[1]  # Sequence 2 is the reference for intron/exon annotation

# Process each sequence and generate data for CSV output
data = []
for i, sequence in enumerate(sequences):
    codon_seq = [sequence[j:j + 3] for j in range(0, len(sequence), 3) if len(sequence[j:j + 3]) == 3]
    amino_acid_seq = [dna_to_amino_acid.get(codon, '') for codon in codon_seq]

    for j, base in enumerate(sequence):
        position_type = "exon" if reference_sequence[j] != "-" else "intron"
        amino_acid = amino_acid_seq[j // 3] if (position_type == "exon" and j // 3 < len(amino_acid_seq)) else ""

        # Add duration and accent information
        duration = 0.125
        accent = "accent" if (j % 3 == 0) else ""

        data.append([f"Sequence{i + 1}", j + 1, base, position_type, amino_acid, duration, accent])

# Write data to CSV
with open("OG0002459_codon.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["header", "position", "sequence", "type", "codons", "duration", "accent"])
    writer.writerows(data)
