from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from src.preprocess import load_data, clean_data, split_features_target


def main():
    df = load_data("data/churn.csv")
    df = clean_data(df)
    X, y = split_features_target(df)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=2000, class_weight="balanced"))
    ])

    scores = cross_val_score(
        pipeline,
        X,
        y,
        cv=5,
        scoring="roc_auc"
    )

    print("ROC-AUC scores:", scores)
    print("Mean ROC-AUC:", scores.mean())


if __name__ == "__main__":
    main()