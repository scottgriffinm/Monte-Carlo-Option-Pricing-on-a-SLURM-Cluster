from time import time
import numpy as np
from statistics import mean
import mc_euro_call_no_slurm

'''Single, independent computer script for pricing a number of European 
call options with Monte Carlo for a number of worker computers and 
asset path simulations.'''

if __name__ == "__main__":
	# Option parameters
	S = 110   
	K = 100      
	r = 0.05     
	sigma = 0.2 
	q = 0.01       
	T = 1
	# Experiment parameters
	total_simulations = 100000000 
	bs_price = 16.79983686 # Black-Scholes price to compare to
	runs = 10 
	average_runtime = 0
	runtimes = []
	prices = []
	# Run runtime and pricing experiment
	for i in range(runs):
		print(f"\nrun {i}/{runs}")
		start = time()	
		price = mc_euro_call_no_slurm(S, K, r, sigma, q, T, total_simulations)
		end = time()
		runtime = end-start
		runtimes.append(runtime)
		prices.append(price)
		average_runtime += runtime/runs		
		print(f"sims = {total_simulations}")
		print(f"price = {price}")
		print(f"time = {round(runtime,6)} seconds")
		print(f"running_average = {round((average_runtime*runs)/(i+1),6)}")
	# Print runtimes and prices
	average_runtime = round(mean(runtimes),5)
	average_error = float(round(abs(mean(prices)-bs_price),5))
	print("---------------------------------------------------")
	print(f"\nsingle, independent computer")
	print(f"sims = {total_simulations}")
	print(f"\nRUNTIMES")
	for i in range(len(runtimes)):
		print(f"run {i}, {runtimes[i]} seconds.")
	print(f"\nPRICES")
	for i in range(len(prices)):
		print(f"run {i}, {prices[i]}")
	print(f"\nAVERAGE RUNTIME = {average_runtime}")
	print(f"AVERAGE ERROR = {average_error}")