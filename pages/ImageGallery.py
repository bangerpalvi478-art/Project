import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel purple/violet color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f7f5fa;
    --main-accent: #d6bcfa;
    --main-accent-dark: #7f56d9;
    --main-card: #ede9f7;
    --main-hero-gradient: linear-gradient(135deg, #d6bcfa 0%, #7f56d9 100%);
    --main-feature-card: #ede9f7;
    --main-feature-title: #7f56d9;
    --main-stat-number: #7f56d9;
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
        <h1 class="hero-title">🚗 Car Models Showcase</h1>
        <p class="hero-subtitle">Explore car models with detailed information, pricing, and statistics.</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar filters
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🔍 Filters</div>', unsafe_allow_html=True)
    
    # Car type filter
    car_types = ['All'] + sorted(df_cleaned['Type'].unique().tolist())
    selected_type = st.selectbox("Car Type", car_types)
    
    # Fuel type filter
    fuel_types = ['All'] + sorted(df_cleaned['Fuel'].unique().tolist())
    selected_fuel = st.selectbox("Fuel Type", fuel_types)
    
    # Price range filter
    min_price = int(df_cleaned['Price'].min())
    max_price = int(df_cleaned['Price'].max())
    price_range = st.slider(
        "Price Range (₹)", 
        min_value=min_price, 
        max_value=max_price, 
        value=(min_price, max_price)
    )
    
    # Year range filter
    min_year = int(df_cleaned['Year'].min())
    max_year = int(df_cleaned['Year'].max())
    year_range = st.slider(
        "Year Range", 
        min_value=min_year, 
        max_value=max_year, 
        value=(min_year, max_year)
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_df = df_cleaned.copy()
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['Type'] == selected_type]
    if selected_fuel != 'All':
        filtered_df = filtered_df[filtered_df['Fuel'] == selected_fuel]
    filtered_df = filtered_df[
        (filtered_df['Price'] >= price_range[0]) & 
        (filtered_df['Price'] <= price_range[1]) &
        (filtered_df['Year'] >= year_range[0]) & 
        (filtered_df['Year'] <= year_range[1])
    ]

    # Display filtered results count
    st.info(f"📊 Showing {len(filtered_df)} cars matching your criteria")

    # Key statistics
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Average Price</div></div>'.format(int(filtered_df['Price'].mean())), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Median Price</div></div>'.format(int(filtered_df['Price'].median())), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Unique Models</div></div>'.format(filtered_df['Car Name'].nunique()), unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-item"><span class="stat-number">{:,}</span><div class="stat-label">Avg Distance</div></div>'.format(int(filtered_df['Distance'].mean())), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Car models showcase
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🚙 Featured Car Models</div>', unsafe_allow_html=True)
    
    # Get top models by count
    top_models = filtered_df['Car Name'].value_counts().head(10).index
    
    # Display car cards
    for i, model in enumerate(top_models):
        model_data = filtered_df[filtered_df['Car Name'] == model]
        
        with st.expander(f"🏎️ {model} ({len(model_data)} listings)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Model statistics
                avg_price = model_data['Price'].mean()
                avg_distance = model_data['Distance'].mean()
                avg_year = model_data['Year'].mean()
                
                st.markdown(f"""
                <div class="feature-description">
                **Price Range:** ₹{model_data['Price'].min():,.0f} - ₹{model_data['Price'].max():,.0f}  
                **Average Price:** ₹{avg_price:,.0f}  
                **Average Distance:** {avg_distance:,.0f} km  
                **Average Year:** {avg_year:.0f}  
                **Fuel Types:** {', '.join(model_data['Fuel'].unique())}  
                **Transmission:** {', '.join(model_data['Drive'].unique())}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Price distribution chart for this model
                fig = px.histogram(
                    model_data, 
                    x='Price', 
                    nbins=10,
                    title=f"Price Distribution - {model}",
                    labels={'Price': 'Price (₹)', 'count': 'Count'}
                )
                fig.update_layout(height=200, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Interactive charts
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📈 Interactive Analysis</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Price Analysis", "Year Trends", "Fuel Comparison"])
    
    with tab1:
        # Price vs Distance scatter plot
        fig = px.scatter(
            filtered_df,
            x='Distance',
            y='Price',
            color='Type',
            hover_data=['Car Name', 'Year', 'Fuel'],
            title="Price vs Distance by Car Type"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Price trends by year
        yearly_avg = filtered_df.groupby('Year')['Price'].mean().reset_index()
        fig = px.line(
            yearly_avg,
            x='Year',
            y='Price',
            title="Average Price Trends by Year",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Fuel type comparison
        fuel_stats = filtered_df.groupby('Fuel').agg({
            'Price': ['mean', 'count'],
            'Distance': 'mean'
        }).round(0)
        fuel_stats.columns = ['Avg Price', 'Count', 'Avg Distance']
        fuel_stats = fuel_stats.reset_index()
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                fuel_stats,
                x='Fuel',
                y='Avg Price',
                title="Average Price by Fuel Type"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(
                fuel_stats,
                values='Count',
                names='Fuel',
                title="Distribution by Fuel Type"
            )
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download filtered data
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data (CSV)",
        data=csv,
        file_name=f'filtered_cars_{selected_type}_{selected_fuel}.csv',
        mime='text/csv'
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Explore the car models and use filters to find your perfect match! 🚗")

# Call the app function
app()