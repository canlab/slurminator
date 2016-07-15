queue="batch"
processors=1
memory="4GB"
standard_output="~/slurminator.out"
job_name="testjob"
parameter_lists={"n_points":[(750,750)],
                 "dx":[(0.2,0.2)],
                 "dt":[0.015],
                 "EnergyThreshold":[1.0E-13],
                 "outputFolder":["'"+output_dir+"'"],
                 "wavelength_nm":[800],
                 "intensity_w_cm2":[1E13,5E13,1E14],
                 "carrier_envelope_phase":[(2.0*math.pi/cep_pts)*x for x in range(0,cep_pts)],
                 "pulse_length_cycles":[3,5,10],
                 "free_propagation_time":[500],
                 "pre_run_propagation_time":[1000],
                 "soft_core":[0.5], 
                 "Z_eff":[1.9]}

