#!/usr/bin/python

# This script is used to merge pseudo-haploid genotype calls from the same individual. 
# If there is only one non-missing call, the output is the non-missing genotype. 
# If there are more than one non-missing calls, the output is randomly selected.
# Input: eigenstrat files with libraries to be merged, and an individual list file with the individual names to be output
# Output: eigenstrat files of merged individuals, with individual names as given in individual list file (not the ind file of eigenstrat input!)
# Author: He Yu

import sys
import argparse
from collections import Counter
import random

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--geno",help="prefix of input files in eigenstrat format")
parser.add_argument("--ind",help="individual name list of input data, should have the same number of lines with input eigenstrat individual file")
parser.add_argument("-o","--output",help="prefix of output files in eigenstrat format")
parser.add_argument("-d","--dataset",help="""the genotypes included in output dataset. Select from all, unique or merged.\nall: all the input genotypes plus merged genotypes\nunique: one genotype for each individual, for individuals with more than one genotypes only keep the merged genotypes\nmerge: only merged genotypes""")
args = parser.parse_args()

if len(sys.argv)==1: 
    parser.print_help()
    sys.exit()

with open(args.geno+'.geno','r') as f1:
    in_geno = f1.readlines()
with open(args.geno+'.ind','r') as f2:
    in_ind = f2.readlines()
with open(args.ind,'r') as f3:
    individual = f3.readlines()

if len(in_ind) != len(individual): sys.exit("Error: individual list not matching with input dataset!")

# Define functions for different types of output
def write_all_output(output):
    o1 = open(output+'.ind','w')
    index_all = []
    for i in in_ind: print >>o1, i.strip()
    for ind in dup:
        index = [i for i,x in enumerate(individual) if x==ind]
        index_all.append(index)
        sexs = [in_ind[j].split()[1] for j in index]
        if "F" in sexs and "M" in sexs: merge_sex = "U"
        elif "F" in sexs: merge_sex = "F"
        elif "M" in sexs: merge_sex = "M"
        else: merge_sex = "U"
        print >>o1, ind.strip()+"\t"+merge_sex+"\t"+"merge_genotype"
    o1.close()
    
    o2 = open(output+'.geno','w')
    for site in in_geno:
        merge_call = site.strip()
        for i,ind in enumerate(dup):
            index = index_all[i]
            calls = [site[j] for j in index]
            if "0" in calls and "2" in calls: merge_call += random.choice("02")
            elif "0" in calls: merge_call += "0"
            elif "2" in calls: merge_call += "2"
            else: merge_call += "9"
        print >>o2, merge_call
    o2.close()
    return "1"

def write_unique_output(output):
    o1 = open(output+'.ind','w')
    index_all = []
    for i,ind in enumerate(individual):
        if ind in dup: continue
        else: 
            print >>o1, in_ind[i].strip()
    for ind in dup:
        index = [i for i,x in enumerate(individual) if x==ind]
        index_all.append(index)
        sexs = [in_ind[j].split()[1] for j in index]
        if "F" in sexs and "M" in sexs: merge_sex = "U"
        elif "F" in sexs: merge_sex = "F"
        elif "M" in sexs: merge_sex = "M"
        else: merge_sex = "U"
        print >>o1, ind.strip()+"\t"+merge_sex+"\t"+"merge_genotype"
    o1.close()
    
    o2 = open(output+'.geno','w')
    for site in in_geno:
        merge_call = ""
        for i,ind in enumerate(individual):
            if ind in dup: continue
            else: merge_call += site[i]
        for i,ind in enumerate(dup):
            index = index_all[i]
            calls = [site[j] for j in index]
            if "0" in calls and "2" in calls: merge_call += random.choice("02")
            elif "0" in calls: merge_call += "0"
            elif "2" in calls: merge_call += "2"
            else: merge_call += "9"
        print >>o2, merge_call
    o2.close()
    return "1"

def write_merge_output(output):
    o1 = open(output+'.ind','w')
    index_all = []
    for ind in dup:
        index = [i for i,x in enumerate(individual) if x==ind]
        index_all.append(index)
        sexs = [in_ind[j].split()[1] for j in index]
        if "F" in sexs and "M" in sexs: merge_sex = "U"
        elif "F" in sexs: merge_sex = "F"
        elif "M" in sexs: merge_sex = "M"
        else: merge_sex = "U"
        print >>o1, ind.strip()+"\t"+merge_sex+"\t"+"merge_genotype"
    o1.close()
    
    o2 = open(output+'.geno','w')
    for site in in_geno:
        merge_call = ""
        for i,ind in enumerate(dup):
            index = index_all[i]
            calls = [site[j] for j in index]
            if "0" in calls and "2" in calls: merge_call += random.choice("02")
            elif "0" in calls: merge_call += "0"
            elif "2" in calls: merge_call += "2"
            else: merge_call += "9"
        print >>o2, merge_call
    o2.close()
    return "1"

# The main code start
c = Counter(individual)
dup = []
for i in c.keys():
    if c[i] >1: dup.append(i) #find individuals with more than one genotype calls
dup.sort()

print "Input reading finished!"
print "Number of input genotypes:",len(in_ind)
print "Number of individuals to be combined", len(dup)

if args.dataset == "all":
    print "Output all the input genotypes and merged genotypes, n =",len(in_ind)+len(dup)
    write_all_output(args.output)
elif args.dataset == "unique": 
    print "Output one genotype for each individual, n =",len(c.keys())
    write_unique_output(args.output)
elif args.dataset == "merge": 
    print "Output only the merged genotypes, n =",len(dup)
    write_merge_output(args.output)
else: sys.exit("Error: please specify the type of output dataset!")

print "Writing output files finished!"
