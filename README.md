# Customer Churn Prediction

## 📌 Project Overview
This project focuses on predicting customer churn using the Telco Customer Churn dataset.  
The goal is to identify customers who are likely to leave the service, allowing businesses to take preventive actions.

---

## 📊 Dataset
Telco Customer Churn dataset includes:
- Customer demographics
- Services used (Internet, Phone, etc.)
- Billing information
- Contract type
- Target variable: `Churn` (Yes/No)

---

## ⚙️ Project Pipeline

### 1. Data Loading
- Loaded dataset from CSV file

### 2. Data Cleaning
- Converted `TotalCharges` to numeric
- Removed rows with invalid values
- Dropped `customerID` (not useful for prediction)

### 3. Feature Engineering
- Converted binary features to 0/1
- Applied one-hot encoding to categorical variables
- Created numerical feature matrix for modeling

### 4. Train/Test Split
- Used 80/20 split
- Applied `stratify` to preserve class distribution

### 5. Model Training
- Logistic Regression
- Used `StandardScaler` for feature scaling
- Applied `class_weight="balanced"` to handle class imbalance

### 6. Evaluation
- Metrics:
  - Precision
  - Recall
  - F1-score
  - ROC-AUC

- ROC-AUC on holdout set: **~0.83**

### 7. Cross-Validation
- 5-fold cross-validation
- Mean ROC-AUC: **~0.845**

---

## 📈 Exploratory Data Analysis (EDA)

Key observations:
- Customers with **month-to-month contracts** churn more frequently
- Customers using **fiber optic internet** have higher churn rates
- Dataset is **imbalanced**, making accuracy alone unreliable

---

## 🧠 Model Insights

- Logistic Regression outperformed Random Forest on this dataset
- Most important features:
  - `tenure`
  - `MonthlyCharges`
  - `TotalCharges`
- Threshold tuning significantly improved recall for churn detection

---

## ⚖️ Metrics Trade-off

Lowering classification threshold:
- Increased recall (better detection of churn)
- Decreased precision (more false positives)

This trade-off is important in real-world business scenarios.

---

## 📌 Key Learnings

- Importance of proper data preprocessing
- Why scaling matters for linear models
- Why ROC-AUC is more reliable than accuracy for imbalanced data
- Understanding precision vs recall trade-off
- Avoiding data leakage using pipelines
- Using cross-validation for robust evaluation

---

## 🚀 How to Run

From project root:

```bash
python -m src.train
python -m src.evaluate