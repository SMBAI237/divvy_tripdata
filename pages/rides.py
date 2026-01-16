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

        st.subheader("📊 This page gives some visualizations about rides based on the current dataset 👉🏽 **{}**".format(file_name))

        ##### subsetting

        started_date = df_divvy.groupby(["started_date", "rideable_type"])["ride_id"].count().reset_index()
        fig = px.area(data_frame=started_date, x="started_date", y="ride_id", color="rideable_type")
        st.plotly_chart(figure_or_data=fig)
        st.markdown("____")

        day_of_week = df_divvy.groupby(["day_of_week", "rideable_type"])["ride_id"].count().reset_index()
        fig = px.bar(data_frame=day_of_week, y="day_of_week", x="ride_id", color="rideable_type", orientation='h')
        fig.update_layout(barmode='stack')
        st.plotly_chart(figure_or_data=fig)
        st.markdown("_____")

        rideable_type = df_divvy.groupby(["started_hour", "rideable_type"])["ride_id"].count().reset_index()
        fig = px.area(data_frame=rideable_type, x="started_hour", y="ride_id", color="rideable_type")
        st.plotly_chart(figure_or_data=fig)

        st.markdown("_____")

        # Get top 10 route
        top_route = df_divvy.groupby("route")["unit"].sum().nlargest(10).sort_values().reset_index()
        fig = px.bar(data_frame=top_route, y="route", x="unit", orientation='h')
        fig.update_layout(barmode='stack')
        st.plotly_chart(figure_or_data=fig)

        st.markdown("_____")

        duration_min= df_divvy.groupby(["duration_min", "rideable_type"])["ride_id"].count().reset_index()
        fig = px.area(data_frame=duration_min, x="duration_min", y="ride_id", color="rideable_type")
        st.plotly_chart(figure_or_data=fig)

else:
    st.markdown("_____")
    st.write("🚨 Data not available. Please check the loading process on the home page.")   
