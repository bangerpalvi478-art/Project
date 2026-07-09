# 🚗 RECnREV - Car Analysis Dashboard

A comprehensive Streamlit-based dashboard for analyzing used car market data with interactive visualizations and insights.

## ✨ Features

### 🏠 Home Page
- **Dashboard Overview**: Key metrics and statistics
- **Quick Insights**: Top car types and price ranges
- **Data Preview**: Sample of the dataset
- **Download Options**: Export cleaned data

### 📊 EDA Analysis
- **Interactive Charts**: Sunburst, scatter plots, treemaps
- **Animated Visualizations**: Price vs distance by year
- **Statistical Analysis**: Price distributions by fuel type
- **Market Insights**: Car type and transmission analysis

### 🔍 Search & Filter
- **Advanced Filtering**: By car type, fuel, price range, year
- **Text Search**: Search by car name
- **Real-time Results**: Dynamic filtering with live updates
- **Visual Feedback**: Charts for filtered results

### 🚙 Car Models Showcase (Enhanced ImageGallery)
- **Interactive Filters**: Sidebar filters for car type, fuel, price, year
- **Model Statistics**: Detailed information for each car model
- **Price Analysis**: Distribution charts for each model
- **Comparative Charts**: Price trends, fuel comparison, year analysis
- **Data Export**: Download filtered results

### 🔍 Car Comparison Tool (New)
- **Side-by-Side Comparison**: Compare up to 4 car models
- **Detailed Metrics**: Price ranges, average distance, year statistics
- **Visual Analysis**: Box plots, violin plots, histograms
- **Smart Recommendations**: Similar cars based on price range
- **Export Options**: Download comparison data

### 📈 Trends & Insights
- **Market Trends**: Price trends by year
- **Animated Charts**: Interactive visualizations
- **Statistical Analysis**: Comprehensive market insights
- **Filtered Views**: Customizable analysis

### 📊 Advanced Analytics
- **Correlation Analysis**: Feature relationships and correlations
- **Statistical Tests**: T-tests and hypothesis testing
- **Price Prediction Factors**: Feature importance analysis
- **Market Segmentation**: Customer and price segmentation
- **Anomaly Detection**: Outlier identification and analysis

### 🗺️ Geographic Analysis
- **Regional Price Analysis**: Price variations by location
- **Market Composition**: Regional car type and fuel distribution
- **Location-based Trends**: Price trends by state/region
- **Regional Insights**: Best value and premium markets
- **State-wise Analysis**: Detailed analysis by location

### 🤖 Price Prediction
- **Machine Learning Models**: Random Forest and Linear Regression
- **Interactive Prediction**: Real-time price predictions
- **Model Performance**: Accuracy metrics and comparisons
- **Feature Importance**: Key factors affecting prices
- **Confidence Intervals**: Price range predictions

### 📋 Data Insights
- **Comprehensive Summary**: Complete dataset overview
- **Data Quality Assessment**: Missing values and completeness
- **Key Findings**: Actionable insights and recommendations
- **Statistical Summary**: Detailed statistical analysis
- **Market Intelligence**: Buyer and seller recommendations

## 🚀 Getting Started

### Prerequisites
```bash
pip install streamlit pandas plotly streamlit-lottie
```

### Installation
1. Clone the repository
2. Install dependencies
3. Ensure the `cars_24_combined.csv` file is in the root directory
4. Run the application

### Running the App
```bash
streamlit run app.py
```

## 📁 Project Structure

```
index/
├── app.py                 # Main application file
├── data_utils.py          # Data loading and preprocessing
├── cars_24_combined.csv   # Dataset
├── assets/
│   ├── car_intro.json     # Lottie animation
│   └── global_styles.css  # Custom styles
└── pages/
    ├── Home.py           # Home page (integrated in app.py)
    ├── EDA.py            # Exploratory Data Analysis
    ├── Search.py         # Search and filter functionality
    ├── ImageGallery.py   # Car Models Showcase (enhanced)
    ├── CarComparison.py  # Car comparison tool (new)
    ├── Trends.py         # Market trends and insights
    └── ABOUT.py          # About page
```

## 🔧 Key Improvements Made

### 1. Enhanced ImageGallery → Car Models Showcase
- **Before**: Basic image display with static files
- **After**: Data-driven car model showcase with:
  - Interactive filters
  - Detailed statistics
  - Price analysis charts
  - Comparative visualizations

### 2. New Car Comparison Tool
- **Side-by-side comparison** of up to 4 car models
- **Comprehensive metrics** for each model
- **Visual analysis** with multiple chart types
- **Smart recommendations** for similar cars
- **Export functionality** for comparison data

### 3. Improved Navigation
- **Unified sidebar navigation** across all pages
- **Consistent styling** and user experience
- **Better page organization** with clear icons

### 4. Enhanced Data Handling
- **Centralized data loading** with caching
- **Consistent data preprocessing** across pages
- **Error handling** for missing data

## 📊 Dataset Information

The dashboard uses a comprehensive dataset with the following columns:
- **Car Name**: Model of the car
- **Year**: Manufacturing year
- **Distance**: Kilometers driven
- **Owner**: Number of previous owners
- **Fuel**: Fuel type (Petrol, Diesel, CNG, etc.)
- **Location**: RTO location
- **Drive**: Transmission type (Manual, Automatic)
- **Type**: Car category (SUV, Sedan, Hatchback, etc.)
- **Price**: Selling price in INR

## 🎯 Use Cases

### For Car Buyers
- **Market Research**: Understand price trends and market conditions
- **Model Comparison**: Compare different car models side by side
- **Price Analysis**: Find fair market prices for specific models
- **Filtered Search**: Find cars matching specific criteria

### For Car Sellers
- **Price Setting**: Understand market prices for similar cars
- **Market Trends**: Identify optimal selling times
- **Competitive Analysis**: Compare with similar listings

### For Data Analysts
- **Market Insights**: Analyze trends and patterns
- **Statistical Analysis**: Comprehensive data exploration
- **Data Export**: Download filtered datasets for further analysis

## 🔮 Future Enhancements

- **Machine Learning Integration**: Price prediction models
- **User Authentication**: Personalized experiences
- **Advanced Analytics**: More sophisticated statistical analysis
- **Real-time Data**: Live market data integration
- **Mobile Optimization**: Better mobile experience

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding new visualizations

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit, Plotly, and Pandas** 