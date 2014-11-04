#!/bin/bash

for i in $(seq 1 1 $1)
do
   echo $i
   python filterGff.py ../data/T_thermophila_June2014_assembly.fasta "../data/exout_${i}" "../data/exout_${i}_filtered" > "../data/exout_${i}_report"
done
