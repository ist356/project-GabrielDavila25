# About My Project

Student Name: Gabriel Davila
Student Email: gdavila@syr.edu

### What it does

This project is a Near Earth Objects (NEO) Explorer that uses NASA's NeoWs (Near Earth Object Web Service) API to visualize and analyze data about asteroids that pass close to Earth. The application provides three main features:

1. **Search by Date Range**: 
   - Users can select a date range (up to 7 days)
   - Displays interactive visualizations including:
     - Scatter plot of asteroid size vs. miss distance
     - Histogram of asteroid velocities
   - Shows summary statistics and detailed data table

2. **Asteroid Lookup**: 
   - Search for specific asteroids using their NASA JPL ID
   - View detailed information about individual asteroids

3. **Browse Asteroids**: 
   - Access the complete database of known near-Earth asteroids
   - Filter asteroids by:
     - Potentially hazardous status
     - Minimum diameter
   - View filtered results in an interactive table

### How you run my project

1. Install required dependencies:
```bash
pip install streamlit pandas plotly requests
```

2. Set up your NASA API key:
   - Create a `.streamlit/secrets.toml` file in the project root
   - Add your NASA API key:
     ```toml
     nasa_api_key = "8HPJyy7XR3RJXQoDeW01RSQwGbaXxbUlcaUKDd9k"
     ```

3. Run the Streamlit application:
```bash
cd code
streamlit run app.py
```

4. The application will open in your default web browser

### Other things you need to know

- The date range search is limited to 7 days due to NASA API restrictions
- The browse feature might take a moment to load as it fetches the complete asteroid database
- All data is fetched in real-time from NASA's API
- The cache folder stores temporary data files for better performance
- The application includes error handling for API failures and invalid inputs
