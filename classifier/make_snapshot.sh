#!/bin/bash
#SBATCH -p medium
#SBATCH -C scratch
#SBATCH -N 1
#SBATCH -c 16
#SBATCH --mem=100GB
#SBATCH -t 48:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nick.haupka@sub.uni-goettingen.de

module load python

python3 document_types_make_snapshot_openalex.py
