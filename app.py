import streamlit as st
from streamlit_lottie import st_lottie # type: ignore
import json
import os
import pandas as pd
from data_utils import load_and_preprocess_data, DATASET_PATH

# Set page config
st.set_page_config(
    page_title="RECnREV - Car Analysis Dashboard", 
    layout="wide", 
    page_icon="🚗",
    initial_sidebar_state="expanded"
)

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel sky blue color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f0faff;
    --main-accent: #bae6fd;
    --main-accent-dark: #38bdf8;
    --main-card: #e0f2fe;
    --main-hero-gradient: linear-gradient(135deg, #bae6fd 0%, #38bdf8 100%);
    --main-feature-card: #e0f2fe;
    --main-feature-title: #38bdf8;
    --main-stat-number: #38bdf8;
}
body, html, [class*="css"] {
    background: var(--main-bg) !important;
}
.hero-section {
    background: var(--main-hero-gradient) !important;
}
.feature-card, .main-container, .download-section {
    background: var(--main-card) !important;
}
.feature-title {
    color: var(--main-feature-title) !important;
}
.stat-number {
    color: var(--main-stat-number) !important;
}
</style>
''', unsafe_allow_html=True)

# Load data once for the entire app
@st.cache_data
def load_data():
    return load_and_preprocess_data(DATASET_PATH)

# Load the data
try:
    df_cleaned = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar navigation
st.sidebar.title("🚗 RECnREV Dashboard")
st.sidebar.markdown("---")

# Navigation menu
page = st.sidebar.selectbox(
    "Choose a page:",
    [
        "🏠 Home",
        "📊 EDA Analysis", 
        "🔍 Search & Filter",
        "🚙 Car Models Showcase",
        "🔍 Car Comparison",
        "📈 Trends & Insights",
        "📊 Advanced Analytics",
        "🗺️ Geographic Analysis",
        "🤖 Price Prediction",
        "📋 Data Insights",
        "ℹ️ About"
    ]
)

# Load and display Lottie animation
def load_lottie(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

# Display animation at the top of each page
lottie_path = os.path.join("assets", "car_intro.json")
if os.path.exists(lottie_path):
    lottie_car = load_lottie(lottie_path)
    if lottie_car:
        st_lottie(lottie_car, speed=1, loop=True, height=200)

# Page routing
if page == "🏠 Home":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚗 RECnREV</h1>
        <p class="hero-subtitle">Your Ultimate Car Deal Analysis & Recommendation Platform</p>
        <p class="hero-subtitle">Discover insights, trends, and hidden gems in the Indian used car market</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-item"><span class="stat-number">{:,}</span><div class="stat-label">Total Cars</div></div>'.format(len(df_cleaned)), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Unique Models</div></div>'.format(df_cleaned['Car Name'].nunique()), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Avg Price</div></div>'.format(int(df_cleaned['Price'].mean())), unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-item"><span class="stat-number">{}-{}</span><div class="stat-label">Year Range</div></div>'.format(df_cleaned['Year'].min(), df_cleaned['Year'].max()), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # Quick insights
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🎯 Quick Insights</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="feature-description"><b>Top Car Types:</b></div>', unsafe_allow_html=True)
        top_types = df_cleaned['Type'].value_counts().head(5)
        for car_type, count in top_types.items():
            st.write(f"• {car_type}: {count} cars")
    
    with col2:
        st.markdown('<div class="feature-description"><b>Price Ranges:</b></div>', unsafe_allow_html=True)
        price_ranges = df_cleaned.groupby('Type')['Price'].agg(['mean', 'min', 'max']).round(0)
        for car_type, stats in price_ranges.head(5).iterrows():
            st.write(f"• {car_type}: ₹{stats['min']:,.0f} - ₹{stats['max']:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data preview
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📋 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(df_cleaned.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download option
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    csv = df_cleaned.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Full Dataset (CSV)",
        data=csv,
        file_name='recnrev_car_data.csv',
        mime='text/csv'
    )
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📊 EDA Analysis":
    # Import and run EDA page
    from pages.EDA import app as eda_app
    eda_app(df_cleaned)

elif page == "🔍 Search & Filter":
    # Import and run Search page
    from pages.Search import app as search_app
    search_app(df_cleaned)

elif page == "🚙 Car Models Showcase":
    # Import and run ImageGallery (now Car Models Showcase) page
    from pages.ImageGallery import app as showcase_app
    showcase_app(df_cleaned)

elif page == "🔍 Car Comparison":
    # Import and run CarComparison page
    from pages.CarComparison import app as comparison_app
    comparison_app(df_cleaned)

elif page == "📈 Trends & Insights":
    # Import and run Trends page
    from pages.Trends import app as trends_app
    trends_app(df_cleaned)

elif page == "📊 Advanced Analytics":
    # Import and run Advanced Analytics page
    from pages.AdvancedAnalytics import app as analytics_app
    analytics_app(df_cleaned)

elif page == "🗺️ Geographic Analysis":
    # Import and run Geographic Analysis page
    from pages.GeographicAnalysis import app as geo_app
    geo_app(df_cleaned)

elif page == "🤖 Price Prediction":
    # Import and run Price Prediction page
    from pages.PricePrediction import app as prediction_app
    prediction_app(df_cleaned)

elif page == "📋 Data Insights":
    # Import and run Data Insights page
    from pages.DataInsights import app as insights_app
    insights_app(df_cleaned)

elif page == "ℹ️ About":
    # Import and run About page
    from pages.ABOUT import app as about_app
    about_app()

# Footer
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚗 RECnREV - Car Analysis Dashboard | Built with Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
