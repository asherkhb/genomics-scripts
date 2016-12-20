__author__ = 'asherkhb'
# Newick to Species List
# v.1.0.0
#
# Given a tree in newick format, extract an ordered list of all taxa.
# Trees MUST end with a ';' and MUST NOT contain any preceding text.
#
# HINTS:
# - Trees may be imported from a file or directly on command-line.
# - If a file is specified, tree on first line will be processed.
# - If submitting from command line, it will probably be necessary to surround the tree string in quotes.
#
# Options
# -f : Import tree from file
# + USAGE: nwk_to_list -f <file_path>
#
# -t : Import tree as command-line argument
#    + USAGE: nwk_to_list.py -t <tree>
#
# -o : Output file. If omitted, species will be printed to terminal
#    + USAGE: nwk_to_list.py -f input_tree.nwk -o input_species.txt
#
# -h, --help
#

from argparse import ArgumentParser
from re import compile


def nwk_to_list(nwk_tree):
    species_list = []

    strip_branch_lengths = compile(':.*?,')
    clean_tail = compile(':.*?;')

    pruned = nwk_tree.rstrip().replace('(', ' ').replace(')', ' ')
    pruned = strip_branch_lengths.sub(' ', pruned)
    pruned = clean_tail.sub(' ', pruned)
    pruned = pruned.replace(',', ' ')

    tree_contents = pruned.split(' ')

    for entry in tree_contents:
        if entry != '' and entry != ';':
            species_list.append(entry)

    return species_list


def check_tree(nwk_tree):
    tree_string = nwk_tree.rstrip()
    tree_length = len(tree_string)

    if tree_string == '':
        print("Invalid Tree")
        exit()

    if tree_string[0] != '(':
        print("Invalid Tree")
        exit()

    if tree_string[tree_length - 1] != ';':
        print("Invalid Tree.")
        print("Trees MUST end with ';'")
        exit()


# Parse arguments.
parser = ArgumentParser(description='Given a tree in newick format, extract an ordered list of all taxa. ',
                        epilog='NOTE: Trees MUST end with ; and MUST NOT contain any preceding characters.')
parser.add_argument('-f', type=str, help='Import tree from file F')
parser.add_argument('-t', type=str, help='Import tree as argument T')
parser.add_argument('-o', type=str, help='Specify output file O')

args = parser.parse_args()


# Process arguments.
tree = ''
out_to_file = False
if args.f and args.t:
    print "Specify either a input tree file, or a tree argument, but not both."
    exit()
else:
    if args.f:
        with open(args.f, 'U') as inpt:
            tree = inpt.readline()
    elif args.t:
        tree = args.t
    else:
        print "Please specify an input tree"
        exit()

    if args.o:
        out_to_file = True

# Execute script.
check_tree(tree)
species = nwk_to_list(tree)
if out_to_file:
    with open(args.o, 'w') as otpt:
        for spp in species:
            otpt.write(spp + '\n')
    print("Your tree has been parsed. See %s for results." % args.o)
else:
    for spp in species:
        print(spp)