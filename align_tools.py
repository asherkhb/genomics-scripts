__author__ = 'asherkhb'
# alignment-tools.py
#
# A collection of quick and dirty tools for doing miscellaneous things to/with MSAs
# '*' Indicate poor-quality, basically useless scripts
#
# Includes
#   - species_with_data
#   - fasta_align_to_list
#   - condenser*
#   - identity_calculator
#   - generate_similarity_tsv
#   - generate_site-identity_tsv

from sys import argv


def species_with_data(msa, outputfile):
    """Species with Data in an MSA
    Determines which species possess sequence data in a MSA.
    Usage: species_with_data(<MSA>) <output_file_name>
       * outputfile will contain only those species which have sequence data.
       * outputfile.csv will contain a table of species and their percent coverage over the sequence.

    :param msa: Multiple sequence alignment in PhyLip format (.phy)
    """
    out_file = outputfile
    file_summary = '%s_coverage.csv' % outputfile
    first_line = True
    spp_count = 0
    seq_length = 0
    data_points = {} # name:sequence key:value pairs
    with open(msa, 'r') as inpt:
        for line in inpt:

            # Process data lines
            if not first_line:
                line_data = []
                contents = line.split(' ')
                for item in contents:
                    item = item.strip('\n')
                    line_data.append(item)

                #Define name and sequence variables
                name = line_data[0]
                sequence = line_data[1]

                presence = False
                bases = 0
                gaps = 0
                for i in range(0, len(sequence)):
                    if sequence[i] == '-':
                        gaps += 1
                    else:
                        bases += 1
                        presence = True

                if presence:
                    coverage = float(bases) / seq_length
                    coverage = float("{0:.3f}".format(coverage))
                    #Add entry into data_points dictionary.
                    data_points[name] = {'seq':sequence, 'coverage':coverage}

             # Process first line
            else:
                msa_info = []
                contents = line.split(' ')
                for item in contents:
                    item = item.strip('\n')
                    item = int(item)
                    msa_info.append(item)

                # Define species count and sequence length.
                spp_count = msa_info[0]
                seq_length = msa_info[1]

                #End first line loop.
                first_line = False

    with open(msa, 'r') as inpt, open(out_file, 'w') as otpt, open(file_summary, 'w') as summary:
        spp_number = len(data_points)
        new_head = '%s %s\n' % (spp_number, seq_length)
        otpt.write(new_head)
        for line in inpt:
            contents = line.split(' ')
            if contents[0] in data_points:
                #Write line to output file
                otpt.write(line)

                #Write summary entry
                key = contents[0]
                coverage = data_points[key]['coverage']
                summary_entry = '%s,%s\n' % (key, coverage)
                summary.write(summary_entry)


def fasta_alignment_to_list(alignment_file):
    """FASTA-format MSA to List
    Converts multiple sequence alignments (in FASTA format) to lists.
    Generates file with single-line sequences,

    Returns a list of lists of sequences.

    :param alignment_file:
    """
    sequences = []

    with open(alignment_file, 'r') as alignment, open('temp-align-out.txt', 'w') as otpt:
        reading = True
        first = True
        while reading:
            line = alignment.readline()
            if line == '':
                reading = False
            elif line[0] == '>':
                if first:
                    otpt.write(line)
                    first = False
                else:
                    otpt.write('\n' + line)
            else:
                line = line.strip('\n')
                otpt.write(line)

    with open('temp-align-out.txt', 'r') as aligned_seq:
        reading = True
        while reading:
            line = aligned_seq.readline()
            if line == '':
                reading = False
            elif line[0] == '>':
                pass
            else:
                line = line.strip('\n')
                sequences.append(line)

    #for sequence in sequences:
    #    print sequence
    #    print len(sequence)

    return sequences

