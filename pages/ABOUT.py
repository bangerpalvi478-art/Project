# simport streamlit as st

import streamlit as st

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel gold/yellow color scheme
st.markdown('''
<style>
:root {
    --main-bg: #fffbea;
    --main-accent: #ffe066;
    --main-accent-dark: #ffd600;
    --main-card: #fff9db;
    --main-hero-gradient: linear-gradient(135deg, #ffe066 0%, #ffd600 100%);
    --main-feature-card: #fff9db;
    --main-feature-title: #ffd600;
    --main-stat-number: #ffd600;
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

def app():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚗 RECnREV Dashboard</h1>
        <p class="hero-subtitle">Advanced Car Market Analysis & Price Prediction Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Project Overview
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <h3 class="feature-title">Project Mission</h3>
        <p class="feature-description">
            To revolutionize the used car market by providing data-driven insights, 
            accurate price predictions, and comprehensive market analysis. Our platform 
            empowers buyers and sellers with the information they need to make informed decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key Features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <h3 class="feature-title">Advanced Analytics</h3>
            <p class="feature-description">
                Comprehensive statistical analysis, correlation studies, and market segmentation 
                to understand the factors driving car prices.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🤖</span>
            <h3 class="feature-title">ML Price Prediction</h3>
            <p class="feature-description">
                Machine learning models (Random Forest & Linear Regression) for accurate 
                price predictions with confidence intervals.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🗺️</span>
            <h3 class="feature-title">Geographic Analysis</h3>
            <p class="feature-description">
                Regional price variations, location-based insights, and market trends 
                across different states and regions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔍</span>
            <h3 class="feature-title">Smart Comparison</h3>
            <p class="feature-description">
                Side-by-side car comparison tool with detailed metrics, visual analysis, 
                and smart recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Dataset Information
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📋</span>
        <h3 class="feature-title">Dataset Overview</h3>
        <p class="feature-description">
            Our comprehensive dataset contains detailed information about used cars including:
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
                <strong>🚗 Car Details</strong><br>
                • Model & Brand<br>
                • Manufacturing Year<br>
                • Kilometers Driven
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
                <strong>💰 Pricing</strong><br>
                • Current Market Price<br>
                • Price Trends<br>
                • Value Analysis
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
                <strong>🔧 Specifications</strong><br>
                • Fuel Type<br>
                • Transmission<br>
                • Car Category
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
                <strong>📍 Location</strong><br>
                • RTO Location<br>
                • Regional Data<br>
                • Market Variations
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Technology Stack
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">⚙️</span>
        <h3 class="feature-title">Technology Stack</h3>
        <p class="feature-description">
            Built with modern technologies for optimal performance and user experience:
        </p>
        <div class="tech-stack">
            <span class="tech-item">Python</span>
            <span class="tech-item">Streamlit</span>
            <span class="tech-item">Pandas</span>
            <span class="tech-item">Plotly</span>
            <span class="tech-item">Scikit-learn</span>
            <span class="tech-item">NumPy</span>
            <span class="tech-item">SciPy</span>
            <span class="tech-item">HTML/CSS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Development Timeline
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📅</span>
        <h3 class="feature-title">Development Journey</h3>
        <div class="timeline">
            <div class="timeline-item">
                <h4>Phase 1: Data Collection & Preprocessing</h4>
                <p>Web scraping, data cleaning, and feature engineering to create a robust dataset.</p>
            </div>
            <div class="timeline-item">
                <h4>Phase 2: Exploratory Data Analysis</h4>
                <p>Comprehensive analysis to understand market patterns, correlations, and trends.</p>
            </div>
            <div class="timeline-item">
                <h4>Phase 3: Machine Learning Integration</h4>
                <p>Development of predictive models and advanced analytics features.</p>
            </div>
            <div class="timeline-item">
                <h4>Phase 4: Interactive Dashboard</h4>
                <p>Creation of user-friendly interface with real-time visualizations and insights.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Future Roadmap
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🚀</span>
        <h3 class="feature-title">Future Enhancements</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1.5rem; border-radius: 15px;">
                <h4>🤖 Advanced AI</h4>
                <p>Deep learning models for even more accurate predictions</p>
            </div>
            <div style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; padding: 1.5rem; border-radius: 15px;">
                <h4>📱 Mobile App</h4>
                <p>Native mobile application for on-the-go access</p>
            </div>
            <div style="background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; padding: 1.5rem; border-radius: 15px;">
                <h4>🔐 User Authentication</h4>
                <p>Personalized experiences and saved preferences</p>
            </div>
            <div style="background: linear-gradient(135deg, #43e97b, #38f9d7); color: white; padding: 1.5rem; border-radius: 15px;">
                <h4>📈 Real-time Data</h4>
                <p>Live market data integration and updates</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Contact Section
    st.markdown("""
    <div class="contact-section">
        <h2>💬 Get in Touch</h2>
        <p>Have questions, suggestions, or want to collaborate? We'd love to hear from you!</p>
        <div style="margin-top: 1rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">
                📧 Email: contact@recnrev.com
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">
                🌐 Website: www.recnrev.com
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666; font-size: 0.9rem;">
        <p>🚗 Built with ❤️ for the automotive community | © 2025 RECnREV</p>
    </div>
    """, unsafe_allow_html=True)

# Call the app function
app()