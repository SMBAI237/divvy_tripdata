import pandas as pd 
import numpy as np
import plotly.express as px
import streamlit as st
import pydeck as pdk

##### create load data function

# Get the dataframe from the home page

if 'divvy' in st.session_state:
    df_divvy = st.session_state['divvy']

    # Get the file name loaded in the home page
    if 'file_name' in st.session_state:
        file_name = st.session_state['file_name']

        st.subheader("📈  This page display some usefuls metrics about your Divvy trip dataset 👉🏽 **{}**".format(file_name))

    st.markdown("______")

    # daily rides
    daily_ride = df_divvy.groupby("started_date")["unit"].sum().reset_index()
    daily_duration = df_divvy.groupby("started_date")["duration_min"].sum().reset_index()
    st.write(" ")
    st.badge("📌 Rides overview")
    col1, col2 = st.columns(2)
    col1.metric(label="🚲 Total rides", value=len(df_divvy), height='stretch', border=True)
    col2.metric(label="🛴 Daily average rides", value=round(daily_ride["unit"].mean()), height='stretch', border=True)
    st.write(" ")

    st.badge("📌 Rides durations", color="green")
    col3, col4 = st.columns(2)
    col3.metric(label="⌚️ Average hours spent (Daily)", value=round(daily_duration["duration_min"].mean()/60, 2), height='stretch', border=True)
    col4.metric(label="⏳ Average trip duration (Min)", value=round(df_divvy["duration_min"].mean(),2), height='stretch', border=True)

else:
    st.markdown("_____")
    st.write("🚨 Data not available. Please check the loading process on the home page.") 