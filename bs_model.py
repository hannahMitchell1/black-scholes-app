import math
from scipy.stats import norm
import numpy as np
import pandas as pd
import streamlit as st

#black scholes method
def black_scholes(S, K, T, r, sigma, option):
    x = (math.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*math.sqrt(T))
    y = x - sigma*math.sqrt(T)
    if option == "call":
        price = S*norm.cdf(x) - K*math.exp(-r*T)*norm.cdf(y)
    else:
        price = K*math.exp(-r*T)*norm.cdf(-y) - S*norm.cdf(-x)
    return price

#binomial method
def binomial_(S, K, T, r, sigma, option, steps=100):
    c = T/steps
    u = np.exp(sigma*np.sqrt(c))
    d = 1/u
    p = (np.exp(r*c)- d)/(u - d)
    asset_prices = np.zeros((steps + 1, steps + 1))
    
    for i in range(steps + 1):

        for j in range(i + 1):
            asset_prices[j, i] = S*(u**(i - j))*(d**j)

    op_values = np.zeros((steps + 1, steps + 1))
    if option == "call":
        op_values[:, steps] = np.maximum(0, asset_prices[:, steps] - K)
    else:
        op_values[:, steps] = np.maximum(0, K - asset_prices[:, steps])

    for i in range(steps - 1, -1, -1):

        for j in range(i + 1):
            op_values[j, i] = np.exp(-r*c)*(p*op_values[j, i + 1] + (1 - p)*op_values[j + 1, i + 1])

    return op_values[0, 0]

#produce heat maps
def generate_price_grid(K, T, r, option, S_vals, sigmas):
    data = []
    for sigma in sigmas:
        row = []
        for S in S_vals:
            price = black_scholes(S, K, T, r, sigma, option)
            row.append(price)
        data.append(row)

    df = pd.DataFrame(data, index=sigmas, columns=S_vals)
    return df
