import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

DATASET_PATH = r'C:\Users\gurme\Downloads\project car\index\cars_24_combined.csv'

@st.cache_data # Cache data to avoid reloading on every rerun
def load_and_preprocess_data(file_path):
    """
    Loads the dataset and performs all necessary preprocessing steps.
    Uses the exact column names provided:
    'Car Name', 'Year', 'Distance', 'Owner', 'Fuel', 'Location', 'Drive', 'Type', 'Price'
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please ensure it's in the correct directory.")
        st.stop() # Stop the app if file is not found
    except Exception as e:
        st.error(f"An error occurred during file loading: {e}")
        st.stop()

    df_cleaned = df.copy()

    # Handle Duplicate Rows
    df_cleaned.drop_duplicates(inplace=True)

    # Clean and Convert 'Price' Column
    if 'Price' in df_cleaned.columns:
        if df_cleaned['Price'].dtype == 'object':
            df_cleaned['Price'] = df_cleaned['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df_cleaned['Price'] = pd.to_numeric(df_cleaned['Price'], errors='coerce')
        df_cleaned.dropna(subset=['Price'], inplace=True) # Drop rows where Price became NaN
    else:
        st.warning("Warning: 'Price' column not found for cleaning. This is a critical column.")

    # Clean and Convert 'Distance' Column
    if 'Distance' in df_cleaned.columns:
        if df_cleaned['Distance'].dtype == 'object':
            df_cleaned['Distance'] = df_cleaned['Distance'].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df_cleaned['Distance'] = pd.to_numeric(df_cleaned['Distance'], errors='coerce')
        df_cleaned.dropna(subset=['Distance'], inplace=True) # Drop rows where Distance became NaN
    else:
        st.warning("Warning: 'Distance' column not found for cleaning. This is a critical column.")

    # Convert 'Year' to Integer and create 'Car Age'
    if 'Year' in df_cleaned.columns:
        df_cleaned['Year'] = pd.to_numeric(df_cleaned['Year'], errors='coerce')
        df_cleaned.dropna(subset=['Year'], inplace=True) # Drop rows with invalid years
        df_cleaned['Year'] = df_cleaned['Year'].astype('Int64') # Use nullable integer type
        current_year = datetime.now().year
        df_cleaned['Car Age'] = current_year - df_cleaned['Year']
        df_cleaned['Car Age'] = df_cleaned['Car Age'].apply(lambda x: max(0, x)).astype(int)
    else:
        st.warning("Warning: 'Year' column not found. 'Car Age' cannot be calculated.")
        df_cleaned['Car Age'] = np.nan # Add as NaN if column missing

    # Handle Missing Values in Categorical Columns (using mode imputation)
    categorical_cols_to_check = ['Owner', 'Location', 'Drive', 'Type', 'Fuel', 'Car Name']
    for col in categorical_cols_to_check:
        if col in df_cleaned.columns and df_cleaned[col].isnull().sum() > 0:
            mode_val = df_cleaned[col].mode()[0]
            df_cleaned[col].fillna(mode_val, inplace=True)
        elif col not in df_cleaned.columns:
            st.warning(f"Warning: Categorical column '{col}' not found for missing value handling.")

    # Final check for critical numerical columns after preprocessing
    df_cleaned.dropna(subset=['Price', 'Distance', 'Car Age'], inplace=True)

    return df_cleaned 