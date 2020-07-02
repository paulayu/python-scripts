#!/usr/bin/python
#This script is used to summarize basic statistics of a reference genome in fasta format
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",help="input reference file in fasta format")
args = parser.parse_args()

print "Reading input reference file..."

chrom = []
seq = []
tempseq = ''
with open(args.input,'r') as f:
    for line in f:
        if line.startswith('>'):
            chrom.append(line.strip()[1:])
            seq.append(tempseq)
	    tempseq = ''
        else:
            tempseq += line.strip()
    seq.append(tempseq)
    seq.pop(0)
f.close()

print "Writing output..."

output = open(args.input+'.summary','w')
print >>output, "chrom\tlength\t#A\t#T\t#C\t#G\t#N\t"

sum_A = 0
sum_T = 0
sum_C = 0
sum_G = 0
sum_N = 0
num_A = 0
num_T = 0
num_C = 0
num_G = 0
num_N = 0
length = 0
total_len = 0
for i,j in zip(chrom,seq):
    length = len(j)
    num_A = j.count('A') + j.count('a')
    num_T = j.count('T') + j.count('t')
    num_C = j.count('C') + j.count('c')
    num_G = j.count('G') + j.count('g')
    num_N = j.count('N')
    sum_A += num_A
    sum_T += num_T
    sum_C += num_C
    sum_G += num_G
    sum_N += num_N
    total_len += length
    print >>output, i+'\t'+str(length)+'\t'+str(num_A)+'\t'+str(num_T)+'\t'+str(num_C)+'\t'+str(num_G)+'\t'+str(num_N)

print >>output, "Total\t"+str(total_len)+'\t'+str(sum_A)+'\t'+str(sum_T)+'\t'+str(sum_C)+'\t'+str(sum_G)+'\t'+str(sum_N)


