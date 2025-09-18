import streamlit as st
import matplotlib.pyplot as plt

def apply_custom_css():
    st.markdown("""
    <style>
        .main-header { font-size: 3rem; color: #0068cf; text-align: center; margin-bottom: 2rem; }
        .sub-header { font-size: 1.5rem; color: #0068cf; margin-bottom: 1rem; }
        .prediction-box { background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #0068cf; margin-bottom: 20px; }
        .input-section { background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .stButton>button { background-color: #0068cf; color: white; font-weight: bold; border: none; padding: 0.5rem 1rem; border-radius: 5px; margin-top: 1rem; }
        .stButton>button:hover { background-color: #0054a8; }
    </style>
    """, unsafe_allow_html=True)