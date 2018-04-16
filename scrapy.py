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
import numpy as np

dfs = pd.read_excel('data_excel.xlsx', sheet_name=0)
my_np = dfs.loc[dfs['Outgoing:']>=0,['Indegree Centrality','Outdegree Centrality','PageRank Score',
                                     'Payment words:','Session words:']].values
print(my_np)
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state = 3)
print(X_train)
clf = DecisionTreeClassifier().fit(X_train, y_train)

print('Accuracy of Decision Tree classifier on training set: {:.2f}'
    .format(clf.score(X_train, y_train)))
print('Accuracy of Decision Tree classifier on test set: {:.2f}'
    .format(clf.score(X_test, y_test)))