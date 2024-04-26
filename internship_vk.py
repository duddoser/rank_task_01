# -*- coding: utf-8 -*-
"""Internship_vk.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V9bksMa4bHPNugsKp2Y5cHmkII2Y9Izs
"""

!pip install catboost

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from catboost import CatBoostRanker, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score

data = pd.read_csv('intern_task.csv', sep=',')

print(data.info())
data.head(5)

df = data[data.isna().any(axis=1)]
df

"""Как видно, только в одной строке присутствуют значения NaN, поэтому просто отбросим найденную строку."""

data = data.dropna()
data = data.drop_duplicates()

for col in data.columns:
  if data[col].dtype != np.int64 and data[col].dtype != np.float64:
    print(col)
data = data.astype({'feature_119': 'float64'})

data['feature_119'].unique()

fig = plt.figure(figsize= (15,10))
sns.heatmap(data, cmap='Blues')
plt.show()

unique_items = data[2:].nunique()
good_cols = [i + 2 for i in range(144) if unique_items[i] > 40]
good_cols = [0, 1] + good_cols
data = data.iloc[:, good_cols]

"""Нужно сгруппировать по query_id."""

X_train, X_test, y_train, y_test = train_test_split(data.drop('rank', axis=1),
                                                    data['rank'],
                                                    train_size=0.7,
                                                    random_state=42)
df_train = pd.DataFrame.join(X_train, y_train, how='left')
df_test = pd.DataFrame.join(X_test, y_test, how='left')
df_train = df_train.sort_values(by='query_id')
df_test = df_test.sort_values(by='query_id')

target = ['rank']
features = data.columns[2:]

train_pool = Pool(
    data = df_train[features],
    label = df_train[target],
    group_id = df_train['query_id'].tolist()
)

test_pool = Pool(
    data = df_test[features],
    label = df_test[target],
    group_id = df_test['query_id'].tolist()
)

model = CatBoostRanker(loss_function='YetiRank',
                       verbose=100,
                       random_seed=42)
model.fit(train_pool, early_stopping_rounds=100)
result = model.predict(test_pool)

model_ndcg = ndcg_score(
    [df_test[target].values.reshape((len(df_test[target].values),)).tolist()],
     [result.tolist()])
model_ndcg

g = []
for i in unique_items:
  if i > 200:
    g.append(i)
print(len(g))