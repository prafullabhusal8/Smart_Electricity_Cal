"""
   pip install -r requirements.txt
   streamlit run app.py
"""
import numpy as np
import streamlit as st
from data_cleaning import loaded_data
from data_preprocessing import ( 
    data_train_test_split_L_to_BC,
    data_train_test_split_B_to_LC,
    data_train_test_split_C_to_LB
)
from model_utils import train_model
from evaluate_model import evaluate_model
from ui_utils import apply_custom_css

# -------------------------
# Page Config & CSS
# -------------------------
st.set_page_config(page_title="SMART Cal AI", page_icon="⚡", layout="wide")
apply_custom_css()

# -------------------------
# Title
# -------------------------
st.markdown('<h1 class="main-header">⚡ Smart Electricity Calculator</h1>', unsafe_allow_html=True)
st.markdown("This AI-powered tool predicts your electricity bill, consumption, connected load")


# -------------------------
# Data
# -------------------------
df = loaded_data(r"D:\Intership_Project\Smart_Cal_AI\data_sets\hackathon.csv")   # path to your uploaded dataset

# -------------------------
# Sidebar: Model selection
# -------------------------
st.sidebar.header("⚙️ Model Settings")
model_choice = st.sidebar.selectbox(
    "Choose a model type:",
    ["Linear Regression", "Decision Tree", "Random Forest", "XGBoost"]
)
# -------------------------
# Input Section
# -------------------------
st.markdown('<div class="input-section"><h3 class="sub-header">Enter Your Electricity Data</h3>', unsafe_allow_html=True)
input_option = st.radio("Select input:", ["Load", "CONSUMPTION_KWH", "BILLED_AMOUNT"], horizontal=True)
input_value = st.number_input(f"Enter your {input_option}", min_value=0.0, format="%.4f")
st.markdown('</div>', unsafe_allow_html=True)

# Train/test split based on choice
if input_option == "Load":
    (x_train, x_test, y_train, y_test) = data_train_test_split_L_to_BC(df)
    targets = ["BILLED_AMOUNT", "CONSUMPTION_KWH"]

elif input_option == "BILLED_AMOUNT":
    (x_train, x_test, y_train, y_test) = data_train_test_split_B_to_LC(df)
    targets = ["Load", "CONSUMPTION_KWH"]

elif input_option == "CONSUMPTION_KWH":
    (x_train, x_test, y_train, y_test) = data_train_test_split_C_to_LB(df)
    targets = ["Load", "BILLED_AMOUNT"]


# Train model
model = train_model(x_train, y_train, model_name=model_choice, scaler=False)




if st.button("Predict"):
    input_array = np.array([[input_value]])   # shape = (1, 1)
    preds = model.predict(input_array)[0]
    for target, pred in zip(targets, preds):
        st.success(f"Predicted {target}: {pred:.4f}")

# Evaluate
metrics = evaluate_model(model, x_test, y_test)
st.sidebar.write("📊 Model Performance : ")
st.sidebar.write(metrics)
