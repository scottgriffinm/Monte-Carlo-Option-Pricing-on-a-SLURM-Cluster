import numpy as np

'''Single, independent computer script for pricing a European down-and-out 
call option using Monte Carlo simulation.'''

def mc_euro_down_and_out_call(S, K, r, sigma, q, T, H, N, total_simulations):
	'''Prices a European down-and-out call option using Monte Carlo 
	simulation.
	
	S: float, initial stock price
	K: float, strike price
	r: float, risk-free interest rate
	sigma: float, volatility
	q: float, dividend yield
	T: int, time to maturity
	H: float, barrier price
	N: int, number of monitoring points
	total_simulations: int, total number of simulations'''
	# Precompute constants
	dt = T/N 
	nudt = (r - q - 0.5*sigma*sigma)*dt
	sigsdt = sigma * np.sqrt(dt)
	sum_CT = 0
	# Simulate asset paths
	for i in range(total_simulations):
		St = S
		BARRIER_CROSSED = False
		for j in range(N):
			e = np.random.randn()
			St = St * np.exp(nudt + sigsdt*e)
			if St <= H:
				BARRIER_CROSSED = True
				break
		if BARRIER_CROSSED:
			CT = 0
		else:
			CT = np.maximum(0, St - K)
		sum_CT += CT
	# Average call value and discount to present time
	call_value = sum_CT/total_simulations*np.exp(-r*T)	
	return call_value

if __name__ == "__main__":
	# Example usage
	K = 100
	T = 1
	S = 100
	sigma = 0.2
	r = 0.06
	q = 0.03
	H = 99
	N = 10
	total_simulations = 1_000_000
	print(f"Simulations = {total_simulations}")
	print("Price = ", mc_euro_down_and_out_call(S, K, r, sigma, q, T, H, N, total_simulations))







