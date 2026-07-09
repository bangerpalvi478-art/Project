import streamlit as st
import pandas as pd
import plotly.express as px

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel orange/amber color scheme
st.markdown('''
<style>
:root {
    --main-bg: #fff8f1;
    --main-accent: #ffe0b2;
    --main-accent-dark: #ffb74d;
    --main-card: #fff3e0;
    --main-hero-gradient: linear-gradient(135deg, #ffe0b2 0%, #ffb74d 100%);
    --main-feature-card: #fff3e0;
    --main-feature-title: #ffb74d;
    --main-stat-number: #ffb74d;
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

def app(df_cleaned):
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🔍 Search & Filter Cars</h1>
        <p class="hero-subtitle">Use the filters below to find cars that match your criteria.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Filters ---
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">Filter Options</div>', unsafe_allow_html=True)
    
    # Dynamic filter creation based on column types
    filtered_df = df_cleaned.copy()

    # Categorical Filters (Dropdowns)
    categorical_cols = ['Type', 'Fuel', 'Drive', 'Owner', 'Location']
    for col in categorical_cols:
        if col in filtered_df.columns:
            options = ['All'] + sorted(filtered_df[col].unique().tolist())
            selected_value = st.selectbox(f"Select {col}", options, key=f"filter_{col}")
            if selected_value != 'All':
                filtered_df = filtered_df[filtered_df[col] == selected_value]
        else:
            st.warning(f"'{col}' column not found for filtering.")

    # Numerical Filters (Sliders)
    numerical_cols = ['Price', 'Distance', 'Year', 'Car Age']
    for col in numerical_cols:
        if col in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[col]):
            min_val, max_val = float(filtered_df[col].min()), float(filtered_df[col].max())
            selected_range = st.slider(
                f"Select {col} Range",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
                key=f"filter_{col}_range"
            )
            filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[1])]
        elif col in df_cleaned.columns: # Check if column exists but is not numeric
             st.warning(f"'{col}' column is not numeric and cannot be filtered by range.")
        else:
            st.warning(f"'{col}' column not found for filtering.")

    # Search Bar for Car Name (Text Input)
    if 'Car Name' in df_cleaned.columns:
        search_query = st.text_input("Search Car Name", key="search_car_name").lower()
        if search_query:
            filtered_df = filtered_df[filtered_df['Car Name'].str.lower().str.contains(search_query)]
    else:
        st.warning("'Car Name' column not found for search.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Results Section
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">Filtered Results</div>', unsafe_allow_html=True)
    st.markdown(f"<div class='feature-description'>Found <b>{filtered_df.shape[0]}</b> cars matching your criteria</div>", unsafe_allow_html=True)

    if not filtered_df.empty:
        # Display filtered data
        st.dataframe(filtered_df)

        # Optional: Display a chart of filtered data (e.g., price distribution of filtered cars)
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Price Distribution of Filtered Cars</div>', unsafe_allow_html=True)
        if 'Price' in filtered_df.columns:
            fig = px.histogram(filtered_df, x='Price', nbins=30,
                               title='Price Distribution of Current Selection',
                               labels={'Price': 'Car Price (INR)'},
                               template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Price column not available in filtered data for plotting.")

        # Optional: Display a chart of filtered data (e.g., Car Type distribution)
        st.markdown('<div class="feature-title">Car Type Distribution of Filtered Cars</div>', unsafe_allow_html=True)
        if 'Type' in filtered_df.columns:
            type_counts = filtered_df['Type'].value_counts().reset_index()
            type_counts.columns = ['Type', 'Count']
            fig = px.bar(type_counts, x='Type', y='Count',
                         title='Car Type Distribution of Current Selection',
                         labels={'Type': 'Car Type', 'Count': 'Number of Cars'},
                         template='plotly_white',
                         color='Count', color_continuous_scale=px.colors.sequential.Blues)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Car Type column not available in filtered data for plotting.")

    else:
        st.warning("No cars match the selected filters. Please adjust your criteria.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Use the filters above to find your perfect car! 🚗")

# Call the app function with the cleaned data
app(df_cleaned)