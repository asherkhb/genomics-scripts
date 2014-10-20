#Script designed for implementation in RAxML pipeline.
#Recieves an input file, outputs the same file but with name "output"
#Use syntax input-output.py -i <inputfile>
#Ex. 
#in-out.py -i input.ext 
#--> returns file output.ext

import sys, getopt, os

def main(argv):
	inputfile = ''
	outputfile = ''
	
	try:
		opts, args = getopt.getopt(argv, 'hi:')
	except getopt.GetoptError:
		print "Incorrect syntax: Use '-h' for help."
		with open('in-out_error-log.txt', 'w') as error:
			error.write("Syntax Error\n")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('Use Syntax: in-out.py -i <inputfile>')
			sys.exit()
		elif opt == '-i':
			inputfile = arg
			_, extension = os.path.splitext(arg)
			outputfile = 'output%s' % (extension)

	with open(inputfile, 'r') as inpt:
		with open(outputfile, 'w') as otpt:
			otpt.write(inpt.read())

if __name__ == '__main__':
	main(sys.argv[1:])
