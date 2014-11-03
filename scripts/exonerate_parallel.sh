#!/bin/bash

pids=()
for i in {1..5}
do
   exonerate --model protein2genome -t ../data/T_thermophila_June2014_assembly.fasta -q ../data/sample-proteins.fa --percent 80 --showtargetgff --showvulgar no --showalignment no --querychunkid $i --querychunktotal 5] > ../data/exout_$i &
   pids+=($!)
done

for pid in "${pids[@]}"
do
   wait $pid
done
