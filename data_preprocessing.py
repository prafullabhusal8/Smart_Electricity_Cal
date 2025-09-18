from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load → predict Bill + Consumption
def data_train_test_split_L_to_BC(df, test_size=0.2, random_state=42):
    x = df[["LOAD"]]
    y = df[["BILLED_AMOUNT", "CONSUMPTION_KWH"]]
    return train_test_split(x, y, test_size=test_size, random_state=random_state)

# Bill → predict Load + Consumption
def data_train_test_split_B_to_LC(df, test_size=0.2, random_state=42):
    x = df[["BILLED_AMOUNT"]]
    y = df[["LOAD", "CONSUMPTION_KWH"]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    return x_train, x_test, y_train, y_test

# Consumption → predict Load + Bill
def data_train_test_split_C_to_LB(df, test_size=0.2, random_state=42):
    x = df[["CONSUMPTION_KWH"]]
    y = df[["LOAD", "BILLED_AMOUNT"]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    return x_train, x_test, y_train, y_test