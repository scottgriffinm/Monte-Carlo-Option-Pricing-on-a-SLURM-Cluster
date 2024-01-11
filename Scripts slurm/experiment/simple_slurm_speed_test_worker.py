import numpy as np
import sys

'''Worker computer script for calculating the average of a number of random numbers.
This script should be located in the \home directory of all SLURM worker computers.'''

if __name__ == "__main__":
	# Collect runs argument from SLURM job command
	runs = int(sys.argv[1])
	random_avg = 0
	for i in range(runs): # Calculate average of random numbers
		random_avg += np.random.randn()/runs 
	print(random_avg) # Return to controller computer
