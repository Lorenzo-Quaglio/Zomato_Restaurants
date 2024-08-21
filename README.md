# Zomato Restaurants
A Comprehensive Data Analysis Project focusing on the Zomato Company's global restaurant distribution.

Zomato API analysis proves invaluable for food enthusiasts seeking to explore the best cuisines worldwide within their budget. This advanced analysis dives deep into Zomato's data across multiple dimensions, providing detailed insights into various restaurant metrics such as quality, reliability, and more.

## Business Challenges
The newly appointed CEO aims to gain deeper insights into the business to make informed strategic decisions and drive the company's growth. To support this objective, a thorough data analysis is essential, along with the creation of dashboards that reflect these insights. This will enable mapping the registered restaurant base and gaining a clear view of business development by leveraging the following information:

### 🔎 Overview
- Number of registered restaurants and their locations
- Number of countries and cities with listings
- Total reviews on the platform
- Variety of cuisine types
- Interactive world map displaying restaurant names, average cost for two, and average review ratings.

### 🌎 Country Overview
- Number of registered restaurants per country
- Number of registered cities per country
- Total reviews per country
- Average meal cost for two people by country.

### 🏪 City Overview
- City in each country with the most restaurants
- Top 10 cities with restaurants rated above 4 stars
- Top 10 cities with restaurants rated below 2.5 stars
- Top 10 cities with the most diverse culinary offerings.

### 🍽️ Cuisine Overview
- Best-rated restaurants in key culinary categories
- Top X restaurants (with interactive filters for number and cuisine types)
- Top 10 best and worst-rated cuisine types.

The challenge is to address these questions and transform the results into dashboards that provide a quick and clear view of the business's progress. The company's data is available on Kaggle (zomato.csv): [Zomato Dataset](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv)

## Data Assumptions
- The business model is assumed to be a marketplace.
- The dataset lacks date information, so temporal analysis is not included.
- Analytical perspectives focused on country, city, and cuisine.

## Solution Strategy
- Analysis began by addressing the CEO's questions, segmented by country, city, and cuisine.
- The following tools were employed:
  - **Jupyter Notebook**: For preliminary analysis and script drafting.
  - **Data Manipulation Libraries**: Pandas and Numpy.
  - **Data Visualization Libraries**: Matplotlib, Plotly, Folium.
  - **Jupyter Lab**: Final Python scripting.
  - **Streamlit and Streamlit Cloud**: For dashboard visualization and production.

## Key Insights
- India leads with the most registered restaurants, likely due to its large population, and dominates in both highest and lowest-rated restaurants.
- Despite having far fewer restaurants than India and the U.S., Brazil stands out for its poorly rated restaurants.
- Restaurants offering 'Japanese' cuisine rank the highest, representing about a quarter of the best-rated culinary experiences.

## Conclusion
The project's goal was to create a visual representation of the data, enabling tracking of the core business characteristics and its geographical distribution.

Zomato Restaurants has a significant global presence, with strongholds in Asia and North America. The platform offers a wide range of culinary diversity, with North Indian cuisine forming a large part of its offerings.

## Next Steps
- Enhance the visualization of results by expanding the tools available through graphing libraries.
- Improve data formatting to allow for more accurate comparisons between restaurants and countries.
- Evaluate the costs and benefits of expanding or reducing culinary diversity, considering meal prices and restaurant ratings.

**Check out the project results here**: https://lorenzo-quaglio-zomato-restaurants.streamlit.app/
