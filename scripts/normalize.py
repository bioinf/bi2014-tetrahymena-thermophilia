f = open("Tetrahymena_thermophila.JCVI-TTA1-2.2.23.dna.genome.fa", "r")
out = open("normalized.fa", "w")
count = 0
for line in f.readlines():
	if line[0] == '>':
		out.write(">supercontig "+str(count)+"\n")
		count += 1
	else:
		out.write(line)

	
