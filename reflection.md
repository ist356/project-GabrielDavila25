# Project Reflection

### What I Learned

1. **API Integration**
   - Gained experience working with NASA's NeoWs API
   - Learned how to handle API rate limits and error responses
   - Implemented proper API key management using Streamlit secrets

2. **Data Visualization**
   - Used Plotly Express to create interactive visualizations
   - Learned to choose appropriate chart types for different data aspects
   - Implemented responsive layouts that work well with varying data sizes

3. **Testing**
   - Implemented unit tests with mock objects for API calls
   - Learned the importance of testing error cases
   - Used unittest for structured test organization

4. **Streamlit Development**
   - Created a multi-tab interface for different features
   - Implemented session state management
   - Used Streamlit's layout options for responsive design
   - Integrated interactive widgets for user input

5. **Data Processing**
   - Used Pandas for efficient data manipulation
   - Implemented data filtering and aggregation
   - Created summary statistics from raw data

### What I Struggled With

1. **API Limitations**
   - Working with NASA's 7-day limit for date ranges
   - Handling rate limits and API timeouts
   - Managing large data responses efficiently

2. **Testing Challenges**
   - Mocking complex API responses
   - Testing asynchronous operations
   - Ensuring comprehensive test coverage

3. **User Interface Design**
   - Balancing functionality with simplicity
   - Making visualizations responsive
   - Handling edge cases in user input

### What I Would Do With More Time

1. **Additional Features**
   - Add more advanced filtering options
   - Implement data caching for better performance
   - Create comparison views for multiple asteroids
   - Add export functionality for data and visualizations

2. **Enhanced Visualizations**
   - Create 3D visualizations of asteroid orbits
   - Add time-series analysis of asteroid approaches
   - Implement more interactive chart features

3. **Performance Improvements**
   - Implement background data loading
   - Add progressive loading for large datasets
   - Optimize data processing for faster response times

4. **Additional Data Sources**
   - Integrate other NASA APIs
   - Add space weather data
   - Include historical impact data

5. **User Experience**
   - Add user preferences and settings
   - Implement dark/light theme options
   - Add tutorial tooltips for new users
   - Create a mobile-friendly layout

## Reflections

While working on this project, I ran into a few roadblocks—especially with testing. Mocking API responses, especially when they got complex, was trickier than I expected. At one point, I found myself getting lost in the weeds trying to figure out the best way to handle edge cases. But that's okay. These struggles were part of the process, and they taught me to embrace the messiness of debugging and testing. I realized that testing isn’t just about ensuring code works—it’s about anticipating what *could* go wrong and learning how to plan for it.

The challenges with API limitations also tested my patience. Initially, I went through so many project iterations before settling on this version. My first plan was to create a space dashboard, but it came with its own share of struggles—data availability issues, maximizing API calls without hitting limits, and handling massive responses efficiently. I kept running into walls, and at times it felt like I was constantly starting over. Looking back, though, this iterative process really pushed me to think creatively and refine my approach.

Having to constantly work around the 7-day limit and rate throttling forced me to think creatively about data handling. Sure, it was frustrating at times, but it pushed me to focus on efficiency and think about scalable solutions.

Overall, I’m proud of the progress I made. Even though the project isn’t perfect, it’s a solid foundation with room for growth. I learned that it’s okay to struggle as long as you keep moving forward—and I did. With a bit more time, I’d refine the details and tackle those wish-list features, but for now, I’m happy with how much I’ve grown through this experience.

