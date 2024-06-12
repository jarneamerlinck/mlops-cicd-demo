


# Model Card

For additional information see the Model Card paper:
https://arxiv.org/pdf/1810.03993.pdf

## Model Details

This model predicts if the income of a person is higher then 50K. The used inputs are:
	age
	workclass
	fnlgt
	education
	education_num
	marital_status
	occupation
	relationship
	race
	sex
	capital_gain
	capital_loss
	hours_per_week
	native_country

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

The data was taken from the same sources as the trainings data but split off from the trainigsdata before use. The train test split ratio is 0.2. So the test data is 20% of the full dataset.

## Metrics

The metrics over all the slices is listed in the table below

   precision    recall     fbeta
0   0.819204  0.685587  0.746463

The slices were made on the column 'race'

           slice_name precision    recall     fbeta
0               White  0.809138  0.684469  0.741601
1               Black  0.813559      0.64  0.716418
2  Asian-Pac-Islander     0.805  0.715556  0.757647
3  Amer-Indian-Eskimo  0.888889       0.5      0.64
4               Other  0.777778  0.636364       0.7



## Ethical Considerations

This data can be found on [sources](https://archive.ics.uci.edu/ml/datasets/census+income) and the only bias should be the bias in the data. **The data is based on the year 1994**. So the salary does not include the inflation, there might be a bias towards race. Amer-Indian-Eskimo, and Other races have lower percision then White, Black and Asian-Pac-Islander. This could be because there are a data imbalance.

## Caveats and Recommendations

This model is best if the new data is somewhat similar to the data it's trained on. So passing data from a Country not included in the trainings data will decrease the model performance.
