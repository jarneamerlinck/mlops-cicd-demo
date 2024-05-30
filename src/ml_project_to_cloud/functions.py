def parse_data_for_predict(df):
    df.columns = df.columns.str.replace("-", "_")
    df = df.drop(columns=["salary"])
    return df
