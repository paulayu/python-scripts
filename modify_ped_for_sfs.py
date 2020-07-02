#!/opt/bin/python
#This script is used to modify ped file for sfs calculation using convert_ped_to_unfolded_sfs.pl by Miao
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",help="input file in map format")
parser.add_argument("-o","--output",help="output file in map format")
args = parser.parse_args()

with open(args.input,'r') as f:
    pedin = f.readlines()

output = open(args.output,'w')

for indv in pedin:
    indv = indv.strip().split('\t')
    pedout = []
    for i in range(6):
        pedout.append(indv[i])
    for i in range(6,len(indv),2):
        geno = indv[i]+' '+indv[i+1]
        pedout.append(geno)
    print >>output, '\t'.join(pedout)

