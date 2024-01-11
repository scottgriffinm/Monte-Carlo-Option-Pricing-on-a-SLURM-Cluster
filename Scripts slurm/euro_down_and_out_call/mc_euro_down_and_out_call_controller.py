import numpy as np
import subprocess

'''Controller computer script for pricing a European down-and-out call option using 
Monte Carlo simulation. This script should be ran in the /home directory of the 
SLURM controller computer.'''

def mc_euro_down_and_out_call_controller(S, K, r, sigma, q, T, H, N, total_simulations, workers):
	'''Controller computer function for pricing a European down-and-out call option using 
	Monte Carlo simulation. 
	
	S: float, initial stock price
	K: float, strike price
	r: float, risk-free interest rate
	sigma: float, volatility
	q: float, dividend yield
	T: int, time to maturity
	H: float, barrier
	N: int, number of monitoring points
	total_simulations: int, total number of simulations
	workers: int, number of workers to employ'''
	if total_simulations % workers != 0:
		total_simulations += (workers - total_simulations % workers)
		print(f"Total number of simulations adjusted to {total_simulations} to be evenly divisible by {workers} workers.")
	worker_simulations = int(total_simulations/workers)
	# Build SLURM job command
	worker_commands = [S, K, r, sigma, q, T, H, N, worker_simulations, total_simulations]
	command_list = ['srun', f"-N{workers}",'python3','mc_euro_down_and_out_call_worker.py']
	for i in range(len(worker_commands)):
		command_list.append(str(worker_commands[i]))
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
	# Example usage
	S = 100
	K = 100
	T = 1
	sigma = 0.2
	r = 0.06
	q = 0.03
	H = 99
	N = 10
	total_simulations = 1_000_000
	workers = 1
	price = mc_euro_down_and_out_call_controller(S, K, r, sigma, q, T, H, N, total_simulations, workers)
	print(f"Workers = {workers}")
	print(f"Total Simulations = {total_simulations}")
	print(f"Price = {price}")
