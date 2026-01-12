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

# Extract ended day of week
df_divvy["day_of_week"] = pd.to_datetime(df_divvy["ended_at"]).dt.day_of_week

# Compute minute column
df_divvy["duration_min"] = round(df_divvy["duration"].dt.total_seconds()/60, 0)

# Compute hour column
df_divvy["duration_hour"] = round(df_divvy["duration"].dt.total_seconds()/3600, 0)


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

##### subsetting

started_date = df_divvy.groupby(["started_date", "rideable_type"])["ride_id"].count().reset_index()
fig = px.area(data_frame=started_date, x="started_date", y="ride_id", color="rideable_type")
st.plotly_chart(figure_or_data=fig)
st.markdown("____")

day_of_week = df_divvy.groupby(["day_of_week", "rideable_type"])["ride_id"].count().reset_index()
fig = px.bar(data_frame=day_of_week, y="day_of_week", x="ride_id", color="rideable_type", orientation='h')
st.plotly_chart(figure_or_data=fig)
st.markdown("_____")

rideable_type = df_divvy.groupby(["started_hour", "rideable_type"])["ride_id"].count().reset_index()
fig = px.area(data_frame=rideable_type, x="started_hour", y="ride_id", color="rideable_type")
st.plotly_chart(figure_or_data=fig)

st.markdown("_____")

duration_min= df_divvy.groupby(["duration_min", "rideable_type"])["ride_id"].count().reset_index()
fig = px.area(data_frame=duration_min, x="duration_min", y="ride_id", color="rideable_type")
st.plotly_chart(figure_or_data=fig)

