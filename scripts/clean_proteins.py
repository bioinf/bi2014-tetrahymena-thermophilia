import sys

def loadRegions(genome_file):
	res = {}
	region = ""
	dna = ""

	for line in genome_file.readlines():
		if line.startswith('>'):
			if region:
				res[region] = dna
			region = line[1:-1]
			dna = ""
		else:
			dna += line.strip()
	if region:
		res[region] = dna
	return res			

def printRegions(f, regions):
	for region in regions:
		f.write('>'+region)
		f.write("\n")
		f.write(regions[region])
		f.write("\n")				

regions = loadRegions(open(sys.argv[1]))
count = 0
include_count = 0
c_regions = regions.copy()
for region in regions:
	protein = regions[region]
	if protein.startswith('M') and protein.endswith('*'):
		include_count+=1
	else:
		del c_regions[region]	
	count+=1

print "Total: {}".format(count)
print "Valid: {}".format(include_count)

printRegions(open(sys.argv[2], 'w'), c_regions)

