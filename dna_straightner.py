"""
	DNA Sequence Straightener, v. 1.0.0
	-->Asks user for "input_file" containing DNA sequence. 
	-->Converts to a continous string and ensures all capital letters. 
	-->Exports new sequence as "fileName_rev.txt"
	-->I personally use this script to convert sequence files for use with CoGeBlast.
	By asherkhb
	Last Update: 10/9/14
"""

inpt = raw_input("Input File: ")
outpt = "%s_rev.txt" % (inpt)

with open(inpt, 'r') as sequence:
	s = sequence.read().strip('\n').replace(" ", "").upper()

with open(outpt,'w') as newseq:
	newseq.write(s)
