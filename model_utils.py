# model_utils.py

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb   
import streamlit as st

@st.cache_resource
def train_models(data, model_type="random_forest"):
    models = {}

    # Choose model class
    if model_type == "linear":
        ModelClass = LinearRegression
    elif model_type == "decision_tree":
        ModelClass = DecisionTreeRegressor
    elif model_type == "random_forest":
        ModelClass = RandomForestRegressor
    elif model_type == "xgboost":
        ModelClass = xgb.XGBRegressor
    else:
        raise ValueError("Invalid model_type. Choose linear, decision_tree, random_forest, or xgboost.")

    # Otherwise → train models
    X_load = data[['LOAD']]
    y_consumption_from_load = data['CONSUMPTION_KWH']
    y_bill_from_load = data['BILLED_AMOUNT']

    X_consumption = data[['CONSUMPTION_KWH']]
    y_load_from_consumption = data['LOAD']
    y_bill_from_consumption = data['BILLED_AMOUNT']

    X_bill = data[['BILLED_AMOUNT']]
    y_load_from_bill = data['LOAD']
    y_consumption_from_bill = data['CONSUMPTION_KWH']

    models['load_to_consumption'] = ModelClass().fit(X_load, y_consumption_from_load)
    models['load_to_bill'] = ModelClass().fit(X_load, y_bill_from_load)
    models['consumption_to_load'] = ModelClass().fit(X_consumption, y_load_from_consumption)
    models['consumption_to_bill'] = ModelClass().fit(X_consumption, y_bill_from_consumption)
    models['bill_to_load'] = ModelClass().fit(X_bill, y_load_from_bill)
    models['bill_to_consumption'] = ModelClass().fit(X_bill, y_consumption_from_bill)

    return models
