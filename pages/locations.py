import pandas as pd 
import numpy as np
import plotly.express as px
import streamlit as st
import pydeck as pdk

st.title("🚕 Divvy Trip Exploratory Data Analysis")
st.markdown("______")
st.write("This app give some insights in the divvy bikesharing dadaset! in november 2020")
st.markdown(" ")

##### create load data function
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

# set url
url = "data/202011-divvy-tripdata.csv"
# call function
df_divvy = load_data(url)

###### Data wrangling step

# fill unknown start station name
df_divvy["start_station_name"].fillna('Unknown_start', inplace=True)

# fill unknown end station name
df_divvy["end_station_name"].fillna('Unknown_end', inplace=True)

# Fill unknown id by 0
df_divvy["start_station_id"].fillna(0, inplace=True)
df_divvy["end_station_id"].fillna(0, inplace=True)

# Keep columns without end and start station id
df_divvy = df_divvy[
    ['ride_id', 'rideable_type', 'started_at', 'ended_at',
       'start_station_name', 'end_station_name','start_lat', 
       'start_lng', 'end_lat', 'end_lng', 'member_casual']
]

# Convert start time and end time to datetime64
df_divvy["started_at"] = pd.to_datetime(df_divvy["started_at"])
df_divvy["ended_at"] = pd.to_datetime(df_divvy["ended_at"])

# Get only data where ended_at is greater or equal to started_at
df_divvy = df_divvy[(df_divvy["ended_at"] > df_divvy["started_at"]) & (df_divvy["start_station_name"]!="Unknown_start") & (df_divvy["end_station_name"]!="Unknown_end")]

# Compute duration
df_divvy["duration"] = df_divvy["ended_at"] - df_divvy["started_at"]

# Extract started date
df_divvy["started_date"] = pd.to_datetime(df_divvy["started_at"]).dt.date

# Extract started time
df_divvy["started_time"] = pd.to_datetime(df_divvy["started_at"]).dt.time

# Extract started hour
df_divvy["started_hour"] = pd.to_datetime(df_divvy["started_at"]).dt.hour

# Extract ended date
df_divvy["ended_date"] = pd.to_datetime(df_divvy["ended_at"]).dt.date

# Extract ended time
df_divvy["ended_time"] = pd.to_datetime(df_divvy["ended_at"]).dt.time

# Extract ended hour
df_divvy["ended_hour"] = pd.to_datetime(df_divvy["ended_at"]).dt.hour

# Compute minute column
df_divvy["duration_min"] = round(df_divvy["duration"].dt.total_seconds()/60, 2)

# Compute hour column
df_divvy["duration_hour"] = round(df_divvy["duration"].dt.total_seconds()/3600, 2)


##### Deal with Outliers Step

# Compute the quantiles and iqr

# get q1
q1 = df_divvy["duration_min"].quantile(.25)

# get q3
q3 = df_divvy["duration_min"].quantile(.75)

# get iqr
iqr = q3 - q1

# get lower bound
lower_dur = q1 - 1 * iqr

# get upper bound
upper_dur = q3 + 1 * iqr

# Apply interquantile to duration_min column
df_divvy= df_divvy[(df_divvy["duration_min"]>= lower_dur) & (df_divvy["duration_min"]<= upper_dur)]

#### plotting with Pydeck

tab1, tab2 = st.tabs(["🔵 Start Station Section", "🔴 End Station Section"])

with tab1 :

    total_rides_per_start_station = df_divvy.groupby(["start_lat", "start_lng", "start_station_name"])["ride_id"].count().reset_index()

    st.markdown("- Rides distribution by Start Station Location")

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

with tab2 :

    st.markdown("- Rides distribution by End Station Location")

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