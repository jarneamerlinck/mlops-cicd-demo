import numpy

from ml_project_to_cloud.ml.model import compute_model_metrics, inference, train_model


def test_train_model(processed_data):
    X_train, y_train, encoder, lb = processed_data
    model = train_model(X_train, y_train)
    assert model is not None

    pred = inference(model, X_train)
    assert pred is not None
    assert type(pred) is numpy.ndarray

    assert pred.shape[0] == X_train.shape[0]


def test_compute_model_metrics(processed_data):
    X_train, y_train, encoder, lb = processed_data
    model = train_model(X_train, y_train)
    pred = inference(model, X_train)

    precision, recall, fbeta = compute_model_metrics(y_train, pred)
    assert type(precision) is numpy.float64
    assert type(recall) is numpy.float64
    assert type(fbeta) is numpy.float64
