import numpy as np
import subprocess

def mc_euro_call_garch_controller(S, K, r, sigma0, q, T, N, kappa, theta, lambda_, total_simulations, workers):
	if total_simulations % workers != 0:
		total_simulations += (workers - total_simulations % workers)
		print(f"Total number of simulations adjusted to {total_simulations} to be evenly divisible by {workers} workers.")
	worker_simulations = int(total_simulations/workers)
	# Build SLURM job command
	worker_commands = [S, K, r, sigma0, q, T, N, kappa, theta, lambda_, worker_simulations, total_simulations]
	command_list = ['srun', f"-N{workers}",'python3','mc_euro_call_garch_worker.py']
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
	S = 100       
	K = 105       
	r = 0.05    
	sigma0 = 0.2 
	q = 0.02    
	T = 1       
	N = 5
	kappa = 0.1
	theta = sigma0  
	lambda_ = 0.6
	total_simulations = 1_000_000 
	workers = 1
	price = mc_euro_call_garch_controller(S, K, r, sigma0, q, T, N, kappa, theta, lambda_, total_simulations, workers)
	print(f"Workers = {workers}")
	print(f"Total Simulations = {total_simulations}")
	print(f"Price = {price}")
