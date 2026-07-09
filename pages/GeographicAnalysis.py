import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel earthy brown/olive color scheme
st.markdown('''
<style>
:root {
    --main-bg: #fafaf5;
    --main-accent: #e6ddb3;
    --main-accent-dark: #b5a642;
    --main-card: #f5f3e6;
    --main-hero-gradient: linear-gradient(135deg, #e6ddb3 0%, #b5a642 100%);
    --main-feature-card: #f5f3e6;
    --main-feature-title: #b5a642;
    --main-stat-number: #b5a642;
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
        <h1 class="hero-title">🗺️ Geographic Analysis</h1>
        <p class="hero-subtitle">Explore regional car market patterns and location-based insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Extract state from location
    if 'Location' in df_cleaned.columns:
        df_cleaned['State'] = df_cleaned['Location'].str.split(',').str[-1].str.strip()
    else:
        st.error("Location column not found in the dataset.")
        return

    # Overview metrics
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Total Locations</div></div>'.format(df_cleaned['Location'].nunique()), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Total States</div></div>'.format(df_cleaned['State'].nunique()), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Avg Price</div></div>'.format(int(df_cleaned['Price'].mean())), unsafe_allow_html=True)
    with col4:
        most_common_state = df_cleaned['State'].mode().iloc[0] if not df_cleaned['State'].mode().empty else "N/A"
        st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Most Common State</div></div>'.format(most_common_state), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # State selection
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📍 Select States to Analyze</div>', unsafe_allow_html=True)
    
    all_states = sorted(df_cleaned['State'].unique())
    selected_states = st.multiselect(
        "Choose states to analyze:",
        all_states,
        default=all_states[:5] if len(all_states) >= 5 else all_states
    )
    
    if not selected_states:
        st.warning("Please select at least one state to analyze.")
        return
    
    filtered_df = df_cleaned[df_cleaned['State'].isin(selected_states)]
    st.markdown('</div>', unsafe_allow_html=True)

    # Regional price analysis
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">💰 Regional Price Analysis</div>', unsafe_allow_html=True)
    
    # Average price by state
    state_avg_price = filtered_df.groupby('State')['Price'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=state_avg_price.index,
        y=state_avg_price.values,
        title="Average Price by State",
        labels={'x': 'State', 'y': 'Average Price (₹)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Car count by state
    state_counts = filtered_df['State'].value_counts()
    fig = px.bar(
        x=state_counts.index,
        y=state_counts.values,
        title="Number of Cars by State",
        labels={'x': 'State', 'y': 'Number of Cars'}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Price distribution by region
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📊 Price Distribution by Region</div>', unsafe_allow_html=True)
    
    fig = px.box(
        filtered_df,
        x='State',
        y='Price',
        title="Price Distribution by State",
        color='State'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Regional market composition
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🏗️ Regional Market Composition</div>', unsafe_allow_html=True)
    
    # Car type distribution by state
    type_by_state = filtered_df.groupby(['State', 'Type']).size().unstack(fill_value=0)
    fig = px.imshow(
        type_by_state,
        title="Car Type Distribution by State",
        labels={'x': 'Car Type', 'y': 'State'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Fuel type distribution by state
    fuel_by_state = filtered_df.groupby(['State', 'Fuel']).size().unstack(fill_value=0)
    fig = px.imshow(
        fuel_by_state,
        title="Fuel Type Distribution by State",
        labels={'x': 'Fuel Type', 'y': 'State'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Transmission distribution by state
    drive_by_state = filtered_df.groupby(['State', 'Drive']).size().unstack(fill_value=0)
    fig = px.imshow(
        drive_by_state,
        title="Transmission Distribution by State",
        labels={'x': 'Transmission', 'y': 'State'}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Regional trends analysis
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📈 Regional Trends Analysis</div>', unsafe_allow_html=True)
    
    # Price trends by year and state
    yearly_state_price = filtered_df.groupby(['Year', 'State'])['Price'].mean().reset_index()
    fig = px.line(
        yearly_state_price,
        x='Year',
        y='Price',
        color='State',
        title="Price Trends by Year and State",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Regional insights
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">💡 Regional Insights</div>', unsafe_allow_html=True)
    
    # Top states by average price
    top_price_states = filtered_df.groupby('State')['Price'].mean().sort_values(ascending=False).head(5)
    st.markdown('<div class="feature-description"><b>Top 5 States by Average Price:</b></div>', unsafe_allow_html=True)
    for state, price in top_price_states.items():
        st.write(f"• {state}: ₹{price:,.0f}")
    
    # Most active markets
    most_active_states = filtered_df['State'].value_counts().head(5)
    st.markdown('<div class="feature-description"><b>Most Active Markets (by car count):</b></div>', unsafe_allow_html=True)
    for state, count in most_active_states.items():
        st.write(f"• {state}: {count} cars")
    
    # Best value markets (lowest price to distance ratio)
    value_ratio = filtered_df.groupby('State').apply(lambda x: x['Price'].mean() / x['Distance'].mean()).sort_values()
    st.markdown('<div class="feature-description"><b>Best Value Markets (Price/Distance ratio):</b></div>', unsafe_allow_html=True)
    for state, ratio in value_ratio.head(5).items():
        st.write(f"• {state}: {ratio:.2f}")
    
    # Premium markets (highest price to distance ratio)
    st.markdown('<div class="feature-description"><b>Premium Markets (Price/Distance ratio):</b></div>', unsafe_allow_html=True)
    for state, ratio in value_ratio.tail(5).items():
        st.write(f"• {state}: {ratio:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Detailed state analysis
    if len(selected_states) == 1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🔍 Detailed State Analysis</div>', unsafe_allow_html=True)
        
        state_data = filtered_df[filtered_df['State'] == selected_states[0]]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Total Cars</div></div>'.format(len(state_data)), unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">Avg Price</div></div>'.format(int(state_data['Price'].mean())), unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Unique Models</div></div>'.format(state_data['Car Name'].nunique()), unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Avg Year</div></div>'.format(int(state_data['Year'].mean())), unsafe_allow_html=True)
        
        # Top models in this state
        top_models = state_data['Car Name'].value_counts().head(10)
        st.markdown('<div class="feature-title">Top Models in {}</div>'.format(selected_states[0]), unsafe_allow_html=True)
        for model, count in top_models.items():
            avg_price = state_data[state_data['Car Name'] == model]['Price'].mean()
            st.write(f"• {model}: {count} listings, avg ₹{avg_price:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Download regional data
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    regional_data = filtered_df.copy()
    csv = regional_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Regional Data (CSV)",
        data=csv,
        file_name=f'regional_analysis_{"_".join(selected_states[:3])}.csv',
        mime='text/csv'
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Geographic analysis completed! Explore regional patterns above. 🗺️")

# Call the app function
app() 