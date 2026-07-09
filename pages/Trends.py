import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel cyan/blue color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f0fcff;
    --main-accent: #b2f0ff;
    --main-accent-dark: #38bdf8;
    --main-card: #e0f7fa;
    --main-hero-gradient: linear-gradient(135deg, #b2f0ff 0%, #38bdf8 100%);
    --main-feature-card: #e0f7fa;
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

# Load data for this page
df_cleaned = load_and_preprocess_data(DATASET_PATH)

def app(df_cleaned):
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">📈 Trends & Insights</h1>
        <p class="hero-subtitle">Discover market trends, seasonal patterns, and price insights over time.</p>
    </div>
    """, unsafe_allow_html=True)

    # Key trends overview
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate some key trends
    yearly_avg_price = df_cleaned.groupby('Year')['Price'].mean()
    price_trend = (yearly_avg_price.iloc[-1] - yearly_avg_price.iloc[0]) / yearly_avg_price.iloc[0] * 100
    
    with col1:
        st.markdown('<div class="stat-item"><span class="stat-number">{:.1f}%</span><div class="stat-label">Price Trend</div></div>'.format(price_trend), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Years of Data</div></div>'.format(df_cleaned['Year'].nunique()), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Most Popular Year</div></div>'.format(df_cleaned['Year'].mode().iloc[0]), unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Most Popular Type</div></div>'.format(df_cleaned['Type'].mode().iloc[0]), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Price trends over time
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">💰 Price Trends Over Time</div>', unsafe_allow_html=True)
    
    # Average price by year
    yearly_stats = df_cleaned.groupby('Year').agg({
        'Price': ['mean', 'median', 'count'],
        'Distance': 'mean'
    }).round(0)
    yearly_stats.columns = ['Avg Price', 'Median Price', 'Count', 'Avg Distance']
    yearly_stats = yearly_stats.reset_index()
    
    # Price trend chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_stats['Year'],
        y=yearly_stats['Avg Price'],
        mode='lines+markers',
        name='Average Price',
        line=dict(color='#667eea', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=yearly_stats['Year'],
        y=yearly_stats['Median Price'],
        mode='lines+markers',
        name='Median Price',
        line=dict(color='#ff9800', width=3)
    ))
    fig.update_layout(
        title="Price Trends by Year",
        xaxis_title="Year",
        yaxis_title="Price (₹)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Market composition trends
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📊 Market Composition Trends</div>', unsafe_allow_html=True)
    
    # Car type trends over time
    type_trends = df_cleaned.groupby(['Year', 'Type']).size().reset_index(name='Count')
    fig = px.line(
        type_trends,
        x='Year',
        y='Count',
        color='Type',
        title="Car Type Popularity Over Time",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Fuel type trends
    fuel_trends = df_cleaned.groupby(['Year', 'Fuel']).size().reset_index(name='Count')
    fig = px.line(
        fuel_trends,
        x='Year',
        y='Count',
        color='Fuel',
        title="Fuel Type Trends Over Time",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Seasonal and cyclical patterns
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🔄 Seasonal Patterns</div>', unsafe_allow_html=True)
    
    # Price vs Distance relationship over time
    fig = px.scatter(
        df_cleaned,
        x='Distance',
        y='Price',
        color='Year',
        size='Price',
        hover_data=['Car Name', 'Type', 'Fuel'],
        title="Price vs Distance Relationship by Year",
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Car age distribution trends
    df_cleaned['Car Age'] = 2024 - df_cleaned['Year']
    age_trends = df_cleaned.groupby(['Year', 'Car Age']).size().reset_index(name='Count')
    age_matrix = age_trends.pivot(index='Year', columns='Car Age', values='Count').fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=age_matrix.values,
        x=age_matrix.columns,
        y=age_matrix.index,
        colorscale='Viridis',
        colorbar=dict(title='Count')
    ))
    fig.update_layout(
        title="Car Age Distribution Heatmap",
        xaxis_title="Car Age (years)",
        yaxis_title="Year"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Market insights
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">💡 Market Insights</div>', unsafe_allow_html=True)
    
    # Top performing models by year
    top_models_by_year = df_cleaned.groupby(['Year', 'Car Name']).agg({
        'Price': ['mean', 'count']
    }).round(0)
    top_models_by_year.columns = ['Avg Price', 'Count']
    top_models_by_year = top_models_by_year.reset_index()
    
    # Find top models for each year
    top_models = top_models_by_year.loc[top_models_by_year.groupby('Year')['Count'].idxmax()]
    
    st.markdown('<div class="feature-description"><b>Most Listed Models by Year:</b></div>', unsafe_allow_html=True)
    for _, row in top_models.iterrows():
        st.write(f"• {row['Year']}: {row['Car Name']} ({row['Count']} listings, avg ₹{row['Avg Price']:,.0f})")
    
    # Price volatility analysis
    price_volatility = df_cleaned.groupby('Car Name')['Price'].agg(['mean', 'std']).round(0)
    price_volatility['cv'] = (price_volatility['std'] / price_volatility['mean'] * 100).round(1)
    price_volatility = price_volatility.sort_values('cv', ascending=False).head(10)
    
    st.markdown('<div class="feature-description"><b>Most Price Volatile Models (Top 10):</b></div>', unsafe_allow_html=True)
    for car, stats in price_volatility.iterrows():
        st.write(f"• {car}: {stats['cv']}% coefficient of variation")
    st.markdown('</div>', unsafe_allow_html=True)

    # Download trends data
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    trends_data = yearly_stats.copy()
    csv = trends_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Trends Data (CSV)",
        data=csv,
        file_name='car_market_trends.csv',
        mime='text/csv'
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Explore the trends above to understand market dynamics! 📈")

# Call the app function
app(df_cleaned) 