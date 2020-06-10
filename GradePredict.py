import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

# Imports dataset and assigns X-attributes and y-label
data_set = pd.read_csv("student-mat.csv", sep=";")
attributes = data_set[["G1", "G2", "studytime", "failures", "absences"]].values
label = data_set["G3"].values

att_train, att_test, lab_train, lab_test = train_test_split(attributes, label, test_size=0.2, random_state=0)

regressor = LinearRegression()
regressor.fit(att_train, lab_train)

accuracy = regressor.score(att_test, lab_test)
print(accuracy)

print("Coefficients: \n", regressor.coef_)
print("Intercept: \n", regressor.intercept_)

lab_pred = regressor.predict(att_test)

df = pd.DataFrame({"Actual": lab_test, "Predicted": lab_pred})
df1 = df.head(25)
print(df1)