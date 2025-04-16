"""
Model training module for the Common Assessment Tool.
Trains and saves three models:
- Random Forest Regressor
- Linear Regression
- Decision Tree Regressor
"""

# Standard library imports
import pickle

# Third-party imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

# === RANDOM FOREST ===


def prepare_models():
    """
    Prepare and train the Random Forest model using the dataset.

    Returns:
        RandomForestRegressor: Trained model for predicting success rates
    """
    data = pd.read_csv("app/clients/service/data_commontool.csv")

    feature_columns = [
        "age",
        "gender",
        "work_experience",
        "canada_workex",
        "dep_num",
        "canada_born",
        "citizen_status",
        "level_of_schooling",
        "fluent_english",
        "reading_english_scale",
        "speaking_english_scale",
        "writing_english_scale",
        "numeracy_scale",
        "computer_scale",
        "transportation_bool",
        "caregiver_bool",
        "housing",
        "income_source",
        "felony_bool",
        "attending_school",
        "currently_employed",
        "substance_use",
        "time_unemployed",
        "need_mental_health_support_bool",
    ]

    intervention_columns = [
        "employment_assistance",
        "life_stabilization",
        "retention_services",
        "specialized_services",
        "employment_related_financial_supports",
        "employer_financial_supports",
        "enhanced_referrals",
    ]

    all_features = feature_columns + intervention_columns
    features = np.array(data[all_features])
    targets = np.array(data["success_rate"])

    features_train, _, targets_train, _ = train_test_split(
        features, targets, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(features_train, targets_train)
    return model


# === LINEAR REGRESSION ===


def prepare_linear_regression_model():
    """
    Prepare and train the Linear Regression model using the dataset.

    Returns:
        LinearRegression: Trained model
    """
    data = pd.read_csv("app/clients/service/data_commontool.csv")

    feature_columns = [
        "age",
        "gender",
        "work_experience",
        "canada_workex",
        "dep_num",
        "canada_born",
        "citizen_status",
        "level_of_schooling",
        "fluent_english",
        "reading_english_scale",
        "speaking_english_scale",
        "writing_english_scale",
        "numeracy_scale",
        "computer_scale",
        "transportation_bool",
        "caregiver_bool",
        "housing",
        "income_source",
        "felony_bool",
        "attending_school",
        "currently_employed",
        "substance_use",
        "time_unemployed",
        "need_mental_health_support_bool",
    ]

    intervention_columns = [
        "employment_assistance",
        "life_stabilization",
        "retention_services",
        "specialized_services",
        "employment_related_financial_supports",
        "employer_financial_supports",
        "enhanced_referrals",
    ]

    all_features = feature_columns + intervention_columns
    features = np.array(data[all_features])
    targets = np.array(data["success_rate"])

    features_train, _, targets_train, _ = train_test_split(
        features, targets, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(features_train, targets_train)
    return model


# === DECISION TREE ===


def prepare_decision_tree_model():
    """
    Prepare and train the Decision Tree model using the dataset.

    Returns:
        DecisionTreeRegressor: Trained model
    """
    data = pd.read_csv("app/clients/service/data_commontool.csv")

    feature_columns = [
        "age",
        "gender",
        "work_experience",
        "canada_workex",
        "dep_num",
        "canada_born",
        "citizen_status",
        "level_of_schooling",
        "fluent_english",
        "reading_english_scale",
        "speaking_english_scale",
        "writing_english_scale",
        "numeracy_scale",
        "computer_scale",
        "transportation_bool",
        "caregiver_bool",
        "housing",
        "income_source",
        "felony_bool",
        "attending_school",
        "currently_employed",
        "substance_use",
        "time_unemployed",
        "need_mental_health_support_bool",
    ]

    intervention_columns = [
        "employment_assistance",
        "life_stabilization",
        "retention_services",
        "specialized_services",
        "employment_related_financial_supports",
        "employer_financial_supports",
        "enhanced_referrals",
    ]

    all_features = feature_columns + intervention_columns
    features = np.array(data[all_features])
    targets = np.array(data["success_rate"])

    features_train, _, targets_train, _ = train_test_split(
        features, targets, test_size=0.2, random_state=42
    )

    model = DecisionTreeRegressor(random_state=42)
    model.fit(features_train, targets_train)
    return model


# === SAVE FUNCTION (shared) ===


def save_model(model, filename="model.pkl"):
    """
    Save the trained model to a file.

    Args:
        model: Trained model to save
        filename (str): Name of the file to save the model to
    """
    with open(filename, "wb") as model_file:
        pickle.dump(model, model_file)


# === MAIN: train all models ===


def train_all_models():
    """
    Trains and saves all three models.
    """
    print("Training and saving all models...")

    rf = prepare_models()
    save_model(rf, "model_rf.pkl")

    lr = prepare_linear_regression_model()
    save_model(lr, "model_lr.pkl")

    dt = prepare_decision_tree_model()
    save_model(dt, "model_dt.pkl")

    print("All models saved successfully!")


if __name__ == "__main__":
    train_all_models()
