


# Model Card

For additional information see the Model Card paper:
https://arxiv.org/pdf/1810.03993.pdf

## Model Details

This mo

## Intended Use

This model was created to predict the income of a person.

## Training Data

The trainings data was taken from the census page (see [Ethical Considerations](#Ethical-Considerations)). Below you can find a sample of the data

    age         workclass   fnlgt  education  education_num         marital_status         occupation  ...   race     sex capital_gain  capital_loss  hours_per_week  native_country salary
0   39         State-gov   77516  Bachelors             13          Never-married       Adm-clerical  ...  White    Male         2174             0              40   United-States  <=50K
1   50  Self-emp-not-inc   83311  Bachelors             13     Married-civ-spouse    Exec-managerial  ...  White    Male            0             0              13   United-States  <=50K
2   38           Private  215646    HS-grad              9               Divorced  Handlers-cleaners  ...  White    Male            0             0              40   United-States  <=50K
3   53           Private  234721       11th              7     Married-civ-spouse  Handlers-cleaners  ...  Black    Male            0             0              40   United-States  <=50K
4   28           Private  338409  Bachelors             13     Married-civ-spouse     Prof-specialty  ...  Black  Female            0             0              40            Cuba  <=50K
5   37           Private  284582    Masters             14     Married-civ-spouse    Exec-managerial  ...  White  Female            0             0              40   United-States  <=50K
6   49           Private  160187        9th              5  Married-spouse-absent      Other-service  ...  Black  Female            0             0              16         Jamaica  <=50K
7   52  Self-emp-not-inc  209642    HS-grad              9     Married-civ-spouse    Exec-managerial  ...  White    Male            0             0              45   United-States   >50K
8   31           Private   45781    Masters             14          Never-married     Prof-specialty  ...  White  Female        14084             0              50   United-States   >50K
9   42           Private  159449  Bachelors             13     Married-civ-spouse    Exec-managerial  ...  White    Male         5178             0              40   United-States   >50K

[10 rows x 15 columns]

## Evaluation Data

The data was taken from the same sources as the trainings data but split off from the trainigsdata before use.

## Metrics

The metrics over all the slices is listed in the table below

   precision    recall     fbeta
0   0.789966  0.634373  0.703671

The slices war made on the column 'marital_status'

              slice_name precision    recall     fbeta
0          Never-married     0.875  0.410714  0.559028
1     Married-civ-spouse  0.782113  0.668916  0.721099
2               Divorced  0.830409   0.38587  0.526902
3  Married-spouse-absent  0.733333  0.423077  0.536585
4              Separated  0.763158       0.5  0.604167
5      Married-AF-spouse       1.0  0.666667       0.8
6                Widowed  0.888889      0.25  0.390244



## Ethical Considerations

This data can be found on [sources](https://archive.ics.uci.edu/ml/datasets/census+income) and the only bias should be the bias in the data

## Caveats and Recommendations

There are not recommendations at this moment