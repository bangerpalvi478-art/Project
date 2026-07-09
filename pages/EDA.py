import streamlit as st
from streamlit_lottie import st_lottie  # type: ignore
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel green/teal color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f6fbf7;
    --main-accent: #a7f3d0;
    --main-accent-dark: #38b2ac;
    --main-card: #e6f9f2;
    --main-hero-gradient: linear-gradient(135deg, #a7f3d0 0%, #38b2ac 100%);
    --main-feature-card: #e6f9f2;
    --main-feature-title: #38b2ac;
    --main-stat-number: #38b2ac;
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

# Re-import and re-cache data from the main app.py
from data_utils import load_and_preprocess_data, DATASET_PATH

# Load data for this page
df_cleaned = load_and_preprocess_data(DATASET_PATH)

def load_lottie(path):
    with open(path, "r") as f:
        return json.load(f)

def app(df_cleaned):
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚗 Used Car Market EDA Dashboard</h1>
        <p class="hero-subtitle">Explore the used car market with interactive and visually engaging charts.</p>
    </div>
    """, unsafe_allow_html=True)

    # Lottie animation at the top
    lottie_path = os.path.join("index", "assets", "car_intro.json")
    if os.path.exists(lottie_path):
        lottie_car = load_lottie(lottie_path)
        st_lottie(lottie_car, speed=1, loop=True, height=200)
    else:
        st.info("Car animation not found.")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # 1. Sunburst: Car Type, Fuel, and Transmission
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">1. Car Type, Fuel, and Transmission Breakdown</div>', unsafe_allow_html=True)
    if {'Type', 'Fuel', 'Drive'}.issubset(df_cleaned.columns):
        fig = px.sunburst(
            df_cleaned,
            path=['Type', 'Fuel', 'Drive'],
            values='Price',
            color='Type',
            color_discrete_sequence=px.colors.qualitative.Set3,
            title="Sunburst: Car Type → Fuel → Transmission"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Columns missing for Sunburst chart.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Donut Chart: Previous Owners
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">2. Previous Owners Distribution</div>', unsafe_allow_html=True)
    owner_counts = df_cleaned['Owner'].value_counts().reset_index()
    owner_counts.columns = ['Owner', 'Count']  # Rename columns for clarity
    fig = px.pie(
        owner_counts,
        names='Owner', values='Count',
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.RdBu,
        title="Donut Chart: Previous Owners"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Animated Scatter: Price vs. Distance by Year
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">3. Price vs. Distance Traveled (Animated by Year)</div>', unsafe_allow_html=True)
    if {'Distance', 'Price', 'Year', 'Type'}.issubset(df_cleaned.columns):
        fig = px.scatter(
            df_cleaned,
            x='Distance', y='Price',
            animation_frame='Year',
            color='Type',
            hover_data=['Car Name', 'Fuel', 'Drive'],
            size='Price',
            title="Animated Scatter: Price vs. Distance by Year",
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Columns missing for animated scatter plot.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Treemap: Popular Models by Type
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">4. Most Popular Car Models by Type (Treemap)</div>', unsafe_allow_html=True)
    if {'Car Name', 'Type'}.issubset(df_cleaned.columns):
        top_models = df_cleaned['Car Name'].value_counts().head(15).index
        df_top = df_cleaned[df_cleaned['Car Name'].isin(top_models)]
        fig = px.treemap(
            df_top,
            path=['Type', 'Car Name'],
            values='Price',
            color='Type',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Treemap: Top Car Models by Type"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Columns missing for treemap.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. Violin Plot: Price Distribution by Fuel Type
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">5. Price Distribution by Fuel Type (Violin Plot)</div>', unsafe_allow_html=True)
    if {'Fuel', 'Price'}.issubset(df_cleaned.columns):
        fig = px.violin(
            df_cleaned,
            x='Fuel', y='Price',
            box=True, points='all',
            color='Fuel',
            color_discrete_sequence=px.colors.qualitative.Set2,
            title="Violin Plot: Price by Fuel Type"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Columns missing for violin plot.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Explore the interactive charts above to discover patterns in the car market! 📊")

# Call the app function with the cleaned data
app(df_cleaned)