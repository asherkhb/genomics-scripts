"""
	BaseCounter Plus v. 1.2.0
	
		Input (at prompt) a multi-fasta file:
			Output a file (output.txt) with the following information:
				Total File Individual Base Count
				Total Bases, including special charactars
				Total Amino Acids G, C, A and T
				Total File Percent GC
				Total File Percent AT
				List of Included Features with Total Base Count and PercentGC/PercentAT Statistics
		
		Future: 
			Change input prompt to command line arguments for input and output file
			Include additional statistics
		
		Test Data Included: multifasta file of 37 various features
	
	By asherkhb
	Last Update: 10/2/14
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

def FastaSplit(input):
	dictionary = {}
	index = ''
	with open(input, 'r') as in_file:
		for line in in_file:
			if line[0] == '>':
				dictionary[line.rstrip('\n')] = []
				index = line.rstrip('\n')
			elif line[0] != '>':
				dictionary[index].append(line.rstrip('\n'))
	return dictionary

def FeatSplit(d):
	for key,value in d.items():
		feature = key
		bcount = {}
		for i in range(len(value)):
			s = value[i]
			for x in range(len(s)):
				if s[x] not in bcount:
					bcount[s[x]] = 0
				bcount[s[x]] += 1
		totalNT = bcount['G'] + bcount['C'] + bcount['A'] + bcount['T']
		gc = PercentPair(bcount['G'], bcount['C'], totalNT)
		at = PercentPair(bcount['A'], bcount['T'], totalNT)
		out_file.write("%s: \n" % (feature))
		out_file.write("  Total Nucleotides: %s\n" % (totalNT))
		out_file.write("  Percent GC:"),
		WritePercent(gc)
		out_file.write("  Percent AT:"),
		WritePercent(at)
		out_file.write("\n")

"""Get Input File"""
inpt = raw_input("Enter MultiFasta File Name: ")

"""Data Processing"""		

#Pull base_count dictionary and fast_list list from BaseLibBuilder
base_count,fasta_list,_ = BaseLibBuilder(inpt)

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
out_file.write("~~~~~Total Base Library:~~~~~\n\n")
out_file.write("Total Base Count: %s\n" % (str(lib_total)))
out_file.write("Total Nucleotide Count: %s\n" % (str(total)))
for key,value in base_count.items():
	out_file.write("  %s: %s\n" % (key,str(value)))

out_file.write("\n")

#Write Total Library Composition Statistics
out_file.write("Total Composition Statistics:\n")
out_file.write("  %GC: ")
WritePercent(gc)
out_file.write("  %AT: ")
WritePercent(at)

out_file.write("\n")
out_file.write("~~~~~Included Features~~~~~\n\n")

#Write Feature List w/ Statistics
d = FastaSplit(inpt)
FeatSplit(d)

#Close Output File
out_file.close()

#Print Confirmation to Console
print("...\n'%s' Analyzed! See 'output.txt' for results..." % (inpt))