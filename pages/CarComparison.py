import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel red/coral color scheme
st.markdown('''
<style>
:root {
    --main-bg: #fff6f6;
    --main-accent: #ffb3b3;
    --main-accent-dark: #ff6f61;
    --main-card: #ffeaea;
    --main-hero-gradient: linear-gradient(135deg, #ffb3b3 0%, #ff6f61 100%);
    --main-feature-card: #ffeaea;
    --main-feature-title: #ff6f61;
    --main-stat-number: #ff6f61;
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

# Load data for this page
df_cleaned = load_and_preprocess_data(DATASET_PATH)

def app(df_cleaned=None):
    if df_cleaned is None:
        df_cleaned = load_and_preprocess_data(DATASET_PATH)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🔍 Car Comparison Tool</h1>
        <p class="hero-subtitle">Compare up to 4 car models side-by-side with detailed analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    # Car selection
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🚗 Select Cars to Compare</div>', unsafe_allow_html=True)
    
    # Get unique car models
    car_models = sorted(df_cleaned['Car Name'].unique())
    selected_cars = st.multiselect(
        "Choose cars to compare (max 4):",
        car_models,
        max_selections=4
    )
    
    if not selected_cars:
        st.markdown('<div class="feature-description">💡 <b>Popular suggestions:</b></div>', unsafe_allow_html=True)
        popular_cars = df_cleaned['Car Name'].value_counts().head(8).index.tolist()
        st.write(", ".join(popular_cars))
    st.markdown('</div>', unsafe_allow_html=True)

    if selected_cars:
        # Filter data for selected cars
        comparison_df = df_cleaned[df_cleaned['Car Name'].isin(selected_cars)]
        
        # Overview metrics
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">📊 Comparison Overview</div>', unsafe_allow_html=True)
        
        # Display key metrics for each car
        cols = st.columns(len(selected_cars))
        for i, car in enumerate(selected_cars):
            car_data = comparison_df[comparison_df['Car Name'] == car]
            with cols[i]:
                st.markdown(f'<div class="stat-item"><span class="stat-number">{car}</span><div class="stat-label">Model</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="stat-item"><span class="stat-number">₹{car_data["Price"].mean():,.0f}</span><div class="stat-label">Avg Price</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="stat-item"><span class="stat-number">{len(car_data)}</span><div class="stat-label">Listings</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="stat-item"><span class="stat-number">{car_data["Year"].mean():.0f}</span><div class="stat-label">Avg Year</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # Detailed analysis tabs
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">📈 Detailed Analysis</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Price Analysis", "Year & Distance", "Fuel & Transmission", "Raw Data"])
        
        with tab1:
            # Price distribution comparison
            fig = px.box(
                comparison_df,
                x='Car Name',
                y='Price',
                color='Car Name',
                title="Price Distribution Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Violin plot for price distribution
            fig = px.violin(
                comparison_df,
                x='Car Name',
                y='Price',
                color='Car Name',
                box=True,
                points='all',
                title="Price Distribution (Violin Plot)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Year distribution
            fig = px.histogram(
                comparison_df,
                x='Year',
                color='Car Name',
                barmode='overlay',
                opacity=0.7,
                title="Year Distribution Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Distance vs Price scatter
            fig = px.scatter(
                comparison_df,
                x='Distance',
                y='Price',
                color='Car Name',
                hover_data=['Year', 'Fuel', 'Drive'],
                title="Distance vs Price by Car Model"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Fuel type distribution
            fuel_counts = comparison_df.groupby(['Car Name', 'Fuel']).size().reset_index(name='Count')
            fig = px.bar(
                fuel_counts,
                x='Car Name',
                y='Count',
                color='Fuel',
                title="Fuel Type Distribution by Car Model"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Transmission distribution
            drive_counts = comparison_df.groupby(['Car Name', 'Drive']).size().reset_index(name='Count')
            fig = px.bar(
                drive_counts,
                x='Car Name',
                y='Count',
                color='Drive',
                title="Transmission Distribution by Car Model"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Raw data table
            st.dataframe(comparison_df, use_container_width=True)
            
            # Download comparison data
            csv = comparison_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Comparison Data (CSV)",
                data=csv,
                file_name=f'car_comparison_{"_".join(selected_cars[:2])}.csv',
                mime='text/csv'
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Smart recommendations
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🤖 Smart Recommendations</div>', unsafe_allow_html=True)
        
        # Find similar cars based on price range
        avg_price = comparison_df['Price'].mean()
        price_range = (avg_price * 0.8, avg_price * 1.2)
        
        similar_cars = df_cleaned[
            (df_cleaned['Price'] >= price_range[0]) & 
            (df_cleaned['Price'] <= price_range[1]) &
            (~df_cleaned['Car Name'].isin(selected_cars))
        ]['Car Name'].value_counts().head(5)
        
        st.markdown(f'<div class="feature-description">💡 <b>Similar cars in price range ₹{price_range[0]:,.0f} - ₹{price_range[1]:,.0f}:</b></div>', unsafe_allow_html=True)
        for car, count in similar_cars.items():
            st.write(f"• {car} ({count} listings)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Select cars above to start your comparison! 🚗")

# Call the app function
app() 