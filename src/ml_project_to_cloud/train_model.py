# Script to train machine learning model.
import os
from sklearn.model_selection import train_test_split
from ml.data import process_data
import pandas as pd
import ml.model as model_lib

# Add the necessary imports for the starter code.
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add code to load in the data.
parent_dir = f"{current_dir}/../.."
data = pd.read_csv(f"{parent_dir}/data/census.csv")

# Optional enhancement, use K-fold cross validation
# instead of a train-test split.
train, test = train_test_split(data, test_size=0.20)

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
    train, categorical_features=cat_features, label="salary", training=True
)

# Proces the test data with the process_data function.
print(X_train.shape)
# print(encoder)
# Train and save a model.
model = model_lib.train_model(X_train, y_train)
print(f"params are: {model.best_params_}")


X_test, y_test, _, _ = process_data(
    train,
    categorical_features=cat_features,
    label="salary",
    training=False,
    encoder=encoder,
    lb=lb,
)

print(X_test.shape)
model_pth = f"{parent_dir}/model/model.pickle"

if os.path.isfile(model_pth):
    print("Prev model available")
    prev_model = model_lib.load_model(model_pth)
    pred_prev_model = model_lib.inference(prev_model, X_test)
    precision_prev_model, _, _ = model_lib.compute_model_metrics(
        y_test, pred_prev_model
    )
else:
    print("No prev model")
    precision_prev_model = -1

pred = model_lib.inference(model, X_test)
precision, recall, fbeta = model_lib.compute_model_metrics(y_test, pred)

if precision > precision_prev_model:
    print("Current model is better")
    print("Saving model")
    model_lib.save_model(model, model_pth)
    print(precision, recall, fbeta)
else:
    print("prev model was better, so no saving current model")
