import subprocess
from time import time

'''Controller computer script for calculating the average of a number of random numbers.
This script should be run in the \home directory of the SLURM controller computer.'''

if __name__ == "__main__":
	start = time()	# Start timer
	runs = 1_000_000_000
	# Build command list
	command_list = ['srun','python3','simple_slurm_speed_test_partial.py', f"{runs}"]
	# Launch SLURM job and collect results
	result = subprocess.run(command_list, capture_output=True, text=True, check=True)
	result = result.stdout.strip()
	end = time()	# End timer
	# Print results
	print(f"random_avg = {result}")
	print(f"time = {round(end-start,6)} seconds")