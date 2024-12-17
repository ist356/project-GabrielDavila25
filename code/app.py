import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from nasa_api import NasaAPI

# Initialize session state
if 'api' not in st.session_state:
    st.session_state.api = None

def init_api():
    """Initialize the NASA API with the provided key"""
    api_key = st.secrets["nasa_api_key"]
    st.session_state.api = NasaAPI(api_key)

def create_asteroid_scatter(df):
    """Create a scatter plot of asteroids"""
    fig = px.scatter(df, 
                    x='miss_distance_km', 
                    y='diameter_max_km',
                    color='is_potentially_hazardous',
                    hover_data=['name', 'close_approach_date', 'relative_velocity_kph'],
                    title='Asteroid Close Approaches',
                    labels={
                        'miss_distance_km': 'Miss Distance (km)',
                        'diameter_max_km': 'Maximum Diameter (km)',
                        'is_potentially_hazardous': 'Potentially Hazardous'
                    })
    return fig

def create_velocity_histogram(df):
    """Create a histogram of asteroid velocities"""
    fig = px.histogram(df, 
                      x='relative_velocity_kph',
                      title='Distribution of Asteroid Velocities',
                      labels={'relative_velocity_kph': 'Relative Velocity (km/h)'})
    return fig

st.title('🌠 Near Earth Objects Explorer')
st.write('Explore near-Earth asteroids using NASA\'s NeoWs API')

# Initialize API if not already done
if st.session_state.api is None:
    try:
        init_api()
    except Exception as e:
        st.error(f"Failed to initialize API: {str(e)}")
        st.stop()

# Create tabs for different features
tab1, tab2, tab3 = st.tabs(["Search by Date", "Lookup Asteroid", "Browse Asteroids"])

with tab1:
    st.header("Search Asteroids by Date Range")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                 datetime.now().date(),
                                 max_value=datetime.now().date())
    with col2:
        end_date = st.date_input("End Date", 
                               min_value=start_date,
                               max_value=start_date + timedelta(days=7),
                               value=start_date + timedelta(days=7))
    
    if st.button("Search"):
        with st.spinner("Fetching asteroid data..."):
            try:
                df = st.session_state.api.get_feed(start_date.strftime('%Y-%m-%d'), 
                                                 end_date.strftime('%Y-%m-%d'))
                
                # Display summary statistics
                st.subheader("Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Asteroids", len(df))
                with col2:
                    st.metric("Potentially Hazardous", 
                             df['is_potentially_hazardous'].sum())
                with col3:
                    st.metric("Average Size (km)", 
                             f"{df['diameter_max_km'].mean():.2f}")
                
                # Display visualizations
                st.plotly_chart(create_asteroid_scatter(df))
                st.plotly_chart(create_velocity_histogram(df))
                
                # Display raw data
                st.subheader("Detailed Data")
                st.dataframe(df)
                
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")

with tab2:
    st.header("Lookup Asteroid by ID")
    asteroid_id = st.text_input("Enter NASA JPL Asteroid ID")
    
    if asteroid_id and st.button("Look Up"):
        with st.spinner("Fetching asteroid details..."):
            try:
                asteroid = st.session_state.api.get_asteroid(asteroid_id)
                
                # Display asteroid information
                st.json(asteroid)
                
            except Exception as e:
                st.error(f"Error looking up asteroid: {str(e)}")

with tab3:
    st.header("Browse All Asteroids")
    
    if st.button("Load Asteroids"):
        with st.spinner("Loading asteroid database..."):
            try:
                df = st.session_state.api.browse_asteroids()
                
                # Add filters
                st.subheader("Filters")
                hazardous = st.checkbox("Show only potentially hazardous asteroids")
                min_size = st.slider("Minimum diameter (km)", 
                                   float(df['diameter_min_km'].min()),
                                   float(df['diameter_max_km'].max()),
                                   float(df['diameter_min_km'].min()))
                
                # Apply filters
                if hazardous:
                    df = df[df['is_potentially_hazardous']]
                df = df[df['diameter_min_km'] >= min_size]
                
                # Display filtered data
                st.subheader(f"Showing {len(df)} asteroids")
                st.dataframe(df)
                
            except Exception as e:
                st.error(f"Error browsing asteroids: {str(e)}")

st.sidebar.markdown("""
## About
This application uses NASA's Near Earth Object Web Service (NeoWs) to explore data 
about asteroids that pass close to Earth.

### Features:
- Search asteroids by date range
- Look up specific asteroids by ID
- Browse the complete asteroid database
""")
