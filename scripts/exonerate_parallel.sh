#!/bin/bash

pids=()
echo "Running $1 exonerate instances"
for i in $(seq 1 1 $1)
do
   echo $i
   exonerate --model protein2genome -t ../data/T_thermophila_June2014_assembly.fasta -q /home/andrey/bionif/bi2014-tetrahymena-thermophilia/data/genomes/relatives/proteins_part.fast --percent 80 --showtargetgff --showvulgar no --showalignment no --geneticcode 6 --querychunkid $i --querychunktotal $1] > ../data/exout_$i &
   pids+=($!)
done

for pid in "${pids[@]}"
do
   wait $pid
done
