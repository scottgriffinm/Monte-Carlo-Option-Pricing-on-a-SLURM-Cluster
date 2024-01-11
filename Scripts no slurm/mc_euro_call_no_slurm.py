from time import time
import numpy as np

'''Single, independent computer script for pricing a European call option 
with Monte Carlo simulation.'''

def mc_euro_call(S, K, r, sigma, q, T, total_simulations):
	'''Prices a European call option using Monte Carlo simulation.

	S: float, initial stock price
	K: float, strike price
	r: float, risk-free rate
	sigma: float, volatility
	q: float, dividend yield
	T: int, time to maturity in years
	total_simulations: int, number of simulations'''
	# Precompute constants
	sum_call = 0
	drift = (r - q - 0.5 * sigma**2) * T
	sig_sqrt_t = sigma * np.sqrt(T)
	up_change = np.log(1.01)
	down_change = np.log(0.99)
	sum_call = 0
	sum_call_change = 0
	sum_pathwise = 0
	random_numbers = np.random.randn(total_simulations)
	# Simulate asset paths
	for i in range(total_simulations): 
		log_st = np.log(S) + drift + sig_sqrt_t * random_numbers[i]
		call_val = max(0, np.exp(log_st) - K)
		sum_call += call_val
		log_su = log_st + up_change
		call_vu = max(0, np.exp(log_su) - K)
		log_sd = log_st + down_change
		call_vd = max(0, np.exp(log_sd) - K)
		sum_call_change += call_vu - call_vd
		if np.exp(log_st) > K:
			sum_pathwise += (np.exp(log_st) / S)
	# Discount average call value to present time	
	call_value = np.exp(-r * T) * sum_call/total_simulations 
	return call_value

if __name__ == "__main__":
    # Example usage
    S = 90 	 
    K = 100 	 
    r = 0.05	 
    sigma = 0.2
    q = 0.01  	 
    T = 1   	 
    M = 1_000_000
    price = mc_euro_call(S, K, r, sigma, q, T, M)
    print(f"Simulations = {M}")
    print(f"Price = {price}")

    
    
    




