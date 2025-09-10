import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path="data/hackathon.csv"):
    # Read CSV file
    df = pd.read_csv(path)

    # ✅ Ensure required columns exist
    required_cols = ["LOAD", "CONSUMPTION_KWH", "BILLED_AMOUNT"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"CSV must contain columns: {required_cols}")
    
    df["LOAD"] = df["LOAD"].fillna(df["LOAD"].mean())
    df["CONSUMPTION_KWH"] = df["CONSUMPTION_KWH"].fillna(df["CONSUMPTION_KWH"].mean())
    df["BILLED_AMOUNT"] = df["BILLED_AMOUNT"].fillna(df["BILLED_AMOUNT"].mean())
    df['CONSUMPTION_KWH'] = df['CONSUMPTION_KWH'].clip(lower=0)
    df['BILLED_AMOUNT'] = df['BILLED_AMOUNT'].clip(lower=0)

    
    return df
