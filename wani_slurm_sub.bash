#!/bin/bash

#Wall Clock time, maximum of 300 minutes
#SBATCH -t 300

#SBATCH -o ~/slurm-output.txt
#SBATCH -e ~/slurm-error-output.txt

#Sets my email
#SBATCH --mail-user=Choongwan.Woo@colorado.edu

#Names the job
#SBATCH --job-name=wani-job

#Sets maximum memory and number of processors
#SBATCH --mem=3G
#SBATCH -n 1

#SBATCH -p blanca-ics

module load matlab

matlab -nodisplay -nosplash -nodesktop -r "name-of-script.m"
