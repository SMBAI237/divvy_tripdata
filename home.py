import pandas as pd 
import numpy as np
import plotly.express as px
import streamlit as st
import pydeck as pdk

##### create load data function
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

# set url
url = "data/202011-divvy-tripdata.csv"
# call function
df_divvy = load_data(url)
st.title("🚕 Divvy Trip Exploratory Data Analysis")
st.markdown("______")
st.subheader("This app give some insights in the divvy bikesharing dadaset! in november 2020")

