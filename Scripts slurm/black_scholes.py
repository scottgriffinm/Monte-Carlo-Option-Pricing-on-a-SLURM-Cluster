import numpy as np
from scipy.stats import norm

def black_scholes_euro_call(S, K, r, sigma, q, T):
    d1 = (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_value = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_value


if __name__ == "__main__":
    S = 110
    K = 100
    r = 0.05
    sigma = 0.2
    q = 0.01
    T = 1
    print(black_scholes_euro_call(S, K, r, sigma, q, T))