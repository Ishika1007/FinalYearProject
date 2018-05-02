import pandas as pd
from sklearn import datasets
'''
iris = datasets.load_iris()

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

dfs = pd.read_excel('data_excel.xlsx', sheet_name=0)
sorted = dfs.sort_values(['Incoming:'], ascending=False)
print(sorted)
sorted['Incoming:'].head(10).plot(kind="barh")
plt.show()
'''
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
reg = linear_model.LinearRegression()
dfs = pd.read_excel('ZEROWEBAPP.xls', sheet_name=0)

features = dfs.loc[dfs['Indegree Centrality']>=0,['Indegree Centrality','Payment words:','Session words:','Method:']].values


iris = load_iris()
#X_train, X_test, y_train, y_test = train_test_split(features, value, random_state = 3)
#clf = DecisionTreeClassifier().fit(X_train, y_train)
#regr_1 = DecisionTreeRegressor()
value = list(dfs['Fscore'].values)

reg.fit(features, value)
print(reg.coef_)
print(reg.intercept_)