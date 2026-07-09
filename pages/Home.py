import streamlit as st
import pandas as pd
import io
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel blue/indigo color scheme
st.markdown('''
<style>
:root {
    --main-bg: #f3f7fa;
    --main-accent: #a3bffa;
    --main-accent-dark: #5a7fd6;
    --main-card: #eaf0fb;
    --main-hero-gradient: linear-gradient(135deg, #a3bffa 0%, #5a7fd6 100%);
    --main-feature-card: #eaf0fb;
    --main-feature-title: #5a7fd6;
    --main-stat-number: #5a7fd6;
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

df_cleaned = load_and_preprocess_data(DATASET_PATH)

def app(df_cleaned):
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚗 Used Car Price Analysis Dashboard</h1>
        <p class="hero-subtitle">Discover insights, trends, and hidden gems in the Indian used car market.<br><b>Interactive. Visual. Actionable.</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Key Stats Section
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="stat-item"><span class="stat-number">{:,}</span><div class="stat-label">Rows</div></div>'.format(df_cleaned.shape[0]), unsafe_allow_html=True)
    col2.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Columns</div></div>'.format(df_cleaned.shape[1]), unsafe_allow_html=True)
    col3.markdown('<div class="stat-item"><span class="stat-number">{}</span><div class="stat-label">Unique Models</div></div>'.format(df_cleaned['Car Name'].nunique()), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Data Preview
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">👀 Preview the Data</div>', unsafe_allow_html=True)
    st.dataframe(df_cleaned.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download button
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    csv = df_cleaned.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Full Cleaned Dataset (CSV)",
        data=csv,
        file_name='cleaned_used_cars.csv',
        mime='text/csv'
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Descriptive Stats
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📊 Descriptive Statistics</div>', unsafe_allow_html=True)
    st.dataframe(df_cleaned.describe().T, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Data Info
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🗂️ Data Information</div>', unsafe_allow_html=True)
    buffer = io.StringIO()
    df_cleaned.info(buf=buffer)
    s = buffer.getvalue()
    st.code(s, language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)

    # How to Use Section
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">✨ How to Use This Dashboard</div>', unsafe_allow_html=True)
    st.markdown('''
    <ul class="feature-description">
        <li>Navigate to <b>EDA</b> for interactive charts and trends.</li>
        <li>Use <b>Search</b> to find specific cars or filter by features.</li>
        <li>Check <b>Image Gallery</b> for car visuals.</li>
        <li>Download the dataset for your own analysis.</li>
    </ul>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Ready to explore? Use the sidebar to dive into the data! 🚀")

app(df_cleaned)