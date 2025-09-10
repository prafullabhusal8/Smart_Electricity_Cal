# evaluate_model.py

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

def evaluate_models(data, models):
    results = {}

    # ---- 1. Load → Consumption / Bill ----
    X_load = data[['LOAD']]
    y_consumption = data['CONSUMPTION_KWH']
    y_bill = data['BILLED_AMOUNT']

    results['Load → Consumption'] = calculate_metrics(
        y_consumption, models['load_to_consumption'].predict(X_load)
    )
    results['Load → Bill'] = calculate_metrics(
        y_bill, models['load_to_bill'].predict(X_load)
    )

    # ---- 2. Consumption → Load / Bill ----
    X_consumption = data[['CONSUMPTION_KWH']]
    y_load = data['LOAD']
    y_bill_from_consumption = data['BILLED_AMOUNT']

    results['Consumption → Load'] = calculate_metrics(
        y_load, models['consumption_to_load'].predict(X_consumption)
    )
    results['Consumption → Bill'] = calculate_metrics(
        y_bill_from_consumption, models['consumption_to_bill'].predict(X_consumption)
    )

    # ---- 3. Bill → Load / Consumption ----
    X_bill = data[['BILLED_AMOUNT']]
    y_load_from_bill = data['LOAD']
    y_consumption_from_bill = data['CONSUMPTION_KWH']

    results['Bill → Load'] = calculate_metrics(
        y_load_from_bill, models['bill_to_load'].predict(X_bill)
    )
    results['Bill → Consumption'] = calculate_metrics(
        y_consumption_from_bill, models['bill_to_consumption'].predict(X_bill)
    )

    return results


def calculate_metrics(y_true, y_pred):
    """Helper function to calculate R², MAE, RMSE."""
    return {
        "R²": r2_score(y_true, y_pred),
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
    }
