import numpy as np

def mc_euro_call_garch(S, K, r, sigma0, q, T, N, kappa, theta, lambda_, total_simulations):
	dt = T/N
	Sqrdt = np.sqrt(dt)
	a = kappa * theta
	b = (1 - kappa) * lambda_
	c = (1 - kappa) * (1 - lambda_)
	LogS0 = np.log(S)
	SumCall = 0
	SumCallSq = 0
	for i in range(total_simulations):
		LogS = LogS0
		sigma = sigma0
		for j in range(N):
			y = sigma * np.random.randn()
			LogS += (r - q - 0.5 * sigma**2) * dt + Sqrdt * y
			sigma = np.sqrt(a + b * y**2 + c * sigma**2)
		CallV = max(0, np.exp(LogS) - K)
		SumCall += CallV
		SumCallSq += CallV**2
	CallV = np.exp(-r * T) * SumCall/total_simulations
	return CallV

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
	print(f"Simulations = {total_simulations}")
	print("Price =  ", mc_euro_call_garch(S, K, r, sigma0, q, T, N, kappa, theta, lambda_, total_simulations))









