import numpy as np
import subprocess
from scipy.stats import norm

'''Controller computer script for pricing an Asian call option using Monte Carlo simulation
with a geometric control variate. This script should be ran in the /home directory 
of the SLURM controller computer.'''

def black_scholes_euro_call(S, K, r, sigma, q, T):
	'''Prices a European call option using the Black-Scholes formula.
	
	S: float, initial stock price
	K: float, strike price
	r: float, risk-free interest rate
	sigma: float, volatility
	q: float, dividend yield
	T: int, time to maturity'''
	d1 = (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
	d2 = d1 - sigma * np.sqrt(T)
	call_value = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
	return call_value

def geometric_asian_call(S, K, sigma, r, q, T, N):
	'''Prices a geometric Asian call option using the Black-Scholes formula.
	
	S: float, initial stock price
	K: float, strike price
	sigma: float, volatility
	r: float, risk-free interest rate
	q: float, dividend yield
	T: int, time to maturity
	N: int, number of monitoring points'''
	dt = T/N
	nu = r - q - 0.5 * sigma * sigma
	a = N * (N + 1) * (2 * N + 1) / 6
	V = np.exp(-r*T)*S*np.exp(((N+1)*nu/2 + sigma*sigma*a/(2*N*N))*dt)
	sigavg = sigma * np.sqrt(a) / (N**1.5)
	call_value = black_scholes_euro_call(V, K, r, sigavg, 0, T)
	return call_value

def mc_asian_call_control_variate_controller(S, K, r, sigma, q, T, total_simulations, workers):
	'''Controller computer function for pricing an Asian call option using Monte Carlo 
	simulation with a geometric control variate.
	
	S: float, initial stock price
	K: float, strike price
	r: float, risk-free interest rate
	sigma: float, volatility
	q: float, dividend yield
	T: int, time to maturity
	total_simulations: int, total number of simulations
	workers: int, number of workers to employ'''
	if total_simulations % workers != 0:
		total_simulations += (workers - total_simulations % workers)
		print(f"Total number of simulations adjusted to {total_simulations} to be evenly divisible by {workers} workers.")
	worker_simulations = int(total_simulations/workers)
	# Build SLURM job command
	worker_commands = [S, K, sigma, r, q, T, N, worker_simulations, total_simulations]
	command_list = ['srun', f"-N{workers}",'python3','mc_asian_call_control_variate_worker.py']
	for i in range(len(worker_commands)):
		command_list.append(str(worker_commands[i]))
	# Launch SLURM job and collect results
	result = subprocess.run(command_list, capture_output=True, text=True, check=True)
	result = result.stdout.strip()
	result = list(result.splitlines())
	for i in range(len(result)):
		result[i] = float(result[i])
	# Sum values and discount to present time
	portfolio_value = sum(result) * np.exp(-r * T)
	# Add control variate
	call_price = portfolio_value + geometric_asian_call(S, K, sigma, r, q, T, N)
	return call_price

if __name__ == "__main__":  
	# Example usage
	K = 100
	T = 1
	S = 100
	sigma = 0.2
	r = 0.06
	q = 0.03
	N = 10
	total_simulations = 1_000_000
	workers = 1
	price = mc_asian_call_control_variate_controller(S, K, r, sigma, q, T, total_simulations, workers)
	print(f"Workers = {workers}")
	print(f"Total Simulations = {total_simulations}")
	print(f"Price = {price}")

