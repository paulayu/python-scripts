#!/usr/bin/python
#This script is used to get masked region from a masked reference genome
#The mask_sta and mask_end are both 1-based, used for bcftools view -T filter.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",help="masked reference genome sequence in fasta format")
parser.add_argument("-o","--output",help="output bed file with masked regions used for bcftools view")
args = parser.parse_args()

mask = [[],[],[]]
name = []
seq = []
tempseq = ''

f= open(args.input,'r')
for line in f:
    if line.startswith('>'): 
        name.append(line.strip()[1:])
        seq.append(tempseq)
        tempseq = ''
    else: 
        tempseq += line.strip()
seq.append(tempseq)
seq.pop(0)

f.close()
print "Reading reference finished!"

for i,j in zip(name,seq):
    mark = 0
    for pos in range(len(j)):
        if j[pos] == 'N':
            if mark == 0:
                mask[0].append(i)
                mask[1].append(pos)
            mark += 1
        else:
            if mark != 0:
                mask[2].append(pos)
            mark = 0
    if mark != 0: mask[2].append(len(j)+1) #check if the end of the sequence is N. If so, add as a mask_end.

print "Masked region identification finished!"

output = open(args.output,'w')
for i in range(len(mask[0])):
    print >> output, mask[0][i]+'\t'+str(mask[1][i])+'\t'+str(mask[2][i])
