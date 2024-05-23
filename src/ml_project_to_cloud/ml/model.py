import multiprocessing
import pickle

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import fbeta_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV

NUMBER_OF_CORES_TO_KEEP_FREE = 4


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
        n_jobs=n_cores,
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


def save_model(model, pth="model/model.pickle"):
    """Save model to pickle.


    Args:
        model (): Model to save.
        pth (str): Path of resulting pickle.
    """
    with open(pth, "wb") as file:
        pickle.dump(model, file)


def load_model(pth="model/model.pickle"):
    """Load model from pickle.

    Args:
        pth (str): Path of the pickle file.
    """
    with open(pth, "rb") as file:
        return pickle.load(file)
