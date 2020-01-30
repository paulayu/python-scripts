#!/usr/bin/python
#change eigenstrat files into phylip sequence file with only variable sites
#Author: Yu He
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",help="prefix of input sequence file in eigenstratgeno format")
parser.add_argument("-o","--output",help="output sequence file in phylip format")
args = parser.parse_args()

with open(args.input+'.eigenstratgeno','r') as f1:
    data = f1.readlines()
with open(args.input+'.snp','r') as f2:
    snp = f2.readlines()
with open(args.input+'.ind','r') as f3:
    ind = f3.readlines()
print "Input reading finished!"
output = open(args.output,'w')
    
ind_num = len(ind)
snp_num = len(snp)
print "Individual number:",ind_num
print "sequence length:",snp_num
print >>output, ind_num,snp_num

iupac = dict([('AT','W'),('TA','W'),('AG','R'),('GA','R'),('AC','M'),('CA','M'),('TG','K'),('GT','K'),('TC','Y'),('CT','Y'),('GC','S'),('CG','S')])

seq =[]
name = []
for i in ind:
    seq.append([])
    name.append(i.split()[0])
    
for i in range(snp_num):
    temp_snp = snp[i].split()
    temp_data = data[i]
    #if i%500000==0: print i,"snp transformation finished."
    for j in range(ind_num):
        if temp_data[j]=='0': seq[j].append(temp_snp[4])
        elif temp_data[j]=='2': seq[j].append(temp_snp[5])
        elif temp_data[j]=='1': seq[j].append(iupac[temp_snp[4]+temp_snp[5]])
        else: seq[j] += 'N'

for i in range(ind_num):
    print >>output, name[i],'\t',''.join(seq[i])
