import shap
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np


import xgboost as xg
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score, median_absolute_error, make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, RandomizedSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, PowerTransformer, FunctionTransformer


# Local
PATH_TO_SRC = Path('../src').resolve()
sys.path.append(PATH_TO_SRC.as_posix())


PATH_TO_DATA = Path('../data').resolve()
PATH_TO_RES = Path('./results').resolve()
PATH_TO_FIGS = Path('./figures').resolve()
os.makedirs(PATH_TO_RES, exist_ok=True)
os.makedirs(PATH_TO_FIGS, exist_ok=True)

RANDOM_STATE = 78239


# ----- Load data
ds = pd.read_csv(PATH_TO_DATA / 'sample_metadata.csv', nrows=50)
db = pd.read_csv(PATH_TO_DATA / 'bacteria_table.csv', nrows=50)

# ----- Preprocess
ds['yield_location'] = ds['yield_location'].str.replace(';', ',').str.replace('_', ',')


def extract_yield(y: str):
    return float(y.split(',')[0])


ds['yield'] = ds['yield_location'].apply(extract_yield)


# ----- Categorise good/bad samples
# # 1. categorise samples into good and bad
yield_quantiles = ds['yield'].quantile([.5, .8, .9])
yield_threshold = ds['yield'].quantile(.8)


def get_80p(x, q=.8):
    return np.quantile(x, q)


cols_category = ['sample_type', 'system_type', 'customer_type']
dyield_threshold = ds.groupby(cols_category).agg(
    {'yield': get_80p}
).reset_index().rename(
    columns={'yield': 'yield_threshold'})

ds = ds.merge(
    dyield_threshold,
    how='left',
    on=cols_category
)
ds['yield_threshold'] = ds['yield_threshold'].fillna(ds['yield'].quantile(.8))
ds['yield_category'] = (ds['yield'] >= ds['yield_threshold']).astype(int)

df = db.rename(columns={'Unnamed: 0': 'sample_id'}).set_index('sample_id').T
df = df.reset_index().rename(columns={'index': 'sample_id'})
df = df.merge(ds[['sample_id', 'yield_category', 'yield']], on='sample_id', how='inner')


# Model train
cols_num = [c for c in df.columns if c.startswith('BACT_')]
cols_feature = cols_num

scaler = ColumnTransformer([
    ('standard_sc', StandardScaler(), cols_num),
], remainder='passthrough')
# scaler.fit(df[cols_feature])
# df_transf = pd.DataFrame(
#     scaler.transform(df[cols_feature]),
#     columns=cols_feature
# )

regressor = ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=RANDOM_STATE)
pipeline = Pipeline([('scaler', scaler), ('regressor', regressor)])

col_target = 'yield'
df_train, df_test, y_train, y_test = train_test_split(
    df[cols_feature],
    df[col_target].values.reshape(-1, 1),
    test_size=.3, random_state=RANDOM_STATE)
pipeline.fit(df_train, y_train)

# evaluate the model
y_pred = pipeline.predict(df_test)
# Calculate evaluation metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# Print results
print(f'R² Score: {r2:.4f}')
print(f'Mean Absolute Error (MAE): {mae:.4f}')


regressor = GradientBoostingRegressor()
regressor.fit(df_train, y_train)

#  explainer = shap.Explainer(pipeline)
explainer = shap.Explainer(regressor)
shap_values = explainer.shap_values(df_test.values)
shap.plots.bar(shap_values)

df_recommendation = pd.DataFrame(data=dict(
    bacteria=cols_feature,
    shap_avg=shap_values.mean(axis=0)
))

print('these are the 5 most important bacteria (as when missing, the yield decreases most on average)')
df_recommendation.sort_values(by='shap_avg', ascending=True).head()
