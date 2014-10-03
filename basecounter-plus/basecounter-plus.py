"""
	BaseCounter Plus v. 1.1.0
	Given a multi-fasta file: 
		Output a file (output.txt) with the following information:
			Total File Individual Base Count
			Total Bases, including special charactars
			Total Amino Acids G, C, A and T
			Total File Percent GC
			Total File Percent AT
			List of Included Features
	Future: 
		Accept command line arguments for input and output file
		Provide statistics on each individual feature

		By asherkhb
		Last Update: 8/2/14
"""

"""Define Functions"""

def BaseLibBuilder(filename):
	#Assign Variables for Return
	fasta_list = []
	base_count = {}
	lines = []
	
	#Open input file, build a list of lines
	with open(filename, 'r') as in_file:
		for line in in_file:
			lines.append(line.rstrip('\n'))

	#Loop through lines, eliminating meta data and counting bases
	for l in range(len(lines)):
		s = lines[l]
		if s[0] != '>':
			for i in range(len(s)):
				if s[i] not in base_count:
					base_count[s[i]] = 0
				base_count[s[i]] += 1
		elif s[0] == '>':
			if s not in fasta_list:
				fasta_list.append(s)

	#Check for file closure, Close if open
	if in_file.closed == False:
		in_file.close()
	return base_count, fasta_list, lines

def FastSplit(filename):
	feat_dict = {}
	index = ''
	with open(input, 'r') as in_file:
		for line in in_file:
			if line[0] == '>':
				feat_dict[line.rstrip('\n')] = []
				index = line.rstrip('\n')
			elif line[0] != '>':
				feat_dict[index].append(line.rstrip('\n'))
	return feat_dict

def LibSum(library):
	count = 0
	for key in library:
		count += library[key]
	return count

def TotalBase(g,c,a,t):
	return g + c + a + t

def PercentPair(x,y,total):
	return ((float(x) + y) / total)*100

def PercentOther(input):
	pass

def WritePercent(i):
	i = "%0.2f" % (i)
	s = str(i) + "%\n"
	out_file.write(s)

"""Data Processing"""		

#Pull base_count dictionary and fast_list list from BaseLibBuilder
base_count,fasta_list,_ = BaseLibBuilder('sample_fasta.txt')

#Calculate Library Total
lib_total = LibSum(base_count)

#Calculate total G,C,A,T Bases
total = TotalBase(base_count['G'], base_count['C'], base_count['A'], base_count['T'])

#Calculate %GC
gc = PercentPair(base_count['G'], base_count['C'], total)

#Calculate %AT
at = PercentPair(base_count['A'], base_count['T'], total)

#Total Features
feat_count = str(len(fasta_list))

"""Data Output"""

#Open output.txt for writing
out_file = open('output.txt', 'w')

#Print Total Base Library
out_file.write("Total Base Library:\n")
out_file.write("    Total Base Count: %s\n" % (str(lib_total)))
out_file.write("    Total Amino Acid Count: %s\n" % (str(total)))
for key,value in base_count.items():
	out_file.write("    %s: %s\n" % (key,str(value)))

out_file.write("\n")

out_file.write("Total Library Composition Statistics:\n  *Calculated on total AA content*\n")
out_file.write("    %GC: ")
WritePercent(gc)
out_file.write("    %AT: ")
WritePercent(at)

out_file.write("\n")

out_file.write("Features: (%s)\n" % (feat_count))
for i in range(len(fasta_list)):
	out_file.write("    %s\n" % (fasta_list[i]))

out_file.close()