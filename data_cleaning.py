import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats

@st.cache_data
def loaded_data(path=r"D:\Intership_Project\Smart_Cal_AI\data_sets\hackathon.csv"):
    # read csv 
    df = pd.read_csv(path)

    # ✅ Ensure required columns exist
    required_cols = ["LOAD", "CONSUMPTION_KWH", "BILLED_AMOUNT"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"CSV must contain columns: {required_cols}")
    
    df = df[(df['LOAD'] != 0) & (df['CONSUMPTION_KWH'] != 0) & (df['BILLED_AMOUNT'] != 0)]
    
    # 1. LOAD → median per SDO_CODE
    df['LOAD'] = df.groupby('SDO_CODE')['LOAD'].transform(lambda x: x.fillna(x.median()))

    # 2. CONSUMPTION_KWH → average of previous months if available
    df['CONSUMPTION_KWH'] = df['CONSUMPTION_KWH'].fillna((df['CONSUMPTION_PREV_MNTH'] + df['CONSUMPTION_PREV_TO_PREV_MNTH']) / 2)

    # Still missing? fill with group median
    # df['CONSUMPTION_KWH'].ffill(inplace=True)

    # 3. Previous months → median
    df['CONSUMPTION_PREV_MNTH'] = df['CONSUMPTION_PREV_MNTH'].fillna(df['CONSUMPTION_PREV_MNTH'].median())
    df['CONSUMPTION_PREV_TO_PREV_MNTH'] = df['CONSUMPTION_PREV_TO_PREV_MNTH'].fillna(df['CONSUMPTION_PREV_TO_PREV_MNTH'].median())

    # 4. NO_OF_AC → drop (too many missing)
    df = df.drop(columns=['NO_OF_AC'])

    # 5. LAT & LON → median per SDO_CODE (or drop if not important)
    df['LAT'] = df.groupby('SDO_CODE')['LAT'].transform(lambda x: x.fillna(x.median()))
    df['LON'] = df.groupby('SDO_CODE')['LON'].transform(lambda x: x.fillna(x.median()))
    
    # 6. Target variable → drop missing
    df['BILLED_AMOUNT'] = df['BILLED_AMOUNT'].fillna(df['BILLED_AMOUNT'].median())

    df[df['BILLED_AMOUNT'] >= 0]

    df = df[["LOAD","CONSUMPTION_KWH","BILLED_AMOUNT"]]

    for col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5*IQR
        upper_bound = Q3 + 1.5*IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    return df



