📘 Project Documentation

Title: AI-Powered Electricity Bill & Consumption Predictor

1️⃣ Introduction

Electricity consumption and billing are key aspects of household and industrial energy management. This project provides an AI-powered tool to:

Predict electricity bill, consumption, connected load, and load class.

Provide interactive visualizations to analyze patterns.

Enable decision-making for energy optimization.

The project is built with Python (Streamlit, Scikit-learn, XGBoost) and uses machine learning regression/classification models for prediction.

2️⃣ Objectives

Build a machine learning model that predicts electricity bill and usage.

Provide an easy-to-use web interface via Streamlit.

Visualize predictions with distribution plots to compare against dataset.

Enable users to upload their own CSV dataset for predictions.

3️⃣ Dataset Description

The project uses a dataset (hackathon.csv) with the following columns:

LOAD → Connected load in kW

CONSUMPTION_KWH → Electricity consumption in kWh

BILLED_AMOUNT → Electricity bill in ₹

✅ Dataset can be replaced with custom CSVs having the same structure.

4️⃣ System Architecture

Workflow:

Data Loading

Load CSV dataset using Pandas.

Handle missing values, outliers, and scaling if needed.

Model Training

Train regression models (Linear Regression, Decision Tree, Random Forest, XGBoost).

Evaluate using R², RMSE, MAE.

Prediction

Accept user input (or new data rows).

Predict bill, consumption, and load class.

Visualization

Show histograms of LOAD, CONSUMPTION_KWH, and BILLED_AMOUNT.

Highlight prediction with a red dashed line.

Frontend (Streamlit)

Interactive web app.

File upload / manual input.

Displays results + graphs.

5️⃣ Technologies Used

Programming Language: Python 3.10+

Frontend: Streamlit

Libraries:

pandas, numpy (data handling)

matplotlib, seaborn (visualization)

scikit-learn (ML models & evaluation)

xgboost (advanced ML model)

6️⃣ Implementation
Key Files

app.py → Main Streamlit app.

data_utils.py → Data loading utilities.

model_utils.py → ML model training functions.

evaluate_model.py → Model evaluation (R², RMSE, MAE).

ui_utils.py → Visualization utilities (distributions, feature plots).

Running the Project
# step 1: Create Vertual environment
python -m venv venv 
venv\Scripts\activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the app
streamlit run app.py

7️⃣ Results

Prediction accuracy: Random Forest & XGBoost give the best performance.

Visualization: Histograms clearly show how predictions compare to dataset distribution.

Example:

Input: LOAD=5, CONSUMPTION=300 → Predicted Bill = ₹1200.

The bill falls within the normal range, as shown by the red dashed line.

8️⃣ Use Cases

Electricity Boards → Demand forecasting, load analysis.

Consumers → Estimate upcoming bills, optimize usage.

Smart Grids → AI-based energy monitoring.

9️⃣ Future Enhancements

Add time-series forecasting for monthly bills.

Deploy on Streamlit Cloud / AWS.

Add tariff-wise billing models.

Build a mobile app frontend.
