import sys
from collections import defaultdict

inFile1 = open(sys.argv[1], 'r')  # input sam file
outFile = open(sys.argv[2], 'w')  # list of contig IDs - one per line

locusDict = defaultdict(list)  # default dict items to list so I don't have to define in-loop, just append value
for line in inFile1:
    if line.startswith('@'):
        pass
    else:
        spLine = line.strip().split('\t')
        if spLine[2].startswith('JAA') and int(spLine[1]) < 2048:  # only include reads that map (have to change JAA
            # prefix for other references) exclude supplementary alignments
            locusID = '/t'.join(spLine[2:4])
            locusDict[locusID].append(spLine[0])
        else:
            pass

pairCt = 0
for i in locusDict:
    if len(locusDict[i]) == 2:
        if locusDict[i][0].startswith('Ieng') and locusDict[i][1].startswith('Ival'):  # this only works because the SAM
            # file is ordered by read ID (i.e. all Ieng come before al Ival)
            pairCt += 1
            print(locusDict[i])
            outFile.write("{}\n{}\n".format(locusDict[i][0], locusDict[i][1]))

print(pairCt)


