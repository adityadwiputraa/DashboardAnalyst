import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# Title of the dashboard
st.title("Bike Sharing Analysis Dashboard")
st.markdown("### Insights from the Bike Sharing Dataset")

# Upload the data files
st.sidebar.header("Upload Data")
day_file = st.sidebar.file_uploader("day.csv", type=['csv'])
hour_file = st.sidebar.file_uploader("hour.csv", type=['csv'])

if day_file is not None and hour_file is not None:
    # Load the datasets
    day_df = pd.read_csv(day_file)
    hour_df = pd.read_csv(hour_file)
    
    st.sidebar.success("Files successfully uploaded!")
    
    # Data Preview
    st.subheader("Day Dataset Preview")
    st.dataframe(day_df.head())
    
    st.subheader("Hour Dataset Preview")
    st.dataframe(hour_df.head())
    
    # Exploratory Data Analysis
    st.markdown("### Exploratory Data Analysis")
    st.markdown("#### Rentals Over Time (Day)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=day_df, x="dteday", y="cnt", ax=ax)
    ax.set_title("Daily Rentals Over Time")
    st.pyplot(fig)
    
    # Clustering Analysis (Manual Grouping)
    st.markdown("#### Rentals by Weekday Group (Manual Grouping)")
    day_df['group'] = day_df['weekday'].apply(
        lambda x: 'Weekend' if x in [0, 6] else 'Weekday'
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="group", y="cnt", data=day_df, ci=None, ax=ax)
    ax.set_title("Average Rentals: Weekday vs Weekend")
    st.pyplot(fig)
    
    # Geospatial Analysis
    st.markdown("### Geospatial Analysis")
    st.markdown("#### Sample Location Data for Visualization")
    sample_data = {
        'location': ['Station A', 'Station B', 'Station C'],
        'lat': [37.7749, 37.7849, 37.7949],
        'lon': [-122.4194, -122.4094, -122.3994],
        'rentals': [150, 200, 250]
    }
    geo_df = pd.DataFrame(sample_data)
    
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
    for _, row in geo_df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"{row['location']} - Rentals: {row['rentals']}"
        ).add_to(m)
    st_folium(m, width=700)
    
    # RFM Analysis
    st.markdown("### RFM Analysis")
    st.markdown("#### Recency, Frequency, and Monetary Values")
    day_df['recency'] = (pd.to_datetime(day_df['dteday']).max() - pd.to_datetime(day_df['dteday'])).dt.days
    day_df['frequency'] = day_df['registered']
    day_df['monetary'] = day_df['cnt']
    day_df['R_Score'] = pd.qcut(day_df['recency'], 4, labels=[4, 3, 2, 1])
    day_df['F_Score'] = pd.qcut(day_df['frequency'], 4, labels=[1, 2, 3, 4])
    day_df['M_Score'] = pd.qcut(day_df['monetary'], 4, labels=[1, 2, 3, 4])
    day_df['RFM_Score'] = day_df[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)
    st.dataframe(day_df[['recency', 'frequency', 'monetary', 'RFM_Score']].head())
    
else:
    st.warning("Please upload both `day.csv` and `hour.csv` to continue.")
