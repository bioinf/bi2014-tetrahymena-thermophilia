#!/bin/bash

pids=()
echo "Running $1 exonerate instances"
for i in $(seq 1 1 $1)
do
   echo $i
   exonerate --model protein2genome -t ../data/T_thermophila_June2014_assembly.fasta -q ../data/sample-proteins.fa --percent 80 --showtargetgff --showvulgar no --showalignment no --querychunkid $i --querychunktotal $1] > ../data/exout_$i &
   pids+=($!)
done

for pid in "${pids[@]}"
do
   wait $pid
done
