import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel slate/gray color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f7fafc;
    --main-accent: #cbd5e1;
    --main-accent-dark: #64748b;
    --main-card: #e2e8f0;
    --main-hero-gradient: linear-gradient(135deg, #cbd5e1 0%, #64748b 100%);
    --main-feature-card: #e2e8f0;
    --main-feature-title: #64748b;
    --main-stat-number: #64748b;
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
        <h1 class="hero-title">📋 Data Insights</h1>
        <p class="hero-subtitle">Comprehensive overview of the dataset, data quality, and key insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Dataset overview
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-item"><span class="stat-number">{:,}</span><div class="stat-label">Total Records</div></div>'.format(len(df_cleaned)), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Unique Car Models</div></div>'.format(df_cleaned['Car Name'].nunique()), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Date Range</div></div>'.format(f"{df_cleaned['Year'].min()}-{df_cleaned['Year'].max()}"), unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Price Range</div></div>'.format(int(df_cleaned['Price'].max())), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Data quality assessment
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🔍 Data Quality Assessment</div>', unsafe_allow_html=True)
    
    # Missing values analysis
    missing_data = df_cleaned.isnull().sum()
    missing_percentage = (missing_data / len(df_cleaned)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing Count': missing_data.values,
        'Missing Percentage': missing_percentage.values
    }).sort_values('Missing Count', ascending=False)
    
    st.markdown('<div class="feature-title">Missing Values Analysis</div>', unsafe_allow_html=True)
    st.dataframe(missing_df, use_container_width=True)
    
    # Data completeness chart
    completeness = ((len(df_cleaned) - missing_data) / len(df_cleaned)) * 100
    fig = px.bar(
        x=completeness.index,
        y=completeness.values,
        title="Data Completeness by Column (%)",
        labels={'x': 'Columns', 'y': 'Completeness (%)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Key insights tabs
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">💡 Key Insights</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Price Analysis", "Market Composition", "Trends", "Recommendations"])
    
    with tab1:
        # Price statistics
        price_stats = df_cleaned['Price'].describe()
        st.markdown('<div class="feature-title">Price Statistics</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Mean</div></div>'.format(int(price_stats['mean'])), unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Median</div></div>'.format(int(price_stats['50%'])), unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Min</div></div>'.format(int(price_stats['min'])), unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Max</div></div>'.format(int(price_stats['max'])), unsafe_allow_html=True)
        
        # Price distribution
        fig = px.histogram(
            df_cleaned,
            x='Price',
            nbins=50,
            title="Price Distribution",
            labels={'Price': 'Price (₹)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Price by car type
        avg_price_by_type = df_cleaned.groupby('Type')['Price'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=avg_price_by_type.index,
            y=avg_price_by_type.values,
            title="Average Price by Car Type",
            labels={'x': 'Car Type', 'y': 'Average Price (₹)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Price by fuel type
        avg_price_by_fuel = df_cleaned.groupby('Fuel')['Price'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=avg_price_by_fuel.index,
            y=avg_price_by_fuel.values,
            title="Average Price by Fuel Type",
            labels={'x': 'Fuel Type', 'y': 'Average Price (₹)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Price by owner
        avg_price_by_owner = df_cleaned.groupby('Owner')['Price'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=avg_price_by_owner.index,
            y=avg_price_by_owner.values,
            title="Average Price by Number of Owners",
            labels={'x': 'Number of Owners', 'y': 'Average Price (₹)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Market composition
        st.markdown('<div class="feature-title">Market Composition</div>', unsafe_allow_html=True)
        
        # Car type distribution
        type_counts = df_cleaned['Type'].value_counts()
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Distribution of Car Types"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Fuel type distribution
        fuel_counts = df_cleaned['Fuel'].value_counts()
        fig = px.pie(
            values=fuel_counts.values,
            names=fuel_counts.index,
            title="Distribution of Fuel Types"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Transmission distribution
        drive_counts = df_cleaned['Drive'].value_counts()
        fig = px.pie(
            values=drive_counts.values,
            names=drive_counts.index,
            title="Distribution of Transmission Types"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Owner distribution
        owner_counts = df_cleaned['Owner'].value_counts()
        fig = px.pie(
            values=owner_counts.values,
            names=owner_counts.index,
            title="Distribution by Number of Previous Owners"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Trends analysis
        st.markdown('<div class="feature-title">Market Trends</div>', unsafe_allow_html=True)
        
        # Price trends by year
        yearly_avg_price = df_cleaned.groupby('Year')['Price'].mean()
        fig = px.line(
            x=yearly_avg_price.index,
            y=yearly_avg_price.values,
            title="Average Price Trends by Year",
            labels={'x': 'Year', 'y': 'Average Price (₹)'},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Distance vs Price relationship
        fig = px.scatter(
            df_cleaned,
            x='Distance',
            y='Price',
            color='Type',
            hover_data=['Car Name', 'Year', 'Fuel'],
            title="Distance vs Price Relationship",
            labels={'Distance': 'Distance (km)', 'Price': 'Price (₹)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Car age distribution
        df_cleaned['Car Age'] = 2024 - df_cleaned['Year']
        fig = px.histogram(
            df_cleaned,
            x='Car Age',
            nbins=20,
            title="Car Age Distribution",
            labels={'Car Age': 'Car Age (years)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Recommendations
        st.markdown('<div class="feature-title">Recommendations</div>', unsafe_allow_html=True)
        
        # For buyers
        st.markdown('<div class="feature-description"><b>For Buyers:</b></div>', unsafe_allow_html=True)
        
        # Best value cars (low price, good condition)
        best_value = df_cleaned[
            (df_cleaned['Price'] <= df_cleaned['Price'].quantile(0.3)) &
            (df_cleaned['Car Age'] <= 5)
        ]['Car Name'].value_counts().head(5)
        
        st.write("**Best Value Options:**")
        for car, count in best_value.items():
            avg_price = df_cleaned[df_cleaned['Car Name'] == car]['Price'].mean()
            st.write(f"• {car}: ₹{avg_price:,.0f} avg ({count} listings)")
        
        # Popular models
        popular_models = df_cleaned['Car Name'].value_counts().head(5)
        st.write("**Most Popular Models:**")
        for car, count in popular_models.items():
            avg_price = df_cleaned[df_cleaned['Car Name'] == car]['Price'].mean()
            st.write(f"• {car}: {count} listings, ₹{avg_price:,.0f} avg")
        
        # For sellers
        st.markdown('<div class="feature-description"><b>For Sellers:</b></div>', unsafe_allow_html=True)
        
        # Optimal selling time
        optimal_years = df_cleaned.groupby('Year')['Price'].mean().sort_values(ascending=False).head(3)
        st.write("**Best Years to Sell:**")
        for year, avg_price in optimal_years.items():
            st.write(f"• {year}: ₹{avg_price:,.0f} avg price")
        
        # Competitive pricing
        price_quartiles = df_cleaned['Price'].quantile([0.25, 0.5, 0.75])
        st.write("**Competitive Price Ranges:**")
        st.write(f"• Budget: ₹{price_quartiles[0.25]:,.0f} - ₹{price_quartiles[0.5]:,.0f}")
        st.write(f"• Mid-range: ₹{price_quartiles[0.5]:,.0f} - ₹{price_quartiles[0.75]:,.0f}")
        st.write(f"• Premium: Above ₹{price_quartiles[0.75]:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Data summary
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📊 Data Summary</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="feature-title">Numerical Variables</div>', unsafe_allow_html=True)
        numerical_summary = df_cleaned.select_dtypes(include=[np.number]).describe()
        st.dataframe(numerical_summary)
    
    with col2:
        st.markdown('<div class="feature-title">Categorical Variables</div>', unsafe_allow_html=True)
        categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            st.write(f"**{col}:** {df_cleaned[col].nunique()} unique values")
            top_values = df_cleaned[col].value_counts().head(3)
            for value, count in top_values.items():
                st.write(f"  - {value}: {count}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Data insights analysis completed! Explore the tabs above for detailed information. 📋")

# Call the app function
app() 