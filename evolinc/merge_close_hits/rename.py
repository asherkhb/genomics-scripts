__author__ = 'asherkhb'

#Define empty dictionary that will hold names & instances
names = {}

#Open input and output files
with open('new_file.txt', 'r') as inpt:
    with open('renamed.txt', 'w') as otpt:
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
                #Check to see if the ID already exists in dictionary, if so, change ID to represent count. Increase count. Write out line.
                if line_array[0] in names:
                    names[line_array[0]] += 1
                    rep = names[line_array[0]]
                    new_name = "%s_%i" % (line_array[0], rep)
                    line_array[0] = new_name
                    new_line = "\t".join(line_array)
                    otpt.write(new_line)
                #If ID does not exist in dictionary, add and set count to 1, then write out line
                else:
                    names[line_array[0]] = 1
                    otpt.write(line)

with open('sample-instance-report.txt', 'w') as instance_report:
    for key in names:
        instance = '%i\t%s\n' % (names[key], key)
        instance_report.write(instance)