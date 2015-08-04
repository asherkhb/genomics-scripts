__author__ = 'asherkhb'
# VCF 2 FASTA (v. 0.1)
# Incorporates SNPs into FASTA files
# For Mosher Lab

from os import path
from csv import reader

input_seq = path.expanduser('~/Downloads/E1_Osativa_japonica_CDS.fasta')
input_vcf = path.expanduser('~/Downloads/snp3kvars-loc_os02g05880.csv')  # Using CSV currently
otpt = 'output.fasta'
ref = 'E1_O.sativa_japonica_CDS'
start_loc = 2904357

# Build an array holding the reference sequence
seq_array = {}
with open(input_seq, 'U') as seq_in:
    s = seq_in.read().split('\n')
    seq_head = s[0]
    seq_array[ref] = s[1]

# Build an array holding the vcf contents
vcf_array = []
with open(input_vcf, 'U') as vcf_in:
    v = reader(vcf_in)
    vcf_head = next(v)
    substitutions = [int(x)-start_loc for x in vcf_head[4:]]  # NOTE: Off by 1 errors can be adjusted here (if needed)
    for row in v:
        vcf_array.append(row)

# Apply changes from VCF to reference and print out to an output FASTA
index_error_count = 0
with open(otpt, 'w') as out:
    out.write(seq_head + ', REFERENCE\n')
    out.write(seq_array[ref] + '\n')
    for entry in vcf_array:
        heading = '>' + ', '.join(entry[:4]) + '\n'
        del entry[:4]
        to_change = zip(substitutions, entry)
        conversion = list(seq_array[ref])
        for change in to_change:
            try:
                if len(change[1]) > 1:
                    conversion[change[0]] = change[1][0]  # Implements first if multiple present
                else:
                    conversion[change[0]] = change[1]
            except IndexError:
                index_error_count += 1
        conversion = ''.join(conversion) + '\n'
        out.write(heading)
        out.write(conversion)
print "You had %s index errors. Not all SNPs were incorporated. Check out input reference sequence length!" % \
      str(index_error_count)
