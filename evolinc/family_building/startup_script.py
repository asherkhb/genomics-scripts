__author__ = 'asherkhb'

from subprocess import call
import sys

#Ensure correct number of arguments are entered
if len(sys.argv) != 3:
    print("Incorrect usage syntax: Must specify input list.\nUse 'startup_script.py <input>'")
    exit()

#Assign input file from first command argument.
inputfile = sys.argv[1]

with open(inputfile, 'r') as inpt:
    reading = True
    while reading:
        line = inpt.readline()
        if line =='':
            reading = False
        elif line == '\n':
            pass
        else:
            line_split = line.split('\t')
            subject = line_split[0]
            lincRNA = line_split[1]
            query_spp = line_split[2]
            subject_spp = line_split[3]
            query = "sh Family_Building.sh -g %s -s %s -q %s -f %s" % (subject, lincRNA, query_spp, subject_spp)
            call(query, shell=True)
