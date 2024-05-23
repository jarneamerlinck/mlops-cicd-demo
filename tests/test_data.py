from ml_project_to_cloud.ml.data import process_data


def test_process_data(data):
    cat_features = [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
    ]
    X_train, y_train, encoder, lb = process_data(
        data, categorical_features=cat_features, label="salary", training=True
    )

    assert data.shape == (10, 15)
    assert X_train.shape == (10, 33)
    assert len(encoder.categories_) == len(cat_features)
    assert lb.classes_.shape == (2,)
