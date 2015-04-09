__author__ = 'asherkhb'
# index_vcf.py
#
# Script that converts a VCF into an index of IDs and binary locations in VCF for that ID
# For quickly finding IDs in very large VCFs
# Requires VCF-formatted input.
#
# Script Usage: Requires 1 Argument (File to Index)
# index_vcf.py <file_to_index>
#
# Index Usage Example:
# import cPickle as pickle
# index = pickle.load(open(generate_index_file.p, 'rb'))
# with open(file_of_interest, 'r') as yourfile:
#     wanted_id = 'id'
#     wanted_id_location = index[wanted_id]
#     yourfile.seek(wanted_id_location)
#     print yourfile.readline()

import cPickle as pickle
from sys import argv

#Establish input/output file names
inputfile = argv[1]
outputfile = '%s.p' % inputfile

#Create an empty index dictionary.
rsid_index = {}

with open(inputfile, 'r') as indexing_file:
    reading = True
    data = False
    while reading:
        #Get index of line start and line contents.
        index = indexing_file.tell()
        line = indexing_file.readline()

        #End reading loop at end of file.
        if line == '':
            reading = False
            continue
        #Mark beginning of data.
        elif line[0:6] == "#CHROM":
            data = True
            continue

        #Create entries for each datapoint.
        if data:
            line_split = line.split('\t')
            rsid = line_split[2]
            rsid_index[rsid] = index

#Dump index to a new file.
pickle.dump(rsid_index, open(outputfile, "wb"))


print('Indexing of "%s" complete.' % inputfile)