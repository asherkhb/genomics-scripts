__author__ = 'asherkhb'

import os
import shutil


def generate_summary(final_dictionary):
    """Generate a full summary report.

    Using the final 'categories' dictionary, generates a full summary report.
    Report contains each category and number of associated files and a list of each file, plus...
    Total number of entries, number of unique species, and a species list for each file

    :param final_dictionary: Final 'categories' dictionary
    """
    otpt = open('multifind_summary.txt', 'w')
    for cat in final_dictionary:
        category_name = cat[0] + ': ' + str(len(cat[1])) + '\n'
        otpt.write(category_name)
        for entry in cat[1]:
            otpt.write('\t' + str(entry[0]) + '\n')
            otpt.write('\t\tTotal Entries: %s\n' % str(entry[1]))
            otpt.write('\t\tUnique Species: %s\n' % str(entry[2]))
            count = 0
            for sp in entry[3]:
                if count < entry[2]-1:
                    if count == 0:
                        otpt.write('\t\tSpecies: ' + sp + ', ')
                    else:
                        otpt.write(sp + ', ')
                else:
                    otpt.write(sp + '\n')
                count += 1
    otpt.close()


def generate_simple_report(final_dictionary):
    """Generate a simple summary report.

    Using final categories dictionary, generates a simple summary report (category and number of associated files)

    :param final_dictionary: Final 'categories' dictionary
    """
    otpt = open('multifind_simple_summary.txt', 'w')
    for cat in final_dictionary:
        category_name = cat[0]
        category_cont = str(len(cat[1]))
        otpt.write(category_name + ' ')
        otpt.write(category_cont + '\n')
    otpt.close()


#Establish FASTA-containing directory, build list of contents.
directory = './sample_fastas/'  # Use trailing forward slash.
file_list = os.listdir(directory)

#Generate Directories
categories = [['species_specific', []],       # 1 Unique Taxa: categoryID: 0
              ['poorly_conserved', []],       # 2-4 Unique Taxa: categoryID: 1
              ['moderately_conserved', []],   # 4 - (total-1) taxa: categoryID: 2
              ['completely_conserved', []]]   # All unique taxa: categoryID: 3


#Create unique folder for each category.
for category in categories:
    if not os.path.exists(category[0]):
        os.makedirs(category[0])

#Process files.
for fasta_file in file_list:
    #Establish entry counter.
    entries = 0
    #Establish list of species.
    species = []
    #Open the file for processing.
    file_path = "%s%s" % (directory, fasta_file)
    with open(file_path, 'r') as current_file:
        reading = True
        while reading:
            line = current_file.readline()
            if line == '':
                reading = False
            else:
                #Identify header lines.
                if line[0] == '>':
                    #Increase entry counter by one.
                    entries += 1
                    #Obtain species from header.
                    line_components = line.split('_')
                    spp = line_components[0].strip('>')
                    #Add species to species list (if not already present).
                    if not spp in species:
                        species.append(spp)
        #Establish total number of species.
        species_number = len(species)
        #Generate an entry (for final categories dictionary) for the file.
        file_entry = [file, entries, species_number, species]

        #Classify each FASTA by category, move file into appropriate category, and append category dictionary.
        #To change from copy to move, simply change the next 4 "copy2" to "move"
        #Species Specific.
        if species_number == 1:
            categories[0][1].append(file_entry)
            shutil.copy2(file_path, './species_specific')
        #Poorly Conserved.
        elif species_number < 4:
            categories[1][1].append(file_entry)
            shutil.copy2(file_path, './poorly_conserved')
        #Moderately Conserved.
        elif species_number < entries:
            categories[2][1].append(file_entry)
            shutil.copy2(file_path, './moderately_conserved')
        #Completely Conserved.
        elif species_number == entries:
            categories[3][1].append(file_entry)
            shutil.copy2(file_path, './completely_conserved')

#Generate a complex report.
generate_summary(categories)

#Generate a simple report.
generate_simple_report(categories)