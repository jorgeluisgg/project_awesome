#Imports
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_selector
from sklearn.compose import make_column_transformer

#CLEANING THE DATA:

#drop columns that have more than 30% of missing data:
def remove_shitty_columns(df):
    for column in df.columns:
        if df[column].isnull().sum()/len(df) > 0.3:
            df.drop(columns=[column], inplace=True)
    return df


#drop rows that have more than 30% of missing values
def remove_shitty_rows(df):
    threshold = 0.3 * df.shape[1]  # Calculate the threshold for missing values
    df = df.dropna(thresh=int(df.shape[1] - threshold))
    return df

#FINAL CLEANING FUNCTION
def clean_dataframe(df):
    df = remove_shitty_columns(df)
    df = remove_shitty_rows(df)
    df = df.reset_index(drop=True)
    return df


#PREPROCESSING
def preprocessing_the_data(df):
    #use simple impute with strategy = "constant"
    imputer = SimpleImputer(strategy="constant", fill_value=0)

    #Robust Scaler to Scale data because of outliers
    rb_scaler = RobustScaler()

    #select numerical columns
    num_transformer = make_pipeline(imputer, rb_scaler)
    num_columns = make_column_selector(dtype_exclude="object")

    #Create Preproc Pipeline
    preproc_basic = make_column_transformer((num_transformer, num_columns))

    #Apply Preprocessing to dataframe
    preprocessed_data = preproc_basic.fit_transform(df)

    #Change column names of transformed dataframe
    df_preproc = pd.DataFrame(preprocessed_data, columns=preproc_basic.get_feature_names_out())

    #Merge with tickers
    df_preproc = df_preproc.join(df.Ticker)

    return df_preproc


"""to import in the other file:

from preprocessing import clean_dataframe, preprocessing_the_data

df = clean_dataframe(df)
df = propcessing_the_data(df)

"""
