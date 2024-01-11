import numpy as np
import sys

def mc_euro_call_garch_worker(S, K, r, sigma0, q, T, N, kappa, theta, lambda_, worker_simulations, total_simulations):
	dt = T/N
	Sqrdt = np.sqrt(dt)
	a = kappa * theta
	b = (1 - kappa) * lambda_
	c = (1 - kappa) * (1 - lambda_)
	LogS0 = np.log(S)
	SumCall = 0
	SumCallSq = 0
	for i in range(worker_simulations):
		LogS = LogS0
		sigma = sigma0
		for j in range(N):
			y = sigma * np.random.randn()
			LogS += (r - q - 0.5 * sigma**2) * dt + Sqrdt * y
			sigma = np.sqrt(a + b * y**2 + c * sigma**2)
		CallV = max(0, np.exp(LogS) - K)
		SumCall += CallV
		SumCallSq += CallV**2
	return SumCall/total_simulations

if __name__ == "__main__":
	# Collect arguments from SLURM job command
    S = float(sys.argv[1])
    K = float(sys.argv[2])
    r = float(sys.argv[3])
    sigma0 = float(sys.argv[4])
    q = float(sys.argv[5])
    T = int(sys.argv[6])
    N = int(sys.argv[7])
    kappa = float(sys.argv[8])
    theta = float(sys.argv[9])
    lambda_ = float(sys.argv[10])
    worker_simulations = int(sys.argv[11])
    total_simulations = int(sys.argv[12])
	# Return partial average payoff to controller computer
    print(mc_euro_call_garch_worker(S, K, r, sigma0, q, T, N, kappa, theta, lambda_, worker_simulations, total_simulations))




