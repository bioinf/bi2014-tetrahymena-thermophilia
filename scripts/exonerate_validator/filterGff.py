import sys
from string import maketrans


def reverseComplementary(dna):
	trans = maketrans("ACGT", "TGCA")
	cDna = dna[::-1].translate(trans)
	return cDna


def is_start_codon(codon):
	return codon == 'ATG'

def validateCds(dna, triplet_before_dna, triplet_after_dna):
	first_codon = dna[0:3]
	print "First codon in CDS ({}) is start codon: {}".format(first_codon, is_start_codon(first_codon))
	print "Tripplet before CDS ({}) is start codon: {}".format(triplet_before_dna, is_start_codon(triplet_before_dna))
	
	res = is_start_codon(first_codon) or is_start_codon(triplet_before_dna)

	print "CDS:"+dna
	length_valid = (len(dna)%3 == 0)
	print "Length ({}) valid: {}".format(len(dna), length_valid)
	res &= length_valid

	count = 0
	for i in xrange(0, len(dna)-3, 3):
		if dna[i:i+3]=='TGA':
			count+=1
	stop_codons_count_valid = (count == 0)
	print "Number of stop codons inside CDS ({}) valid: {}".format(count, stop_codons_count_valid)
	res &= stop_codons_count_valid

	stop_codon_valid = (triplet_after_dna == 'TGA')
	print "Stop codon ({}) valid: {}".format(triplet_after_dna, stop_codon_valid)
	res &= stop_codon_valid

	return res


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

def getDna(regions, region, begin, end):
	return regions[region][begin:end]


def validateGffEntry(entry, regions, gffout):
	res = ""
	strand = ""
	exons = []
	line = entry[0]
	columns = line.split('\t')
	strand = columns[6]
	region = columns[0]
	begin = int(columns[3])
	end = int(columns[4])

	print '>'+columns[8]
	if strand == '+':
		tripplet_after_cds = getDna(regions, region, end, end+3)
		tripplet_before_cds = getDna(regions, region, begin-4, begin-1)
	else:
		tripplet_after_cds = reverseComplementary(getDna(regions, region, begin-4, begin-1))
		tripplet_before_cds = reverseComplementary(getDna(regions, region, end, end+3))


	for i in xrange(1, len(entry)):
		line = entry[i]
		columns = line.split('\t')
		t = columns[2]
		if t == 'exon':
			strand = columns[6]
			begin = int(columns[3])-1
			end = int(columns[4])
			dna = getDna(regions, columns[0], begin, end)
		
			if strand == '+':
				exons.append(dna)
			else:
				exons.append(reverseComplementary(dna))

	cds = ''.join(exons)
	stop_codon = cds[len(cds)-3:len(cds)]

	include = validateCds(''.join(exons), tripplet_before_cds, stop_codon) 
	print "Gff entry included: {}".format(include)
	if include:	
		gffout.write("\n".join(entry))
		gffout.write("\n\n\n")
		return True
	return False

if len(sys.argv) < 4:
	print "Usage: python filterGff.py <genome> <gff> <filtered-gff>"
	print "Report will be directed to stdout"
	sys.exit()

regions = loadRegions(open(sys.argv[1]))
f = open(sys.argv[2])
gffout = open(sys.argv[3], 'w')

entry = []
entries_count = 0
included_entries_count = 0

for line in f.readlines():
	if line.startswith('--') or line.startswith('Command') or line.startswith('Hostname'):
		continue
	if not line.startswith('#'):
		entry.append(line.strip())
	elif entry:
		entries_count += 1
		if validateGffEntry(entry, regions, gffout):
			included_entries_count += 1
		print "\n"
		entry = []

print "Total entries: {}".format(entries_count)
print "Included entries: {}".format(included_entries_count)

