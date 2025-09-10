"""
   pip install -r requirements.txt
   streamlit run app.py
"""

import streamlit as st
from data_utils import load_data
from model_utils import train_models   # Import train_models
from ui_utils import apply_custom_css, plot_distributions
from evaluate_model import evaluate_models

# -------------------------
# Page Config & CSS
# -------------------------
st.set_page_config(page_title="Smart Electricity Calculator", page_icon="⚡", layout="wide")
apply_custom_css()

# -------------------------
# Title
# -------------------------
st.markdown('<h1 class="main-header">⚡ Smart Electricity Calculator</h1>', unsafe_allow_html=True)
st.markdown("This AI-powered tool predicts your electricity bill, consumption, connected load, system size, and load class.")

# -------------------------
# Data
# -------------------------
data = load_data("data/hackathon.csv")   # path to your uploaded dataset


# -------------------------
# Sidebar: Model selection
# -------------------------
st.sidebar.header("⚙️ Model Settings")
model_choice = st.sidebar.selectbox(
    "Choose a model type:",
    ["Linear Regression", "Decision Tree", "Random Forest", "XGBoost"]
)

model_type_map = {
    "Linear Regression": "linear",
    "Decision Tree": "decision_tree",
    "Random Forest": "random_forest",
    "XGBoost": "xgboost"
}

# Train models based on selection
models = train_models(data, model_type=model_type_map[model_choice])


performance = evaluate_models(data, models)

# Show results in sidebar
st.sidebar.subheader("📊 Model Performance")
for task, metrics in performance.items():
    st.sidebar.markdown(f"**{task}**")
    st.sidebar.write(f"R²: {metrics['R²']:.3f}")
    st.sidebar.write(f"MAE: {metrics['MAE']:.2f}")
    st.sidebar.write(f"RMSE: {metrics['RMSE']:.2f}")
    st.sidebar.markdown("---")

# -------------------------
# Input Section
# -------------------------
st.markdown('<div class="input-section"><h3 class="sub-header">Enter Your Electricity Data</h3>', unsafe_allow_html=True)
input_option = st.radio("Select input:", ["Connected Load (kW)", "Units Consumed (kWh)", "Electricity Bill (₹)"], horizontal=True)
input_value = st.number_input(f"Enter your {input_option}", min_value=0.0, format="%.2f")
predict_button = st.button("Predict")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Predictions
# -------------------------
if predict_button and input_value > 0:
    if input_option == "Connected Load (kW)":
        load = input_value
        consumption = models['load_to_consumption'].predict([[load]])[0]
        bill = models['load_to_bill'].predict([[load]])[0]
    elif input_option == "Units Consumed (kWh)":
        consumption = input_value
        load = models['consumption_to_load'].predict([[consumption]])[0]
        bill = models['consumption_to_bill'].predict([[consumption]])[0]
    else:
        bill = input_value
        load = models['bill_to_load'].predict([[bill]])[0]
        consumption = models['bill_to_consumption'].predict([[bill]])[0]

    # -------------------------
    # New: System Size (rule-based)
    # -------------------------
    # Assumption: 1 kW system ≈ 120 kWh/month
    system_size = consumption / 120  

    # Load Class
    if load < 5:
        load_class = "Low"
    elif load < 10:
        load_class = "Medium"
    else:
        load_class = "High"

    # Show results
    st.markdown('<div class="prediction-box"><h3 class="sub-header">Prediction Results</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Connected Load", f"{load:.2f} kW")
    col2.metric("Units Consumed", f"{consumption:.2f} kWh")
    col3.metric("Electricity Bill", f"₹{bill:.2f}")
    col4.metric("System Size", f"{system_size:.2f} kW")  # ✅ New Output
    st.markdown(f"**Load Class:** {load_class}")  # ✅ Show Load Class
    st.markdown('</div>', unsafe_allow_html=True)

    # Plot distributions
    plot_distributions(data, load, consumption, bill)

    # -------------------------
    # Insights Section
    # -------------------------
    st.markdown('<div class="prediction-box"><h3 class="sub-header">Insights</h3>', unsafe_allow_html=True)

    avg_load = data['LOAD'].mean()
    avg_consumption = data['CONSUMPTION_KWH'].mean()
    rate = bill / consumption if consumption > 0 else 0
    utilization = consumption / load if load > 0 else 0

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
        f"""
        <div style="background-color:#E6F2FF; padding:15px; border-radius:10px; margin-bottom:10px;">
            <b>Load Analysis:</b> Your connected load of {load:.2f} kW is {"above" if load > avg_load else "below"} the average.
        </div>
        """,
        unsafe_allow_html=True
        )

        st.markdown(
        f"""
        <div style="background-color:#E6F2FF; padding:15px; border-radius:10px; margin-bottom:10px;">
            <b>Consumption Analysis:</b> Your consumption of {consumption:.2f} kWh is {"above" if consumption > avg_consumption else "below"} the average.
        </div>
        """,
        unsafe_allow_html=True
        )

    with col2:
        st.markdown(
        f"""
        <div style="background-color:#E6F2FF; padding:15px; border-radius:10px; margin-bottom:10px;">
            <b>Cost Efficiency:</b> Your electricity rate is ₹{rate:.2f} per kWh.
        </div>
        """,
        unsafe_allow_html=True
       )

        st.markdown(
        f"""
        <div style="background-color:#E6F2FF; padding:15px; border-radius:10px; margin-bottom:10px;">
            <b>Load Utilization:</b> You're using {utilization:.2f} kWh per kW of connected load.
        </div>
        """,
        unsafe_allow_html=True
        )

    # -------------------------
    # How It Works Section
    # -------------------------
    st.subheader("How It Works")

    st.markdown("""
    This AI-powered calculator uses machine learning models trained on electricity consumption data to predict:

    1. **Connected Load** - The total power capacity available to your premises (in kW)  
    2. **Units Consumed** - Your electricity consumption (in kWh)  
    3. **Electricity Bill** - The amount you'll be charged (in ₹)  
    4. **System Size** - Estimated solar PV system size (in kW) needed to meet your usage  
    5. **Load Class** - Categorized as Low / Medium / High based on your connected load  

    Simply enter any one of these values, and our system will accurately predict the others based on patterns learned from historical data.
    """)

    st.markdown("---")
    st.markdown("<p style='text-align: center;'>Smart Electricity Calculator AI • Powered by Machine Learning</p>", unsafe_allow_html=True)

    