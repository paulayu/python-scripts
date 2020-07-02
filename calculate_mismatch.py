#!/usr/bin/python
#This script is used to infer the relateness between individuals by calculating the mismatch rates
#Author: Yu He
#Input: eigenstrate format genotype data in autosomes, no missing data taken into calculation
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--geno",help="input genotype file in eigenstrat format")
parser.add_argument("--ind",help="input individual file in eigenstrat format")
parser.add_argument("--output",help="the output mismatch summary")
args = parser.parse_args()

input1 = open(args.geno,'r')
input2 = open(args.ind,'r')
genotype = input1.readlines()
indiv = input2.readlines()
input1.close()
input2.close()
mismatch =[]
count = []
print "Input reading finished!"
# Set matrix to 0
indiv_num = len(indiv)
for i in range(indiv_num):
    tmp = []
    for j in range(indiv_num):
        tmp.append(0)
    mismatch.append(tmp)
for i in range(indiv_num):
    tmp = []
    for j in range(indiv_num):
        tmp.append(0)
    count.append(tmp)

#distance calculation

for line in genotype:
    for i in range(indiv_num):
        for j in range(i+1,indiv_num):
            if line[i]=='9' or line[j]=='9': continue
            else:
                count[i][j] += 1
                mismatch[i][j] += abs(int(line[i])-int(line[j]))/2

print "Mismatch calculation finished!"

#print results

output = open(args.output,'w')
print >>output,"ID1 ID2 nSNP nMismatch pMismatch"
for i in range(indiv_num):
    for j in range(i+1,indiv_num):
        ind1=indiv[i].split('\t')[0]
        ind2=indiv[j].split('\t')[0]
        print >>output,ind1,ind2,count[i][j],mismatch[i][j],float(mismatch[i][j])/count[i][j]
