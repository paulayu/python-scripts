#!/usr/bin/python
#This script is used to calculate p-distance between individuals
#Author: Yu He
#Input: eigenstrate format genotype data, no missing data taken into calculation
#The individual file must be in the same directory with genotype file
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",help="input file in eigenstratgeno format")
parser.add_argument("-o","--output",help="the prefix of output matrix and snp number files")
args = parser.parse_args()

input1 = open(args.input,'r')
#input2 = open(".".join(args.input.split(".")[:-1])+".ind",'r')
genotype = input1.readlines()
#indiv = input2.readlines()
input1.close()
#input2.close()
distance = []
snp = []
print "Input reading finished!"

# Set distance matrix to 0
indiv_num = len(genotype[0].strip())
print "Individual number:",indiv_num

for i in range(indiv_num):
    tmp1 = []
    tmp2 = []
    for j in range(indiv_num):
        tmp1.append(0)
        tmp2.append(0)
    distance.append(tmp1)
    snp.append(tmp2)

#distance calculation
for line in genotype:
    for i in range(indiv_num):
        for j in range(i,indiv_num):
            if line[i] == "9" or line[j] == "9": continue
            else:
                distance[i][j] += abs(int(line[i])-int(line[j]))/2
                snp[i][j] += 1
        #print i,distance[i]
print "Distance calculation finished!"
print "Total SNP number:",len(genotype)

#distance matrix and snp number print
output_matrix = open(args.output+".matrix",'w')
output_snp = open(args.output+".snp",'w')

for i in range(indiv_num):
    for j in range(indiv_num):
        print >>output_snp,snp[i][j],
        if snp[i][j] == 0: print >>output_matrix,"NA",
        else: print >>output_matrix,float(distance[i][j])/snp[i][j],
    print >>output_matrix,''
    print >>output_snp,''

print "Writing output finished!"


output_snp = open(args.output+".snp",'w')
