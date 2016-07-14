#!/home/becker/weflen/progs/bin/python3

from itertools import product
from subprocess import STDOUT,PIPE,Popen,call
import math
import sys

queue="batch"
key=0
processors=1
config_prefix="/home/becker/weflen/Queue_Config/"
prog_name="/home/becker/weflen/npsf_h/npsf_h"
queue_prefix=open("queue_h_prefix","r").read()
run_name="second_trial_run"
output_dir="/mpdata/becker/weflen/H/"+run_name+"/"
jobname=output_dir+run_name
queue_display_name=run_name

cep_pts=20
parameter_lists={"n_points":[(750,750)],
                 "dx":[(0.2,0.2)],
                 "dt":[0.015],
                 "EnergyThreshold":[1.0E-13],
                 "outputFolder":["\""+output_dir+"\""],
                 "wavefunctionFolder":["\""+output_dir+"\""],
                 "run_name":["\""+run_name+"\""],
                 "wavelength_nm":[800],
                 "intensity_w_cm2":[1E13,5E13,1E14],
                 "carrier_envelope_phase":[(2.0*math.pi/cep_pts)*x for x in range(0,cep_pts)],
                 "pulse_length_cycles":[3,5,10],
                 "free_propagation_time":[500],
                 "pre_run_propagation_time":[1000],
                 "soft_core":[0.5], 
                 "absorber_fraction":[tuple(0.2 for x in range(4))],
                 "Z_eff":[1.9],
                 "jobname":["\""+jobname+"\""]}

param_dicts=[zip(parameter_lists.keys(), params) for params in product(*parameter_lists.values())]


def print_list_as_config_file(filename, params,key):
   with open(filename,"w") as config_file:
      output_string=""
      for item in params:
         output_string=output_string+str(item[0])+"="+str(item[1])+"\n"
      config_file.write(output_string+"key="+str(key)+"\n")
      

for parameter_dict in param_dicts:
   print_list_as_config_file(config_prefix+"config"+str(key)+".inp",parameter_dict,key)
   queue_file_text=queue_prefix+"\n#PBS -l nodes=1:ppn="+str(processors)+"\n\n"
   queue_file_text=queue_file_text+"#PBS -N "+queue_display_name+"\n\n"
   queue_file_text=queue_file_text+"#PBS -o "+prog_name"_"run_name+".out\n\n"
   queue_file_text=queue_file_text+"\n"+"mkdir -p "+output_dir+"\n"
   queue_file_text=queue_file_text+"\n"+"export OMP_NUM_THREADS="+str(processors)+"\n\n\n"
   queue_file_text=queue_file_text+prog_name+" "+config_prefix+"config"+str(key)+".inp\n"
   open("queue_h.bash","w").write(queue_file_text)
   result_string=Popen(["qsub","-q",queue, "queue_h.bash"],stderr=STDOUT,stdout=PIPE).stdout.read().decode("utf-8")
   sys.stdout.write(result_string)
   key=key+1

