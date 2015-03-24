__author__ = 'asherkhb'

import sys
import os

#Ensure correct number of arguments are entered
if len(sys.argv) != 3:
    print("Incorrect usage syntax: Must specify input and output files.\nUse 'merge_close_hits.py <input> <output>'")
    exit()

#Establish Global Variables
#DONT CHANGE THESE
input_file = sys.argv[1]
output_file = sys.argv[2]
line_memory = ''
line_memory_array = ["null"]
names = {}

#***Combine Multiple Hits***
#Open input file and temporary output file
with open("scriptpy-temp-out.txt", 'w') as otpt:
    with open(input_file, 'r') as inpt:
        #Establish a reading loop
        reading = True
        while reading:
            line = inpt.readline()
            #End reading loop at end of document
            if line == '':
                reading = False
            #Skip empty lines
            elif line == '\n':
                pass
            #Process data-containing lines
            else:
                #Split line (of TSVs) into an array
                line_array = line.split('\t')
                #Remove pesky quotes from last column. Comment this out if you want to leave them.
                #line_array[8] = line_array[8].replace('"', '')
                #If two hits are from the same ID, process.
                if line_array[0] == line_memory_array[0]:
                    #Establish length of HSP
                    start = int(line_memory_array[3])
                    stop = int(line_array[4])
                    hsp_length = stop - start
                    #Combine HSPs (if appropriate)
                    if int(line_array[9]) + 500 >= hsp_length > 0:
                        line_memory_array[4] = line_array[4]
                    #If not appropriate to combine, write out line to temporary output file.
                    else:
                        line_memory_array.remove(line_memory_array[9])
                        printline = "\t".join(line_memory_array)
                        printline += "\n"
                        otpt.write(printline)
                        #Reset line memory array to current line array
                        line_memory_array = line_array
                #If two hits are not from same ID, write out line to temporary output file.
                else:
                    if line_memory_array[0] != 'null':
                        line_memory_array.remove(line_memory_array[9])
                        printline = "\t".join(line_memory_array)
                        printline += "\n"
                        otpt.write(printline)
                    #Reset line memory array to current line array
                    line_memory_array = line_array

#***Rename Duplicates***
#Open input and output files
with open('scriptpy-temp-out.txt', 'r') as inpt:
    with open(output_file, 'w') as otpt:
        #Establish a reading loop
        reading = True
        while reading:
            line = inpt.readline()
            #End reading loop when end of document is reached
            if line == "":
                reading = False
            #Skip lines without content
            elif line == "\n":
                pass
            #Process data-containing lines
            else:
                #Split line (of TSVs) into an array
                line_array = line.split("\t")
                #Check to see if the ID already exists in dictionary
                #If so, increase count and change ID to represent count. Write out line.
                if line_array[0] in names:
                    names[line_array[0]] += 1
                    rep = names[line_array[0]]
                    old_name = line_array[0]
                    new_name = "%s_%i" % (line_array[0], rep)
                    line_array[0] = new_name
                    line_array[8] = line_array[8].replace(old_name, new_name)
                    new_line = "\t".join(line_array)
                    otpt.write(new_line)
                #If ID does not exist in dictionary, add and set count to 1. Write out line
                else:
                    names[line_array[0]] = 1
                    otpt.write(line)

#Remove the temporary output file
os.remove("scriptpy-temp-out.txt")

#Generate a report of IDs and and number of HSPs
with open('sample-instance-report.txt', 'w') as instance_report:
    for key in names:
        instance = '%i\t%s\n' % (names[key], key)
        instance_report.write(instance)