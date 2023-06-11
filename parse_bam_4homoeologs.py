import sys
import pysam

inFile1 = pysam.view(sys.argv[1], "-h")
samList = inFile1.split("\n")
outFile1 = open(sys.argv[2]+".eng.sam", "w")  # output BAM file for engelmannii reads
outFile2 = open(sys.argv[2]+".val.sam", "w")  # output BAM file for valida reads
outFile3 = open(sys.argv[2]+".eng.list", "w")
outFile4 = open(sys.argv[2]+".val.list", "w")

primAlign = 0
filtAlign = 0
engCt = 0
valCt = 0

for i in samList:
    if i.startswith("@"):
        outFile1.write(i+"\n")
        outFile2.write(i+"\n")
    spLine = i.strip().split()
    if len(spLine) > 5:
        flagSet = set(["99", "147", "83", "163"])
        if spLine[1] in flagSet:  # You can add/change numbers here to pull sequences according to particular sam flags
            AS = int(spLine[14].split(":")[2])
            XS = int(spLine[15].split(":")[2])
            alDiff = AS-XS
            primAlign += 1
            if XS == 0 or alDiff > 10:  # This number can be changed to filter for differential alignment scores
                # print(i)
                filtAlign += 1
                if spLine[2].startswith('Ieng'):
                    outFile1.write(i+"\n")
                    outFile3.write(spLine[0]+"\n")
                    engCt += 1
                elif spLine[2].startswith('Ival'):
                    outFile2.write(i+"\n")
                    outFile4.write(spLine[0]+"\n")
                    valCt += 1
        elif spLine[1] == "73":  # You can add/change numbers here to pull sequences according to particular sam flags
            AS = int(spLine[13].split(":")[2])
            XS = int(spLine[14].split(":")[2])
            alDiff = AS-XS
            primAlign += 1
            if XS == 0 or alDiff > 10:  # This number can be changed to filter for differential alignment scores
                # print(i)
                filtAlign += 1
                if spLine[2].startswith('Ieng'):
                    outFile1.write(i+"\n")
                    outFile3.write(spLine[0]+"\n")
                    engCt += 1
                elif spLine[2].startswith('Ival'):
                    outFile2.write(i+"\n")
                    outFile4.write(spLine[0]+"\n")
                    valCt += 1
        else:
            pass
print("{} out of {} alignments printed to sam files".format(filtAlign, primAlign))
print("{} written to: {}\n{} written to: {}".format(engCt, sys.argv[2]+".eng.sam", valCt,sys.argv[2]+".val.sam"))