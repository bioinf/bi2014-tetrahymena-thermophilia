#augustus_set.py gff_in gff_out selects top 1000 gff entries for augustus
import sys

gff_in = open(sys.argv[1])
gff_out = open(sys.argv[2], 'w')

lengths = []
while True:
	line = gff_in.readline().strip()
	if not line:
		break
	columns = line.split('\t')
	length = int(columns[5])
	lengths.append(length)

	while True:
		line = gff_in.readline().strip()
		if not line:
			gff_in.readline()
			break


length_set = set(sorted(lengths, reverse=True)[0:1000])

gff_in = open(sys.argv[1])

while True:
	write = False
	line = gff_in.readline().strip()
	if not line:
		break
	columns = line.split('\t')
	length = int(columns[5])
	if length in length_set:
		gff_out.write(line+'\n')
		write = True
	while True:
		line = gff_in.readline().strip()
		if write:		
			gff_out.write(line+'\n')
		if not line:
			if write:
				gff_out.write('\n\n')
			gff_in.readline()
			break