def condenser(alignment_file, lines):
    """MSA Condenser

    Not a good script, very fussy.
    Condenses MSA into single-lines and returns scored.
    Will be redone (eventually)

    :param alignment_file:
    :param lines: Number of lines that make up each iteration of alignment
    :return: Scores (* indicating 100% seq. identity output by MUSCLE)
    """
    with open(alignment_file, 'r') as inpt, open('condensed-alignment.txt', 'w') as otpt:
        sequences = []
        for i in range(0, lines-1):
            sequences.append([])

        reading = True
        line_counter = 0
        while reading:
            line = inpt.readline()
            if line == '':
                reading = False
            elif line == '\n':
                pass
            else:
                line = line.strip('\n')
                sequences[line_counter].append(line)
                line_counter += 1
                if line_counter == lines-1:
                    line_counter = 0

        for i in range(0, len(sequences)):
            entry = ''.join(sequences[i])
            otpt.write(entry + '\n')
            #print len(entry)
            if i == len(sequences) - 1:
                scores = entry

    return scores


def generate_similarity_tsv(scores):
    """Similarity TSV Generator

    From a string of identity values (as generated by MUSCLE - * indicate 100% identity).
    Generate a TSV of site locations & identity conservation.
    Only functions to generate report for 100% similarity.
    For specific percentages, use "generate_site_identity_tsv"

    :param scores: String of identity values for a MSA.
    """
    seq_len = len(scores)
    with open('similarity-chart.tsv', 'w') as otpt:
        otpt.write('Site\t% Identity\n')
        for i in range (0, seq_len):
            site = i + 1
            if scores[i] == ' ':
                score = 0
            elif scores[i] == '*':
                score = 1
            entry = '%d\t%d\n' % (site, score)
            otpt.write(entry)


def generate_site_identity_tsv(scores):
    """Percent Site Identity TSV Generator

    From a string of identity values (Typically generated with identity_calculator).
    Generate a TSV of site locations & percent identity at site.

    :param scores: String of identity values for a MSA, usually from identity_calculator.
    """
    seq_len = len(scores)
    with open('site-identity-chart.tsv', 'w') as otpt:
        otpt.write('Site\t% Identity\n')
        for i in range (0, seq_len):
            site = i + 1
            score = scores[i]
            entry = '%d\t%f\n' % (site, score)
            otpt.write(entry)

def identity_calculator(alignment_file):
    """Percent Site Identity Calculator

    From a MSA (only sequence data - single line per sequence, no species names, sequences same length)
    Generate a list of conservation percentages for each site.

    :param alignment_file: MSA file, must contain only sequence data (no species names) and sequences same length
    :return: List of %identity scores for each site in MSA.
    """
    from operator import itemgetter

    #Establish global variables
    sequences = []
    scores = []
    sequence_count = 0

    #Build a list with sequences from alignment file
    with open(alignment_file, 'r') as inpt:
        reading = True
        while reading:
            seq = inpt.readline()
            if seq == '':
                reading = False
            elif seq == '\n':
                pass
            else:
                seq = seq.strip('\n')
                sequences.append(seq)
                sequence_count += 1

    #Calculates length of sequences
    sequence_length = len(sequences[0])

    #Calculates percent identity at each site in the sequences
    #Iterate through each site
    for i in range(0, sequence_length):
        #Establish a dictionary of the bases
        occurances = {'A': 0, 'T': 0, 'G': 0, 'C': 0}

        #Establish an empty list for holding value of each site
        comp_list = []

        #Add each sequence site to comparison list
        for sequence in sequences:
            comp_list.append(sequence[i])

        #Modify occurances dictioanry with number of times each base occurs
        for entry in comp_list:
            if entry in occurances:
                occurances[entry] += 1

        #Calculate the most frequent base
        most_freq_base = max(occurances.iteritems(), key=itemgetter(1))[0]

        #Calculate how conserved most frequent base is over alignment
        percent_identity = float(occurances[most_freq_base]) / sequence_count

        #Add score for site to scores list
        scores.append(percent_identity)

    #Return a list of site %identity scores
    return scores

generate_site_identity_tsv(identity_calculator(argv[1]))