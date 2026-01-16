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

################################################################
st.title("Divvy 🚲 Trip Exploratory Data Analysis 🎯")
st.subheader('Use this streamlit App to visualize some insights from your Divvy trip dataset !')
st.write(" ")
st.write("💡 You can use your own divvy data source to get an overview of those data. Grab one from Kaggle : https://www.kaggle.com/datasets/raymondmutyaba/divvytripdata")
st.write(" ")


# set file attachment capability
divvy_file = st.file_uploader("Select your local Divvy csv file (default provider)")

# check if the user has provided a file before loading data
if divvy_file is not None :
    df_divvy = load_data(divvy_file)
    file_name = divvy_file.name
else:
    st.markdown("_____")
    st.subheader("👨🏽‍💼 About me !")
    st.write(" ")
    st.markdown("🧠 Skills :")
    st.markdown("📆 Let's talk ! :")
    st.stop()

##############################################################

df_divvy_raw = df_divvy.copy()

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

# Extract month
df_divvy["month"] = pd.to_datetime(df_divvy["started_date"]).dt.month

# Extract month
df_divvy["year"] = pd.to_datetime(df_divvy["started_date"]).dt.year

# Extract ended hour
df_divvy["day_of_week"] = pd.to_datetime(df_divvy["started_at"]).dt.day_of_week

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

# Unité
df_divvy["unit"] = 1

# Create column route
df_divvy["route"] = "From " + df_divvy["start_station_name"] + " To " + df_divvy["end_station_name"]

month = df_divvy["month"].unique()
year = df_divvy["year"].unique()


###############################################################################


# web page section
raw_rows, raw_cols = df_divvy_raw.shape
clean_rows, clean_cols = df_divvy.shape

# Compute delta 
delta_rows = round(((clean_rows-raw_rows)/raw_rows)*100,2)
delta_cols = round(((clean_cols-raw_cols)/raw_cols)*100,2)

st.markdown("______")

st.badge("📌 Dataframe shape before cleaning")
col1, col2 = st.columns(2)
col1.metric(label="Total rows", value=raw_rows, height='stretch', border=True)
col2.metric(label="Total columns", value=raw_cols, height='stretch', border=True)
st.write(" ")

st.badge("📌 Dataframe shape after cleaning", color="green")
col3, col4 = st.columns(2)
col3.metric(label="Total rows", value=clean_rows, height='stretch', border=True, delta=delta_rows)
col4.metric(label="Total columns", value=clean_cols, height='stretch', border=True, delta=delta_cols)

# store the final dataframe df_divvy in session
st.session_state['divvy'] = df_divvy
st.session_state['file_name'] = divvy_file.name

# about me section
st.markdown("_____")
st.subheader("👨🏽‍💼 About me !")
st.write(" ")
st.markdown("🧠 Skills :")
st.markdown("📆 Let's talk ! :")


