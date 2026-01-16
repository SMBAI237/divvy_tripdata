import pandas as pd 
import numpy as np
import plotly.express as px
import streamlit as st
import pydeck as pdk

# Get the dataframe from the home page

if 'divvy' in st.session_state:
    df_divvy = st.session_state['divvy']

    # Get the file name loaded in the home page
    if 'file_name' in st.session_state:
        file_name = st.session_state['file_name']

        st.subheader("🚏 This page give informations about stations traffic in the city of Chicago based on the current dataset 👉🏽 **{}**".format(file_name))

        st.markdown(" ")

        tab1, tab2 = st.tabs(["🔵 Mapping from started station", "🔴 Mapping from ended station"])

        with tab1 :

            total_rides_per_start_station = df_divvy.groupby(["start_lat", "start_lng", "start_station_name"])["ride_id"].count().reset_index()

            st.markdown("- Rides distribution from started station location")

            ch_initial_view = pdk.ViewState(
                latitude=41.85003,
                longitude=-87.65005,
                zoom = 9
                )
            sp_layer = pdk.Layer(
                'ScatterplotLayer',
                data = total_rides_per_start_station[["start_lng", "start_lat"]],
                get_position = ["start_lng", "start_lat"],
                get_color=[0, 0, 255, 140],
                get_radius=40)
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=ch_initial_view,
                layers = [sp_layer],
                tooltip = {
                    "html": "<b>Start Station Name:</b> {start_station_name}",
                    "style": {"color": "white"}
                }
                ))

            st.markdown("____")
            st.write("📌 Comments :")
            st.write("Write your comments here !")

        with tab2 :

            st.markdown("- Rides distribution from ended location")

            total_rides_per_end_station = df_divvy.groupby(["end_lat", "end_lng"])["ride_id"].count().reset_index()

            ch_initial_view = pdk.ViewState(
                latitude=41.85003,
                longitude=-87.65005,
                zoom = 9
                )
            sp_layer = pdk.Layer(
                'ScatterplotLayer',
                data = total_rides_per_end_station[["end_lng", "end_lat"]],
                get_position = ["end_lng", "end_lat"],
                get_fill_color=[200, 30, 0, 160],
                get_radius=40)
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=ch_initial_view,
                layers = [sp_layer]
                ))
            st.markdown("_____")
            st.write("📌 Comments :")
            st.write("Write your comments here !")
else:
    st.markdown("_____")
    st.write("🚨 Data not available. Please check the loading process on the home page.")   

