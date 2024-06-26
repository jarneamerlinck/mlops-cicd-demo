import numpy

from ml_project_to_cloud.ml.model import (
    compute_model_metrics,
    inference,
    load_model,
    save_model,
    train_model,
)


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


def test_save_model(processed_data, tmp_path):
    X_train, y_train, encoder, lb = processed_data
    cat_features = ["list", "of", "features"]
    model = train_model(X_train, y_train)
    save_model(model, lb, encoder, cat_features, tmp_path)

    tmp_file = tmp_path / "model.pickle"
    assert tmp_file.exists()
    tmp_file = tmp_path / "lb.pickle"
    assert tmp_file.exists()
    tmp_file = tmp_path / "encoder.pickle"
    assert tmp_file.exists()
    tmp_file = tmp_path / "cat_features.pickle"
    assert tmp_file.exists()

    loaded_model, lb, encoder, cat_features = load_model(tmp_path)

    assert type(model) is type(loaded_model)
