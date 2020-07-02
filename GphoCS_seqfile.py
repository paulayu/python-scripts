#!/usr/bin/python
#This script is used to generate the sequence file for G-phoCS
#Author: Yu He
import textwrap
from textwrap import wrap
def select_loci(x): #slicing fasta file of individual x
    """Slicing the autosomal fasta sequence of individual x to 1kb loci, and select the loci for analysis"""
    
    print 'Selecting loci based on',x,'...'
    chrom = []
    seq = []
    temp = ''
    with open(x+'.fa','r') as f:
        for line in f:
            if line.startswith('>'):
                chrom.append(line.strip()[1:])
                seq.append(temp)
                temp = ''
            else:
                temp += line.strip()
    seq.append(temp)
    seq.pop(0)
    #print 'Slicing individual',x,'...'
    selection=[]
    for i,j in zip(chrom,seq):
        if len(j)<1000000:
            continue #ignore scaffolds shorter than 1Mb
        temp = 50
        for index in range(len(j)/1000):
            loci_name = i+'_'+str(index)
            frag = j[index*1000:(index*1000+1000)]
            temp +=1
            if temp <= 50:
                continue
            elif frag.count('N') >100:
                continue
            else: 
                selection.append([i,loci_name,index*1000,index*1000+1000])
                temp = 0
    #print "Selecting loci finished!"
    #print "loci number:",len(selection)
    return selection

def slice_sample(x,loci):
    """Grep the loci for analysis from autosomal fasta sequence of individual x based on location from loci"""
    print 'Processing individual',x,'...'
    chrom = []
    seq = []
    temp = ''
    with open(x+'.fa','r') as f:
        for line in f:
            if line.startswith('>'):
                chrom.append(line.strip()[1:])
                seq.append(temp)
                temp = ''
            else:
                temp += line.strip()
    seq.append(temp)
    seq.pop(0)
    slicing = []
    for locus in loci:
        for i,j in zip(chrom,seq):
            if locus[0]==i:
                slicing.append([locus[1],x,j[locus[2]:locus[3]]])
            else: continue
    return slicing


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",help="sample list for generating sequence file")
parser.add_argument("-o","--output",help="prefix of the output sequence file")
args = parser.parse_args()

#reading sample list for slicing
sample_list = []
with open(str(args.input),'r') as f:
    temp = f.readlines()
    for i in temp:
        sample_list.append(i.strip()) 

#slicing each individual in the list one by one, then summarize the results in a large list
sample_num = len(sample_list)
print "Reading individual list finished!\nIndividual number:",sample_num

summary = []
loci_list = select_loci(sample_list[0])
loci_num = len(loci_list)

print "Select loci finished!\nLoci number:",loci_num

output1 = open(str(args.output)+'.gphocs.locus','w')
for i in loci_list:
    print >>output1,i[0],i[2],i[3]
output1.close()

for name in sample_list:
    individual = slice_sample(name,loci_list)
    summary += individual
print "Individual processing finished!"

#sort the summary list according to loci name
summary.sort()

#Start writing output file
print "Writing sequence file..."
output2 = open(str(args.output)+'.gphocs.seq','w') 
print >>output2,loci_num #write the headline of sequence file: number of loci in the file

loci_name = ''
#write each locus block separately
for record in summary:
    if loci_name != record[0]:
        loci_name = record[0]
        print >>output2,'\n'+loci_name+'\t'+str(sample_num)+'\t'+str(len(record[2])) #write the first line of each locus block
        print >>output2,record[1]+'\t'+record[2]
    else:
        print >>output2,record[1]+'\t'+record[2]
        
output2.close()
