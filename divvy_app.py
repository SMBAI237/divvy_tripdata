import streamlit as st

# Create the navigation page

pages = [
    st.Page("pages/home.py", title="Home", icon="🛖"),
    st.Page("pages/metrics.py", title="Metrics", icon="📊"),
    st.Page("pages/rides.py", title="Rides", icon="🚲"),
    st.Page("pages/locations.py", title="Stations", icon="🏪"),
    st.Page("pages/celebrate.py", title="Celebrate", icon="🎈")
]

# Adding pages to the sidebar navigation
pg = st.navigation(pages, position="sidebar", expanded=True)

# Run the App
pg.run()