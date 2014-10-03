"""
	MultiFasta Splitter v. 1.0.0
	Short script to split multi-FASTA files into separate FASTA files. Program will ask for input file name, file and script should be in same folder.
	Distributed with test data (test.txt) multi-fasta file for 7 neuroreceptors in Chicken
	By asherkhb
	Last Update: 8/2/14
"""


def FastaSplit(input):
	dictionary = {}
	index = ''
	with open(input, 'r') as in_file:
		for line in in_file:
			if line[0] == '>':
				dictionary[line.rstrip('\n')] = []
				index = line.rstrip('\n')
			elif line[0] != '>':
				dictionary[index].append(line)
	return dictionary

def WriteNewFastas(d):
	counter = 0
	for key,value in d.items():
		feature = key
		bcount = {}
		filename = '%s.txt' % (key.strip('>'))
		with open(filename, 'w') as new_file:
			new_file.write("%s\n" % (feature))
			for item in value:
				new_file.write(item)
		counter += 1
	return counter

inpt = raw_input("Enter Multi-Fasta File Name: ")
d = FastaSplit(inpt)
count = WriteNewFastas(d)
print("...\n%s split into %s files" % (inpt, str(count)))


