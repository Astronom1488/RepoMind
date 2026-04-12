import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna()

    df = df.drop(columns=["customerID"])

    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    binary_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling"]
    for col in binary_cols:
        df[col] = df[col].map({"Yes": 1, "No": 0})

    df["gender"] = df["gender"].map({"Male": 1, "Female": 0})

    df = pd.get_dummies(df, drop_first=True)

    return df


def split_features_target(df: pd.DataFrame):
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    return X, y