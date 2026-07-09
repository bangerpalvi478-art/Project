import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import LabelEncoder
from data_utils import load_and_preprocess_data, DATASET_PATH

# Import global styles
with open("assets/global_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page-specific pastel pink/magenta color scheme
st.markdown('''
<style>
:root {
    --main-bg: #fff5fa;
    --main-accent: #fbcfe8;
    --main-accent-dark: #ec4899;
    --main-card: #fbeaf7;
    --main-hero-gradient: linear-gradient(135deg, #fbcfe8 0%, #ec4899 100%);
    --main-feature-card: #fbeaf7;
    --main-feature-title: #ec4899;
    --main-stat-number: #ec4899;
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
        <h1 class="hero-title">🤖 Price Prediction</h1>
        <p class="hero-subtitle">Predict car prices using machine learning models and get insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Prepare data for ML
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🔧 Data Preparation</div>', unsafe_allow_html=True)
    
    # Create a copy for ML
    df_ml = df_cleaned.copy()
    
    # Encode categorical variables
    categorical_cols = ['Type', 'Fuel', 'Drive', 'Owner']
    label_encoders = {}
    
    for col in categorical_cols:
        if col in df_ml.columns:
            le = LabelEncoder()
            df_ml[col + '_encoded'] = le.fit_transform(df_ml[col].astype(str))
            label_encoders[col] = le
    
    # Select features for ML
    feature_cols = ['Year', 'Distance', 'Car Age'] + [col + '_encoded' for col in categorical_cols if col in df_ml.columns]
    feature_cols = [col for col in feature_cols if col in df_ml.columns]
    
    X = df_ml[feature_cols]
    y = df_ml['Price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    st.markdown(f'<div class="feature-description">Prepared {len(feature_cols)} features for {len(df_ml)} cars</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Model selection and training
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🎯 Model Selection & Training</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_type = st.selectbox(
            "Select Model:",
            ["Random Forest", "Linear Regression"]
        )
    
    with col2:
        if model_type == "Random Forest":
            n_estimators = st.slider("Number of Trees:", 50, 200, 100)
            max_depth = st.slider("Max Depth:", 5, 20, 10)
        else:
            n_estimators = 100
            max_depth = 10
    
    # Train model
    if model_type == "Random Forest":
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    else:
        model = LinearRegression()
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Model performance
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-item"><span class="stat-number">{:.3f}</span><div class="stat-label">R² Score</div></div>'.format(r2), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">MAE</div></div>'.format(int(mae)), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-item"><span class="stat-number">₹{:,}</span><div class="stat-label">RMSE</div></div>'.format(int(rmse)), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Model visualization
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📊 Model Performance Visualization</div>', unsafe_allow_html=True)
    
    # Actual vs Predicted
    fig = px.scatter(
        x=y_test,
        y=y_pred,
        title="Actual vs Predicted Prices",
        labels={'x': 'Actual Price (₹)', 'y': 'Predicted Price (₹)'}
    )
    fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], 
                            mode='lines', name='Perfect Prediction', line=dict(dash='dash')))
    st.plotly_chart(fig, use_container_width=True)
    
    # Residuals plot
    residuals = y_test - y_pred
    fig = px.scatter(
        x=y_pred,
        y=residuals,
        title="Residuals Plot",
        labels={'x': 'Predicted Price (₹)', 'y': 'Residuals (₹)'}
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance (for Random Forest)
    if model_type == "Random Forest":
        feature_importance = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        fig = px.bar(
            feature_importance,
            x='Importance',
            y='Feature',
            orientation='h',
            title="Feature Importance"
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Interactive prediction
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">🔮 Interactive Price Prediction</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input features
        year = st.slider("Year:", int(df_cleaned['Year'].min()), int(df_cleaned['Year'].max()), 2020)
        distance = st.slider("Distance (km):", int(df_cleaned['Distance'].min()), int(df_cleaned['Distance'].max()), 50000)
        car_age = 2024 - year
        
        car_type = st.selectbox("Car Type:", sorted(df_cleaned['Type'].unique()))
        fuel_type = st.selectbox("Fuel Type:", sorted(df_cleaned['Fuel'].unique()))
        drive_type = st.selectbox("Transmission:", sorted(df_cleaned['Drive'].unique()))
        owner_type = st.selectbox("Owner:", sorted(df_cleaned['Owner'].unique()))
    
    with col2:
        # Encode inputs
        input_features = [year, distance, car_age]
        for col, value in zip(categorical_cols, [car_type, fuel_type, drive_type, owner_type]):
            if col in label_encoders:
                encoded_value = label_encoders[col].transform([value])[0]
                input_features.append(encoded_value)
        
        # Make prediction
        predicted_price = model.predict([input_features])[0]
        
        # Confidence interval (for Random Forest)
        if model_type == "Random Forest":
            predictions = []
            for _ in range(100):
                sample_indices = np.random.choice(len(X_train), len(X_train), replace=True)
                sample_model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=None)
                sample_model.fit(X_train.iloc[sample_indices], y_train.iloc[sample_indices])
                predictions.append(sample_model.predict([input_features])[0])
            
            confidence_interval = np.percentile(predictions, [5, 95])
            st.markdown(f'<div class="stat-item"><span class="stat-number">₹{predicted_price:,.0f}</span><div class="stat-label">Predicted Price</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="feature-description">95% Confidence: ₹{confidence_interval[0]:,.0f} - ₹{confidence_interval[1]:,.0f}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="stat-item"><span class="stat-number">₹{predicted_price:,.0f}</span><div class="stat-label">Predicted Price</div></div>', unsafe_allow_html=True)
        
        # Show similar cars
        similar_cars = df_cleaned[
            (df_cleaned['Type'] == car_type) &
            (df_cleaned['Fuel'] == fuel_type) &
            (df_cleaned['Year'] >= year - 2) &
            (df_cleaned['Year'] <= year + 2)
        ].head(5)
        
        if not similar_cars.empty:
            st.markdown('<div class="feature-title">Similar Cars for Reference:</div>', unsafe_allow_html=True)
            for _, car in similar_cars.iterrows():
                st.write(f"• {car['Car Name']}: ₹{car['Price']:,.0f} ({car['Year']})")
    st.markdown('</div>', unsafe_allow_html=True)

    # Model comparison
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">📈 Model Comparison</div>', unsafe_allow_html=True)
    
    # Train both models for comparison
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    lr_model = LinearRegression()
    
    rf_model.fit(X_train, y_train)
    lr_model.fit(X_train, y_train)
    
    rf_pred = rf_model.predict(X_test)
    lr_pred = lr_model.predict(X_test)
    
    # Compare metrics
    comparison_data = {
        'Model': ['Random Forest', 'Linear Regression'],
        'R² Score': [r2_score(y_test, rf_pred), r2_score(y_test, lr_pred)],
        'MAE': [mean_absolute_error(y_test, rf_pred), mean_absolute_error(y_test, lr_pred)]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            comparison_df,
            x='Model',
            y='R² Score',
            title="R² Score Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            comparison_df,
            x='Model',
            y='MAE',
            title="Mean Absolute Error Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Price prediction insights
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">💡 Price Prediction Insights</div>', unsafe_allow_html=True)
    
    # Price trends by features
    insights_data = []
    for col in ['Type', 'Fuel', 'Drive', 'Owner']:
        if col in df_cleaned.columns:
            avg_prices = df_cleaned.groupby(col)['Price'].mean().sort_values(ascending=False)
            insights_data.append({
                'Feature': col,
                'Highest': f"{avg_prices.index[0]} (₹{avg_prices.iloc[0]:,.0f})",
                'Lowest': f"{avg_prices.index[-1]} (₹{avg_prices.iloc[-1]:,.0f})"
            })
    
    insights_df = pd.DataFrame(insights_data)
    st.dataframe(insights_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download prediction results
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    # Create results dataframe
    results_df = pd.DataFrame({
        'Actual': y_test,
        'Predicted': y_pred,
        'Residuals': residuals
    })
    
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Prediction Results (CSV)",
        data=csv,
        file_name=f'price_prediction_results_{model_type.lower().replace(" ", "_")}.csv',
        mime='text/csv'
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.success("Price prediction analysis completed! Try different models and parameters above. 🤖")

# Call the app function
app() 