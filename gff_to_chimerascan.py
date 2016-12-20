# GFF to ChimeraScanGFF
# Parses GFF files to produce the genePredictions expected by ChimeraScan.
# Assumes genes are labeled 'gene' and exons are labeled 'CDS'

import argparse
from pprint import pprint

# Define & parse arguments.
parser = argparse.ArgumentParser()
# Input arguments.
parser.add_argument('-gff', type=str, required=True, help="GFF to parse")
parser.add_argument('-sep', type=str, required=False, default='\t', help="seperator")
# Flag arguments.
parser.add_argument('--header', action="store_true", help="GFF includes header")

args = parser.parse_args()

output = open(args.gff + '.parsed', 'w')
with open(args.gff, 'U') as gff:

    # Parse out header, if present.
    header = False
    if args.header:
        header = gff.readline()

    # Define genes object.
    # genes = {'gene_name': [chr, strand, start, stop, [exons..]]}
    ordered_genes = []
    genes = {}

    # Parse lines & populate genes object.
    for line in gff.readlines():
        values = line.strip().split(args.sep)
        c = values[0]  # Chromosome
        t = values[2]  # Type (i.e. gene, mRNA, CDS)
        s = values[3]  # Start
        e = values[4]  # End (stop)
        o = values[6]  # Orientation (strand)
        k = values[8]  # Keywords
        d = {}         # Description

        # Parse keywords.
        k = k.split(';')
        for keyword in k:
            key_value = keyword.split("=")
            d[key_value[0]] = key_value[1]

        # Handle genes.
        if t == 'gene':
            # Check if gene has an ID (name), if not issue warning.
            name = d.get('ID', None)
            if name == None:
                print("Warning: gene has no ID.")

            # Check if gene is already known. Add to list if unknown, warn if known.
            present = genes.get(name, None)
            if present == None:
                ordered_genes.append(name)
                genes[name] = [c, o, s, e, []]
            else:
                print("Warning: duplicate genes (%s) in file." % present)

        # Handle exons.
        if t == 'CDS':
            # Check if exon has a parent, warn if not.
            parent = d.get('Parent', None)
            if parent == None:
                print("Warning: exon has no parent.")

            # Check for parent gene, add exon to array.
            present = genes.get(parent, None)
            if present == None:
                # TODO: Implement ability to store misplaced exons and try placing after parsing file.
                print("Warning: exon seems misplaced")
            else:
                genes[name][4].append([s, e])

    # Parse genes & output to a file.
    for gene in ordered_genes:
        # ChimeraScan uses 11 tab-separated columns.
        # GeneID | Chromosome | Strand | Tstart | Tstop | Mstart | Mstop | exonCount | exonStarts | exonEnds | geneSymbol
        info = genes[gene]
        eCount = len(info[4])
        eStarts = ','.join([i[0] for i in info[4]]) + ','
        eEnds = ','.join([i[1] for i in info[4]]) + ','
        components = [gene, info[0], info[1], info[2], info[3], info[2], info[3], eCount, eStarts, eEnds, gene]
        entry = '\t'.join([str(c) for c in components]) + '\n'
        output.write(entry)

output.close()
