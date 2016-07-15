#!/home/becker/weflen/progs/bin/python3

from itertools import product
from subprocess import STDOUT,PIPE,Popen,call
import math
import sys
import uuid

# A "config file" in this sense is a short string of valid matlab assignments. You
#can use it to get 
def print_list_as_config_file(filename, params,identifier):
   with open(filename,"w") as config_file:
      output_string=""
      for item in params:
         output_string=output_string+str(item[0])+"="+str(item[1])+";\n"
      config_file.write(output_string+"identifier="+str(identifier)+"\n")

def slurminator(variable_filename):
   varfile=open(variable_filename)
   #Evaluates the first 10 megabytes of a python script. If you're configuration file
   #is longer than 10 megabytes, you're doing something wrong. Also, "eval" as used
   #here is probably not a problem, as this script is only useful to people who
   #have permission to run arbitrary code on the machine anyway.
   eval(varfile.read(int(1E7)))
   #The file denoted by variable_filename needs to define the following variables,
   #in standard python syntax. You can define whatever you want, or do
   #arbitrary computation as well:
   #  queue: The name of the queue to which the job will be submitted.
   #  processors: The number of processors needed.
   #  memory: The amount of memory needed. A string with a number and unit, like "6GB".
   #  standard_output: File name to dump stdout and stderr. Important for debugging.
   #  job_name: The name that the job will appear as in the queue.
   #  parameter_lists: A dictionary of lists. The job will be run for every value of every list.
   #    Parameter lists will be turned into a series of matlab assignments, to be executed in matlab
   #    before the main script. This allows you to have seperate jobs for each subject (for
   #    preprocessing) or region (for group-level analysis), taking full advantage of the parallelism
   #    of the machine you're running on.

   matlab_script_name="example.m"
   #This converts a dictionary of lists to a list of dictionaries. Each dictionary is a
   #representation of a single job.
   param_dicts=[zip(parameter_lists.keys(), params) for params in product(*parameter_lists.values())]
   for parameter_dict in param_dicts:
      job_id=uuid.uuid4() #Generates a random, universally unique identifier.
      print_list_as_config_file(config_prefix+"config"+str(job_id)+".inp",parameter_dict,job_id)
      queue_file_text=queue_prefix+"\n#PBS -l nodes=1:ppn="+str(processors)+"\n\n"
      queue_file_text=queue_file_text+"#PBS -N "+queue_display_name+"\n\n"
      queue_file_text=queue_file_text+"#PBS -o "+prog_name"_"run_name+".out\n\n"
      queue_file_text=queue_file_text+"\n"+"mkdir -p "+output_dir+"\n"
      queue_file_text=queue_file_text+"\n"+"export OMP_NUM_THREADS="+str(processors)+"\n\n\n"
      queue_file_text=queue_file_text+prog_name+" "+config_prefix+"config"+str(job_id)+".inp\n"
      open("queue_h.","w").write(queue_file_text)
      result_string=Popen(["srun","-q",queue, "queue_h.bash"],stderr=STDOUT,stdout=PIPE).stdout.read().decode("utf-8")
      sys.stdout.write(result_string)

if __name__ =="__main__":
   slurminator(sys.argv[1])

