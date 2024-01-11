import numpy as np
import subprocess
from time import time
from statistics import mean

def mc_euro_call_controller(S, K, r, sigma, q, T, M, workers):
	'''
	Prices a European call option with Monte Carlo, utilizing a SLURM cluster. 
	This function should be ran in the /home directory of the SLURM controller computer.

	S: float, initial stock price
	K: float, strike price
	r: float, risk-free rate
	sigma: float, volatility
	q: float, dividend yield
	T: int, time to maturity in years
	M: int, number ofa simulations
	workers: int, number of worker computers to employ
	'''
	if M % workers != 0:
		M = M + (workers - M % workers)
		print(f"M adjusted to {M} to be evenly divisible by {workers} workers.")
	n = int(M/workers)
	# Build SLURM job command
	command_list = ['srun', f"-N{workers}",'python3','mc_euro_call_partial.py', str(S), str(K), str(r), str(sigma), str(q), str(T), str(n), str(M)]
	# Launch SLURM job and collect results
	result = subprocess.run(command_list, capture_output=True, text=True, check=True)
	result = result.stdout.strip()
	result = list(result.splitlines())
	for i in range(len(result)):
		result[i] = float(result[i])
	# Sum values and discount to present time
	sum_call = sum(result)
	call_value = np.exp(-r * T) * sum_call
	return call_value

if __name__ == "__main__":
    # Option parameters
	S = 100   
	K = 100      
	r = 0.05     
	sigma = 0.2 
	q = 0.01       
	T = 1

    # Average runtime and average price error experiment
	M = 100000000 # Number of simulations
	workers = 4 # Number of workers to employ
	bs_price = 16.79983686 # Black-Scholes price to compare to
	runs = 10 # Number of runs to average over
	average_runtime = 0
	runtimes = []
	prices = []
	for i in range(runs):
		print(f"run {i}/{runs}")
		start = time()	
		price = mc_euro_call_controller(S, K, r, sigma, q, T, M, workers)
		end = time()
		runtime = end-start
		runtimes.append(runtime)
		prices.append(price)
		average_runtime += runtime/runs		
		print(f"\nworkers = {workers}")
		print(f"sims = {M}")
		print(f"price = {price}")
		print(f"time = {round(runtime,6)} seconds")
		print(f"running_average = {round((average_runtime*runs)/(i+1),6)}")
		
	# Calculate and print results
	average_runtime = round(mean(runtimes),5)
	average_error = float(round(abs(mean(prices)-bs_price),5))
	print("---------------------------------------------------")
	print(f"\nworkers = {workers}")
	print(f"sims = {M}")
	print(f"\nRUNTIMES")
	for i in range(len(runtimes)):
		print(f"run {i}, {runtimes[i]} seconds.")
	print(f"\nPRICES")
	for i in range(len(prices)):
		print(f"run {i}, {prices[i]}")
	print(f"\nAVERAGE RUNTIME = {average_runtime}")
	print(f"AVERAGE ERROR = {average_error}")
