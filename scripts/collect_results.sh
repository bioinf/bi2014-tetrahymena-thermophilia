#!/bin/bash


find $1 -name "exout_*" | xargs cat > exout_cat

python filterGff.py ../data/T_thermophila_June2014_assembly.fasta exout_cat "../data/exout_cat_filtered" > "../data/exout_cat_report"

