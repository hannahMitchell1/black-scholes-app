
import math
from scipy.stats import norm
import numpy as np
import pandas as pd
import streamlit as st
from bs_model import black_scholes, generate_price_grid
from bs_model import binomial_, generate_price_grid
import seaborn as sns
import matplotlib.pyplot as plt

#the html for when the generate button is pressed
def html_for_buttons(model_type, option, S_current, K, T, r, sigma):
    if model_type == "Black-Scholes":
        option_price = black_scholes(S_current, K, T, r, sigma, option)
    else:
        option_price = binomial_(S_current, K, T, r, sigma, option, steps=100)

    if option == "call":
        value_label = "CALL" 
        st.markdown(
        f"""
        <div style="background-color:#90ee90;
                    padding:1rem 1.5rem;
                    border-radius:10px;
                    width:200px;
                    margin-bottom:1rem;
                    margin-left:0px;">
            <h4 style="margin:0; font-size:1rem;">{value_label} Value</h4>
            <h2 style="margin:0; font-size:1.5rem;">${option_price:.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
        )
    else:
        value_label = "PUT"
        st.markdown(
        f"""
        <div style="background-color:#ff6961;
                    padding:1rem 1.5rem;
                    border-radius:10px;
                    width:200px;
                    margin-bottom:1rem;
                    margin-left:0px;">
            <h4 style="margin:0; font-size:1rem;">{value_label} Value</h4>
            <h2 style="margin:0; font-size:1.5rem;">${option_price:.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
        )
#make heatmap
def heat_map(S_min, S_max,option_type,sigma_min, sigma_max, K, T, r):
    S_vals = np.linspace(S_min, S_max, 25)
    sigma_vals = np.linspace(sigma_min, sigma_max, 25)
    price_grid = generate_price_grid(K, T, r, option_type, S_vals, sigma_vals)

    fig, ax = plt.subplots()
    sns.heatmap(price_grid, xticklabels=np.round(S_vals, 2), yticklabels=np.round(sigma_vals, 2),
                cmap="RdYlGn_r", ax=ax, cbar_kws={'label': 'Option Price'})
    ax.set_xlabel("Spot Price (S)")
    ax.set_ylabel("Volatility (\u03C3)")
    ax.set_title(f"{option_type.capitalize()} Option Price Heatmap")


    st.pyplot(fig)