from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor

def train_model(x_train, y_train, model_name="linear", scaler=True):
    """
    Train model based on choice
    """

    if model_name == "Linear Regression":
        base_model = LinearRegression()

    elif model_name == "Decision Tree":
        base_model = DecisionTreeRegressor(max_depth= 100 ,random_state=42)

    elif model_name == "Random Forest":
        base_model = RandomForestRegressor(n_estimators=100, random_state=42)

    elif model_name == "XGBoost":
        base_model = XGBRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
            n_jobs=-1
        )

    else:
        raise ValueError(f"❌ Unknown model: {model_name}")

    # Wrap in MultiOutput if multiple targets
    model = MultiOutputRegressor(base_model)

    # Optionally add scaler
    if scaler:
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("model", model)
        ])
        pipeline.fit(x_train, y_train)
        return pipeline
    else:
        model.fit(x_train, y_train)
        return model
