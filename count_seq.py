# CountSeq FASTA Analyzer
# A slow script useful for seeing what is inside of multiFASTA files.

from sys import argv

with open(argv[1], 'U') as ipt:
    ref_c = ''
    ref_l = ''
    count = 0
    pieces = {}
    for line in ipt:
        line = line.strip()
        if len(line) < 1:
            print("Warning: Empty Line Encountered")
            pass
        elif line[0] == '#':
            print("Warning: Comment Line Encountered")
            pass
        else:
            if line[0] == '>':
                ref_c = line
                if ref_c != ref_l:
                    print ref_l, count, pieces
                    ref_l = ref_c
                    count = 0
                    pieces = {}
            else:
                count += len(line)
                for i in range(len(line)):
                    try:
                        pieces[line[i]] += 1
                    except:
                        pieces[line[i]] = 1
