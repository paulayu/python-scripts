#!/usr/bin/python
#This script is used to generate region for masking from refGene, XenorefGene and CpgIsland of Felis_catus80 annotation
#The output is bed format for bedtools maskfasta, with 0-based chrstart and 1-based chrend

import os
import gzip
import warnings

mask1 = gzip.open("/bak/seqdata/genomes/Felis_catus_80_masked/UCSC_genome_annotation/refGene.txt.gz")
mask2 = gzip.open("/bak/seqdata/genomes/Felis_catus_80_masked/UCSC_genome_annotation/xenoRefGene.txt.gz")
mask3 = gzip.open("/bak/seqdata/genomes/Felis_catus_80_masked/UCSC_genome_annotation/cpgIslandExt.txt.gz")
refgene = mask1.readlines() + mask2.readlines()
cpg = mask3.readlines()
mask1.close()
mask2.close()
mask3.close()

chromosome = []
mask_sta = []
mask_end = []

for line in refgene:
    record = line.split('\t')
    temp_sta = record[9].split(',')
    temp_end = record[10].split(',')
    temp_sta.pop()
    temp_end.pop()
    for i in range(len(temp_sta)):
        chromosome.append(record[2])
        if (int(temp_sta[i])-1000 < 0):
            temp_sta[i] = '0'
        else: temp_sta[i] = str(int(temp_sta[i])-1000)
        mask_sta.append(temp_sta[i])
        mask_end.append(str(int(temp_end[i])+1000))
print "Refgene reading finished"

for line in cpg:
    record = line.split('\t')
    chromosome.append(record[1])
    mask_sta.append(record[2])
    mask_end.append(record[3])
print "cpg reading finished"

output = open('mask_region.bed','w')
for i in range(len(chromosome)):
    print >> output, chromosome[i]+'\t'+mask_sta[i]+'\t'+mask_end[i]
#print len(chromosome)