import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel deep green color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f3fcf7;
    --main-accent: #b7f7d8;
    --main-accent-dark: #34d399;
    --main-card: #e6f9ed;
    --main-hero-gradient: linear-gradient(135deg, #b7f7d8 0%, #34d399 100%);
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

# Load data for this page
df_cleaned = load_and_preprocess_data(DATASET_PATH)

def app(df_cleaned=None):
    if df_cleaned is None:
        df_cleaned = load_and_preprocess_data(DATASET_PATH)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">📊 Advanced Analytics</h1>
        <p class="hero-subtitle">Deep statistical analysis, correlations, and market insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Analysis type selection
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🔬 Select Analysis Type</div>', unsafe_allow_html=True)
    
    analysis_type = st.selectbox(
        "Choose the type of analysis:",
        ["Correlation Analysis", "Statistical Tests", "Price Prediction Factors", "Market Segmentation", "Anomaly Detection"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if analysis_type == "Correlation Analysis":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">📈 Correlation Analysis</div>', unsafe_allow_html=True)
        
        # Numerical correlation heatmap
        numerical_cols = ['Price', 'Distance', 'Year', 'Car Age']
        numerical_cols = [col for col in numerical_cols if col in df_cleaned.columns]
        
        if len(numerical_cols) > 1:
            corr_matrix = df_cleaned[numerical_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu',
                title="Correlation Heatmap of Numerical Features"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed price correlations
            st.markdown('<div class="feature-title">Price Correlations</div>', unsafe_allow_html=True)
            price_corr = corr_matrix['Price'].sort_values(ascending=False)
            fig = px.bar(
                x=price_corr.index,
                y=price_corr.values,
                title="Price Correlation with Other Features",
                labels={'x': 'Features', 'y': 'Correlation Coefficient'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Scatter plot with trendline
            if 'Distance' in numerical_cols:
                fig = px.scatter(
                    df_cleaned,
                    x='Distance',
                    y='Price',
                    trendline="ols",
                    title="Price vs Distance with OLS Trendline"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough numerical columns for correlation analysis.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif analysis_type == "Statistical Tests":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🧪 Statistical Tests</div>', unsafe_allow_html=True)
        
        # T-test for price differences between fuel types
        if 'Fuel' in df_cleaned.columns and 'Price' in df_cleaned.columns:
            fuel_types = df_cleaned['Fuel'].unique()
            if len(fuel_types) >= 2:
                # Get two most common fuel types
                top_fuels = df_cleaned['Fuel'].value_counts().head(2).index
                fuel1_data = df_cleaned[df_cleaned['Fuel'] == top_fuels[0]]['Price']
                fuel2_data = df_cleaned[df_cleaned['Fuel'] == top_fuels[1]]['Price']
                
                # Perform t-test
                t_stat, p_value = stats.ttest_ind(fuel1_data, fuel2_data)
                
                st.markdown(f'<div class="feature-description"><b>T-Test Results:</b> {top_fuels[0]} vs {top_fuels[1]}</div>', unsafe_allow_html=True)
                st.write(f"T-statistic: {t_stat:.4f}")
                st.write(f"P-value: {p_value:.4f}")
                st.write(f"Significant difference: {'Yes' if p_value < 0.05 else 'No'} (α=0.05)")
                
                # Box plot for visualization
                fig = px.box(
                    df_cleaned[df_cleaned['Fuel'].isin(top_fuels)],
                    x='Fuel',
                    y='Price',
                    title=f"Price Distribution: {top_fuels[0]} vs {top_fuels[1]}"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Fuel and Price columns required for statistical tests.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif analysis_type == "Price Prediction Factors":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🎯 Price Prediction Factors</div>', unsafe_allow_html=True)
        
        # Average price by categorical variables
        categorical_cols = ['Type', 'Fuel', 'Drive', 'Owner']
        categorical_cols = [col for col in categorical_cols if col in df_cleaned.columns]
        
        for col in categorical_cols:
            avg_price_by_cat = df_cleaned.groupby(col)['Price'].mean().sort_values(ascending=False)
            
            fig = px.bar(
                x=avg_price_by_cat.index,
                y=avg_price_by_cat.values,
                title=f"Average Price by {col}",
                labels={'x': col, 'y': 'Average Price (₹)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif analysis_type == "Market Segmentation":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🎯 Market Segmentation</div>', unsafe_allow_html=True)
        
        # Create price segments
        df_cleaned['Price_Segment'] = pd.cut(
            df_cleaned['Price'],
            bins=[0, 500000, 1000000, 2000000, float('inf')],
            labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
        )
        
        # Create age segments
        df_cleaned['Age_Segment'] = pd.cut(
            df_cleaned['Car Age'],
            bins=[0, 3, 7, 10, float('inf')],
            labels=['New', 'Recent', 'Mature', 'Vintage']
        )
        
        # Price segment distribution
        price_seg_counts = df_cleaned['Price_Segment'].value_counts()
        fig = px.pie(
            values=price_seg_counts.values,
            names=price_seg_counts.index,
            title="Market Distribution by Price Segment"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Age segment distribution
        age_seg_counts = df_cleaned['Age_Segment'].value_counts()
        fig = px.pie(
            values=age_seg_counts.values,
            names=age_seg_counts.index,
            title="Market Distribution by Age Segment"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Cross-segment analysis
        segment_analysis = df_cleaned.groupby(['Price_Segment', 'Age_Segment'])['Price'].mean().unstack()
        fig = px.imshow(
            segment_analysis,
            text_auto=True,
            aspect="auto",
            title="Average Price by Price and Age Segments"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif analysis_type == "Anomaly Detection":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🔍 Anomaly Detection</div>', unsafe_allow_html=True)
        
        # Outlier detection using IQR method
        Q1 = df_cleaned['Price'].quantile(0.25)
        Q3 = df_cleaned['Price'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df_cleaned[(df_cleaned['Price'] < lower_bound) | (df_cleaned['Price'] > upper_bound)]
        normal_data = df_cleaned[(df_cleaned['Price'] >= lower_bound) & (df_cleaned['Price'] <= upper_bound)]
        
        st.markdown(f'<div class="feature-description"><b>Outlier Analysis:</b> Found {len(outliers)} outliers out of {len(df_cleaned)} total records</div>', unsafe_allow_html=True)
        
        # Box plot showing outliers
        fig = px.box(
            df_cleaned,
            y='Price',
            title="Price Distribution with Outliers",
            points="outliers"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Outlier details
        if len(outliers) > 0:
            st.markdown('<div class="feature-title">Outlier Details</div>', unsafe_allow_html=True)
            st.dataframe(outliers[['Car Name', 'Price', 'Year', 'Distance', 'Type', 'Fuel']].head(10))
        st.markdown('</div>', unsafe_allow_html=True)

    # Summary statistics
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📋 Summary Statistics</div>', unsafe_allow_html=True)
    
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
            st.write(df_cleaned[col].value_counts().head(3))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Advanced analytics completed! Explore different analysis types above. 📊")

# Call the app function
app() 