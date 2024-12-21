import csv

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

sequences = []

with open("extracted_gene_sequences.fa", "r") as f:
    current_sequence = ""
    for line in f:
        if line.startswith(">"):
            if current_sequence:
                sequences.append(current_sequence.upper())
                current_sequence = ""
        else:
            stripped_line = line.strip()
            current_sequence += stripped_line
    if current_sequence:
        sequences.append(current_sequence.upper())

# The first sequence is the reference with introns
reference_sequence = sequences[1]  # Sequence 2 is the reference for intron/exon annotation

# Read CDS regions from input text file
cds_regions = []
with open("gene_and_cds_coordinates.tsv", "r") as cds_file:
    start_offset = None
    for line_num, line in enumerate(cds_file):
        if line_num == 0:
            continue  # Skip header line
        parts = line.strip().split('\t')
        if len(parts) > 4 and "CDS" in parts:
            try:
                start = int(parts[1])
                end = int(parts[2])
                cds_regions.append((start, end))
                print(f"CDS Region - Start: {start}, End: {end}, Type: CDS")
            except ValueError as e:
                print(f"Error parsing start/end positions: {e}")
        if start_offset is None and len(parts) > 1:
            try:
                start_offset = int(parts[1])  # Use the first start position as the offset
                print(f"Start offset set to: {start_offset}")
            except ValueError as e:
                print(f"Error parsing start offset: {e}")

data = []

# Process each sequence and generate codons and intron/exon information
for i, sequence in enumerate(sequences):
    # Generate rows for CSV output
    for j in range(0, len(sequence), 3):
        if len(sequence[j:j + 3]) == 3:
            codon = sequence[j:j + 3]
            position = start_offset + j  # Adjusted position based on the offset from the input file
            position_type = "intron"
            for start, end in cds_regions:
                if start <= position <= end:
                    position_type = "exon"
                    break
            amino_acid = dna_to_amino_acid.get(codon, '') if position_type == "exon" else ""
            for k in range(3):
                if j + k < len(sequence):
                    base = sequence[j + k]
                    data.append([f"Sequence{i + 1}", position + k, base, position_type, amino_acid])  # Add amino acid for all three bases of the codon

# Write to CSV
with open("extracted_sequences.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["header", "position", "sequence", "type", "codons"])
    writer.writerows(data)
