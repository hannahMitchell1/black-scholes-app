import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs_model import black_scholes, generate_price_grid
from bs_model import binomial_, generate_price_grid
from functions import html_for_buttons
from functions import heat_map

st.set_page_config(layout="wide")

# make all of the buttons/sliders on the sidebar
st.sidebar.title("Options Pricing Heatmap")
st.sidebar.markdown("### Model Parameters")

#parameters for models
model_type = st.sidebar.radio("Model Type", ["Black-Scholes", "Binomial"])
K = st.sidebar.number_input("Strike Price", min_value=1.0, value=150.0, step=1.0)
T = st.sidebar.number_input("Time to Maturity (Years)", min_value=0.01, value=5.0, step=0.50)
r = st.sidebar.number_input("Risk-Free Interest Rate", min_value=0.0, value=0.05, step=0.01)
sigma = st.sidebar.number_input("Volatility (σ)", min_value=0.01, max_value=1.0, value=0.2)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
S_current = st.sidebar.number_input("Current Asset Price", min_value=1.0, value=100.0)

#parameters for heatmap graphic
st.sidebar.markdown("### Heatmap Parameters")
S_min = st.sidebar.number_input("Min Spot Price", min_value=1.0, value=150.0, step=10.0)
S_max = st.sidebar.number_input("Max Spot Price", min_value=1.0, value=250.0, step=10.0)
sigma_min = st.sidebar.slider("Min Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.10)
sigma_max = st.sidebar.slider("Max Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.30)

#Button
value_label = "CALL" if option_type == "call" else "PUT"
option_price = black_scholes(S_current, K, T, r, sigma, option_type)

st.title("Option Price Heatmap")
# right side of screen when a button is pushed
if value_label or option_price or S_min or S_max or sigma_min or sigma_max or K or T or r:
    html_for_buttons(model_type, option_type, S_current, K, T, r, sigma)
    heat_map(S_min, S_max,option_type,sigma_min, sigma_max, K, T, r)