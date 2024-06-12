# Script to train machine learning model.
import os

import pandas as pd
from sklearn.model_selection import train_test_split

import ml_project_to_cloud.ml.model as model_lib
from ml_project_to_cloud.ml.data import clean_data, process_data


def train():
    """Run the training script.

    Made as entrypoint.
    """
    # Add the necessary imports for the starter code.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Add code to load in the data.
    parent_dir = f"{current_dir}/../"
    data = pd.read_csv(f"{parent_dir}../data/census.csv")
    data = clean_data(data)

    # Optional enhancement, use K-fold cross validation
    # instead of a train-test split.
    train, test = train_test_split(data, test_size=0.20)

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
    slice_feature = cat_features[5]

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
    model_pth = f"{current_dir}/model/"
    model_card_pth = f"{current_dir}/model/model_card.md"

    if os.path.isfile(model_pth + "model.pickle"):
        print("Prev model available")
        prev_model, _, _, _ = model_lib.load_model(model_pth)
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
        model_lib.save_model(model, lb, encoder, cat_features, model_pth)
        print(precision, recall, fbeta)
    else:
        print("prev model was better, so no saving current model")

    print("Test preformance on slice")
    slice_results = model_lib.preformance_over_slice(
        model,
        data,
        slice_feature=slice_feature,
        encoder=encoder,
        lb=lb,
    )
    slice_results.to_csv(f"{model_pth}/slice_output.txt")
    metric_types = ["precision", "recall", "fbeta"]

    original_metrics = pd.DataFrame(
        data=[[precision, recall, fbeta]], columns=metric_types
    )

    model_details = (
        "This model predicts if the income of a person"
        + " is higher then 50K. The used inputs are: \n\t"
        + "\n\t".join(train.columns.to_list()[:-1])
    )
    model_use = "This model was created to predict the income of a person."
    eval_data = (
        "The data was taken from the same sources as the trainings data"
        + " but split off from the trainigsdata before use."
        + " The train test split ratio is 0.2."
        + " So the test data is 20% of the full dataset."
    )
    train_data = (
        "The trainings data was taken from the census page"
        + " (see [Ethical Considerations](#Ethical-Considerations))."
        + f" Below you can find a sample of the data\n\n {data[:10]}"
    )
    metrics_desc = (
        "The metrics over all the slices is listed in the table below\n\n"
        + f"{original_metrics}\n\nThe slices were made on the column"
        + f" '{slice_feature}'\n\n{slice_results}\n\n"
    )
    ethical_desc = (
        "This data can be found on"
        + " [sources](https://archive.ics.uci.edu/ml/datasets/census+income)"
        + " and the only bias should be the bias in the data."
        + " **The data is based on the year 1994**. So the salary does"
        + " not include the inflation, there might be a bias towards race."
        + " Amer-Indian-Eskimo, and Other races have lower percision then"
        + " White, Black and Asian-Pac-Islander."
        + " This could be because there are a data imbalance."
    )
    recommendations = (
        "This model is best if the new data is somewhat"
        + " similar to the data it's trained on. So passing data"
        + " from a Country not included in the trainings data will"
        + " decrease the model performance."
    )

    model_lib.save_model_card(
        model,
        data,
        slice_feature=slice_feature,
        encoder=encoder,
        lb=lb,
        pth=model_card_pth,
        model_details=model_details,
        model_use=model_use,
        eval_data=eval_data,
        train_data=train_data,
        metrics_desc=metrics_desc,
        ethical_desc=ethical_desc,
        recommendations=recommendations,
    )


if __name__ == "__main__":
    train()
