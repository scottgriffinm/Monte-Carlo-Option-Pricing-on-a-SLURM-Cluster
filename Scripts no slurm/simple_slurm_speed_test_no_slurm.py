import numpy as np
import sys
from time import time

'''Single, independent computer script for calculating the average of a number of random numbers.'''

if __name__ == "__main__":
	start = time() # Start timer
	iters = 1_000_000_000
	random_avg = 0
	# Calculate average of random numbers
	for i in range(iters):
		random_avg += np.random.randn()/iters 
	end = time() # End timer
	# Print results
	print(f"random_avg = {random_avg}")
	print(f"time: {round(end-start,6)}")
