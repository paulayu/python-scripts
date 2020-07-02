#!/opt/bin/python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ac",help="allelecount file generated from bcftools query")
parser.add_argument("--fst",help="windowed fst file generated from vcftools")
parser.add_argument("-n","--number",help="number of individuals involved in analysis")
parser.add_argument("-o","--output",help="prefix of the output files")
args = parser.parse_args()

f1 = open(args.ac,'r')
f2 = open(args.fst,'r')
ac = f1.readlines()
f2.readline() #remove the header of fst file
fst = f2.readlines()
indv_num = int(args.number)
snp = []
print "snp number:",len(ac),"window number:",len(fst),"individual number:",indv_num

for i in range(len(fst)):
    snp.append([])

index = 0
for i,k in enumerate(fst):
    interval = k.split('\t')
    for j in range(index,len(ac)):
        temp_ac = ac[j].split('\t')
        if temp_ac[0] == interval[0]: #match the chromosome
            if (int(temp_ac[1])>=int(interval[1])) and (int(temp_ac[1])<=int(interval[2])):
                snp[i].append(int(temp_ac[2]))
            elif int(temp_ac[1])<int(interval[1]): index=j
            elif int(temp_ac[1])>int(interval[2]): break
print "slice snps finished!"

output1 = open(args.output+".allelecount",'w')
output2 = open(args.output+".Fst.Hp",'w')        

for i,j in zip(snp,fst):
    major = 0
    window = j.split('\t')[:3]
    fst = j.split('\t')[4]
    if len(i) == 0: continue
    else: 
        for k in range(len(i)):
            if i[k] > indv_num: major += i[k]
            else: major += indv_num*2-i[k]
        minor = len(i)*indv_num*2 - major
        print >>output1,' '.join(window),len(i),major,minor #print allele count
        hp = 2*major*minor/float((len(i)*indv_num*2)**2) #calculate hp 
        print >>output2,' '.join(window),fst,hp #print Fst and Hp
