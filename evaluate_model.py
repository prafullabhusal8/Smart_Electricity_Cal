from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def evaluate_model(model, x_test, y_test):
    """
    Evaluate model on test set
    Returns dict with metrics for each output
    """
    y_pred = model.predict(x_test)

    # Ensure 2D for consistency
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(-1, 1)

    metrics = {}

    for i, col in enumerate(y_test.columns):
        mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])

        metrics[col] = {
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "R2": round(r2, 4)
        }

    return metrics