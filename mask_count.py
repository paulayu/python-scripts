f = open ('mask_region_from_felcat8_mfa_masked.bed','r')
length = 0
for line in f:
		mask = line.strip('\n').split('\t')
		length += int(mask[2])-int(mask[1])
print "masked length =",length
