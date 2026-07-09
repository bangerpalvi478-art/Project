import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from data_utils import load_and_preprocess_data, DATASET_PATH

# Page-specific pastel mint color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f3fdf7;
    --main-accent: #b9fbc0;
    --main-accent-dark: #34d399;
    --main-card: #e6f9ed;
    --main-hero-gradient: linear-gradient(135deg, #b9fbc0 0%, #34d399 100%);
    --main-feature-card: #e6f9ed;
    --main-feature-title: #34d399;
    --main-stat-number: #34d399;
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

def app(df_cleaned):
    st.markdown(
        '''<style>@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
        .insights-hero {background: linear-gradient(135deg, #232526 0%, #414345 100%); padding: 2rem 1rem; border-radius: 1rem; margin-bottom: 2rem;}
        .insights-title {font-family: "Orbitron", sans-serif; color: #fcb69f; font-size: 2.5rem; letter-spacing:2px; animation: fadeIn 1.2s cubic-bezier(.68,-0.55,.27,1.55);}
        .insight-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 1rem; margin: 1rem 0; color: white;}
        .metric-card {background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1rem; border-radius: 0.5rem; text-align: center; color: white;}
        @keyframes fadeIn {from {opacity:0; transform:translateY(40px);} to {opacity:1; transform:translateY(0);}}
        </style>''', unsafe_allow_html=True)
    
    st.markdown(
        '<div class="insights-hero"><h1 class="insights-title">💡 Deep Insights</h1><p style="font-family:Orbitron, sans-serif; color:#fff; font-size:1.2rem;">Discover hidden patterns and advanced analytics in the used car data. This page features a dark, tech-inspired theme.</p></div>',
        unsafe_allow_html=True)

    # Key Metrics Dashboard
    st.markdown("### 📊 Key Market Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="metric-card"><h3>💰 Avg Price</h3><h2>₹{df_cleaned["Price"].mean():,.0f}</h2></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="metric-card"><h3>📈 Median Price</h3><h2>₹{df_cleaned["Price"].median():,.0f}</h2></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="metric-card"><h3>🚗 Total Cars</h3><h2>{len(df_cleaned):,}</h2></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'<div class="metric-card"><h3>🏢 Brands</h3><h2>{df_cleaned["Car Name"].str.split().str[0].nunique()}</h2></div>', unsafe_allow_html=True)

    # 1. Price Distribution Analysis
    st.markdown("### 🎯 Price Distribution Insights")
    
    # Create subplots for price analysis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Price Distribution', 'Price by Car Type', 'Price vs Distance', 'Price by Fuel Type'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Price histogram
    fig.add_trace(
        go.Histogram(x=df_cleaned['Price'], nbinsx=50, name='Price Distribution', 
                    marker_color='#fcb69f', opacity=0.7),
        row=1, col=1
    )
    
    # Price by car type (box plot)
    for car_type in df_cleaned['Type'].unique():
        type_data = df_cleaned[df_cleaned['Type'] == car_type]['Price']
        fig.add_trace(
            go.Box(y=type_data, name=car_type, boxpoints='outliers'),
            row=1, col=2
        )
    
    # Price vs Distance scatter
    fig.add_trace(
        go.Scatter(x=df_cleaned['Distance'], y=df_cleaned['Price'], 
                  mode='markers', marker=dict(size=5, opacity=0.6, color='#667eea'),
                  name='Price vs Distance'),
        row=2, col=1
    )
    
    # Price by fuel type (violin plot)
    for fuel in df_cleaned['Fuel'].unique():
        fuel_data = df_cleaned[df_cleaned['Fuel'] == fuel]['Price']
        fig.add_trace(
            go.Violin(y=fuel_data, name=fuel, box_visible=True, meanline_visible=True),
            row=2, col=2
        )
    
    fig.update_layout(height=800, showlegend=False, title_text="Comprehensive Price Analysis")
    st.plotly_chart(fig, use_container_width=True)

    # 2. Market Segmentation Analysis
    st.markdown("### 🎨 Market Segmentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Car type distribution with price
        fig = px.treemap(
            df_cleaned,
            path=['Type'],
            values='Price',
            color='Price',
            color_continuous_scale='RdYlBu',
            title="Market Share by Car Type (Size = Total Price Value)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Brand analysis
        brand_analysis = df_cleaned.groupby(df_cleaned['Car Name'].str.split().str[0]).agg({
            'Price': ['mean', 'count'],
            'Distance': 'mean',
            'Car Age': 'mean'
        }).round(2)
        brand_analysis.columns = ['Avg_Price', 'Count', 'Avg_Distance', 'Avg_Age']
        brand_analysis = brand_analysis.sort_values('Count', ascending=False).head(10)
        
        fig = px.bar(
            brand_analysis.reset_index(),
            x='Car Name',
            y=['Avg_Price', 'Count'],
            title="Top 10 Brands: Average Price vs Count",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

    # 3. Correlation Analysis
    st.markdown("### 🔗 Correlation Insights")
    
    # Calculate correlations
    numeric_cols = ['Price', 'Distance', 'Car Age', 'Year']
    correlation_matrix = df_cleaned[numeric_cols].corr()
    
    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu',
        title="Correlation Matrix: Price, Distance, Age, Year"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation insights
    price_distance_corr = correlation_matrix.loc['Price', 'Distance']
    price_age_corr = correlation_matrix.loc['Price', 'Car Age']
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>🔍 Key Correlation Findings:</h4>
        <ul>
            <li><strong>Price vs Distance:</strong> {price_distance_corr:.3f} - {'Strong negative' if price_distance_corr < -0.5 else 'Moderate negative' if price_distance_corr < -0.3 else 'Weak negative' if price_distance_corr < 0 else 'Positive'} correlation</li>
            <li><strong>Price vs Car Age:</strong> {price_age_corr:.3f} - {'Strong negative' if price_age_corr < -0.5 else 'Moderate negative' if price_age_corr < -0.3 else 'Weak negative' if price_age_corr < 0 else 'Positive'} correlation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # 4. Statistical Analysis
    st.markdown("### 📈 Statistical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price statistics by category
        st.subheader("Price Statistics by Category")
        
        # By Fuel Type
        fuel_stats = df_cleaned.groupby('Fuel')['Price'].agg(['mean', 'median', 'std', 'count']).round(2)
        st.dataframe(fuel_stats, use_container_width=True)
        
        # By Drive Type
        drive_stats = df_cleaned.groupby('Drive')['Price'].agg(['mean', 'median', 'std', 'count']).round(2)
        st.dataframe(drive_stats, use_container_width=True)
    
    with col2:
        # Outlier Analysis
        st.subheader("Outlier Analysis")
        
        # Calculate outliers using IQR method
        Q1 = df_cleaned['Price'].quantile(0.25)
        Q3 = df_cleaned['Price'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df_cleaned[(df_cleaned['Price'] < lower_bound) | (df_cleaned['Price'] > upper_bound)]
        
        st.metric("Total Outliers", len(outliers))
        st.metric("Outlier Percentage", f"{(len(outliers)/len(df_cleaned)*100):.1f}%")
        st.metric("Lower Bound", f"₹{lower_bound:,.0f}")
        st.metric("Upper Bound", f"₹{upper_bound:,.0f}")

    # 5. Advanced Analytics
    st.markdown("### 🧠 Advanced Analytics")
    
    # Price prediction insights
    st.subheader("Price Prediction Factors")
    
    # Simple correlation-based feature importance
    numeric_features = ['Distance', 'Car Age', 'Year']
    correlations = []
    
    for feature in numeric_features:
        if feature in df_cleaned.columns:
            corr = df_cleaned['Price'].corr(df_cleaned[feature])
            correlations.append({'Feature': feature, 'Correlation': abs(corr)})
    
    # Add categorical feature analysis
    for feature in ['Fuel', 'Drive', 'Type']:
        if feature in df_cleaned.columns:
            # Calculate average price difference from overall mean
            overall_mean = df_cleaned['Price'].mean()
            feature_impact = df_cleaned.groupby(feature)['Price'].mean() - overall_mean
            avg_impact = abs(feature_impact).mean()
            correlations.append({'Feature': feature, 'Correlation': avg_impact / overall_mean})
    
    feature_importance = pd.DataFrame(correlations).sort_values('Correlation', ascending=False)
    
    fig = px.bar(
        feature_importance,
        x='Feature',
        y='Correlation',
        title="Feature Importance for Price Prediction (Correlation-based)",
        color='Correlation',
        color_continuous_scale='RdYlBu'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Price range analysis
    price_ranges = pd.cut(df_cleaned['Price'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    price_range_stats = df_cleaned.groupby(price_ranges).agg({
        'Distance': 'mean',
        'Car Age': 'mean',
        'Year': 'mean'
    }).round(2)
    
    st.markdown(f"""
    <div class="insight-card">
        <h4>🎯 Price Range Analysis:</h4>
        <ul>
            <li><strong>Most Important Factor:</strong> {feature_importance.iloc[0]['Feature']}</li>
            <li><strong>Least Important Factor:</strong> {feature_importance.iloc[-1]['Feature']}</li>
            <li><strong>Price Range Distribution:</strong> {len(price_ranges.value_counts())} categories</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Price Range Characteristics")
    st.dataframe(price_range_stats, use_container_width=True)

    # 6. Market Trends
    st.markdown("### 📊 Market Trends Analysis")
    
    # Year-wise trends
    year_trends = df_cleaned.groupby('Year').agg({
        'Price': ['mean', 'count'],
        'Distance': 'mean'
    }).round(2)
    year_trends.columns = ['Avg_Price', 'Count', 'Avg_Distance']
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Average Price by Year', 'Number of Cars by Year'),
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Scatter(x=year_trends.index, y=year_trends['Avg_Price'], 
                  mode='lines+markers', name='Avg Price', line=dict(color='#fcb69f')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=year_trends.index, y=year_trends['Count'], name='Count', marker_color='#667eea'),
        row=2, col=1
    )
    
    fig.update_layout(height=600, title_text="Market Trends Over Years")
    st.plotly_chart(fig, use_container_width=True)

    # 7. Recommendations
    st.markdown("### 💡 Actionable Insights & Recommendations")
    
    st.markdown("""
    <div class="insight-card">
        <h4>🎯 Key Recommendations:</h4>
        <ol>
            <li><strong>For Buyers:</strong> Focus on cars with lower mileage and newer models for better value retention</li>
            <li><strong>For Sellers:</strong> Highlight fuel efficiency and maintenance history to justify higher prices</li>
            <li><strong>Market Opportunity:</strong> SUVs and luxury vehicles show strong price stability</li>
            <li><strong>Risk Factors:</strong> High-mileage vehicles and older models have significant price depreciation</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Load data and run the app
df_cleaned = load_and_preprocess_data(DATASET_PATH)
app(df_cleaned) 