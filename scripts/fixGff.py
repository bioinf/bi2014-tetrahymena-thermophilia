#Fixes exonerate gff output to be suitable for Augustus
import sys

gff_in = open(sys.argv[1])
gff_out = open(sys.argv[2], 'w')


id = 0
skip = False
for line in gff_in.readlines():
	if skip:
		skip = False
		gff_out.write('\n\n')
		continue
	line = line.strip()
	if line:	
		columns = line.split('\t')
		to_append = 'alignment {}'.format(id)
		if len(columns) < 9:
			columns.append(to_append)
		else:
			columns[8] = to_append
		gff_out.write('\t'.join(columns)+'\n')
	else:
		id += 1
		skip = True




