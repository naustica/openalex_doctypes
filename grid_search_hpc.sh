#!/bin/bash
#SBATCH -p medium
#SBATCH -C scratch
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mem=100G
#SBATCH -t 07:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nick.haupka@sub.uni-goettingen.de

module load python

python3 grid_search.py