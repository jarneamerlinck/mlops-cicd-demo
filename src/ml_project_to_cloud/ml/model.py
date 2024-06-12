import multiprocessing
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import fbeta_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, train_test_split

from ml_project_to_cloud.ml.data import process_data

NUMBER_OF_CORES_TO_KEEP_FREE = 2


# Optional: implement hyperparameter tuning.
def train_model(X_train, y_train):
    """
    Trains a machine learning model and returns it.

    Inputs
    ------
    X_train : np.array
        Training data.
    y_train : np.array
        Labels.
    Returns
    -------
    model
        Trained machine learning model.
    """
    params = {
        "n_estimators": range(5, 30, 5),
        "max_depth": range(5, 30, 5),
        "learning_rate": np.linspace(0, 1, 11),
    }

    n_cores = multiprocessing.cpu_count() - NUMBER_OF_CORES_TO_KEEP_FREE

    modelGrid = GridSearchCV(
        GradientBoostingClassifier(random_state=0),
        param_grid=params,
        cv=2,
        verbose=2,
        n_jobs=n_cores if n_cores != 0 else 1,
    )
    modelGrid.fit(X_train, y_train)
    return modelGrid


def compute_model_metrics(y, preds):
    """write a machine learning m
    Validates the trained machine learning model using
    precision, recall, and F1.

    Inputs
    ------
    y : np.array
        Known labels, binarized.
    preds : np.array
        Predicted labels, binarized.
    Returns
    -------
    precision : float
    recall : float
    fbeta : float
    """
    fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
    precision = precision_score(y, preds, zero_division=1)
    recall = recall_score(y, preds, zero_division=1)
    return precision, recall, fbeta


def inference(model, X):
    """Run model inferences and return the predictions.

    Inputs
    ------
    model : ???
        Trained machine learning model.
    X : np.array
        Data used for prediction.
    Returns
    -------
    preds : np.array
        Predictions from the model.
    """
    return model.predict(X)


def save_model_card(
    model,
    data,
    slice_feature: str,
    encoder,
    lb,
    pth: str,
    model_details: str,
    model_use: str,
    eval_data: str,
    train_data: str,
    metrics_desc: str,
    ethical_desc: str,
    recommendations: str,
):
    file_content = (
        """


# Model Card

For additional information see the Model Card paper:"""
        + f"""
https://arxiv.org/pdf/1810.03993.pdf

## Model Details

{model_details}

## Intended Use

{model_use}

## Training Data

{train_data}

## Evaluation Data

{eval_data}

## Metrics

{metrics_desc}

## Ethical Considerations

{ethical_desc}

## Caveats and Recommendations

{recommendations}

"""
    )

    with open(pth, "w") as file:
        file.write(file_content)


def save_model(model, lb, encoder, cat_features, pth="model/"):
    """Save model to pickle.


    Args:
        model (): Model to save.
        lb (): Lb to save.
        encoder (): Encoder to save.
        cat_features (list): List of Categorical features to save.
        pth (str): Path of resulting pickle.
    """
    with open(f"{pth}/model.pickle", "wb") as file:
        pickle.dump(model, file)
    with open(f"{pth}/lb.pickle", "wb") as file:
        pickle.dump(lb, file)
    with open(f"{pth}/encoder.pickle", "wb") as file:
        pickle.dump(encoder, file)
    with open(f"{pth}/cat_features.pickle", "wb") as file:
        pickle.dump(cat_features, file)


def load_model(pth="model/"):
    """Load model from pickle.

    Args:
        pth (str): Path of the pickle file.
    """
    with open(f"{pth}/model.pickle", "rb") as file:
        model = pickle.load(file)
    with open(f"{pth}/lb.pickle", "rb") as file:
        lb = pickle.load(file)
    with open(f"{pth}/encoder.pickle", "rb") as file:
        encoder = pickle.load(file)
    with open(f"{pth}/cat_features.pickle", "rb") as file:
        cat_features = pickle.load(file)
    return model, lb, encoder, cat_features


def preformance_over_slice(model, data, slice_feature: str, encoder, lb):

    metric_types = ["slice_name", "precision", "recall", "fbeta"]
    results = pd.DataFrame(columns=metric_types)
    slices = data[slice_feature].unique()
    # print(slices)
    print(f"Performance over slices on {slice_feature}")
    for slice in slices:
        slice_data = data[data[slice_feature] == slice]

        train, test = train_test_split(slice_data, test_size=0.20)

        cat_features = [
            "workclass",
            "education",
            "marital_status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "native_country",
        ]

        X_train, y_train, encoder, lb = process_data(
            train,
            categorical_features=cat_features,
            label="salary",
            training=False,
            encoder=encoder,
            lb=lb,
        )
        slice_pred = inference(model, X_train)
        tuple_values = compute_model_metrics(y_train, slice_pred)
        # print(tuple_values)
        new_row = pd.Series(
            [slice] + list(tuple_values),
            index=metric_types,
        )
        results = pd.concat([results, new_row.to_frame().T], ignore_index=True)
    return results
