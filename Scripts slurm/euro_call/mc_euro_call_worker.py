import numpy as np
import sys

'''Worker computer script for pricing a European call option using Monte Carlo
simulation. This script should be located in the /home directory of all SLURM 
worker computers.'''

def mc_euro_call_worker(S, K, r, sigma, q, T, worker_simulations, total_simulations):
    '''Worker computer function for pricing a European call option using Monte Carlo 
    simulation.
    
    S: float, initial stock price
    K: float, strike price
    r: float, risk-free interest rate
    sigma: float, volatility
    q: float, dividend yield
    T: int, time to maturity
    worker_simulations: int, number of simulations to run on this worker
    total_simulations: int, total number of simulations'''
    # Precompute constants
    drift = (r - q - 0.5 * sigma**2) * T
    sig_sqrt_t = sigma * np.sqrt(T)
    up_change = np.log(1.01)
    down_change = np.log(0.99)
    sum_call = 0
    sum_call_change = 0
    sum_pathwise = 0
    random_numbers = np.random.randn(worker_simulations)
    # Simulate asset paths
    for i in range(worker_simulations):
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
    # Average payoffs by total simulations
    return sum_call/total_simulations

if __name__ == "__main__":
    # Collect arguments from SLURM job command
    S = float(sys.argv[1]) 
    K = float(sys.argv[2])
    r = float(sys.argv[3])
    sigma = float(sys.argv[4])
    q = float(sys.argv[5])
    T = int(sys.argv[6])
    worker_simulations = int(sys.argv[7])
    total_simulations = int(sys.argv[8])
    # Return partial average payoff to controller computer
    print(mc_euro_call_worker(S, K, r, sigma, q, T, worker_simulations, total_simulations))




