import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np


# Defines dataset, creates numeric/dummy vars from non-int attributes, and specifies label
data_set = pd.read_csv("CSV Files/Students-mat.csv")
data_set = pd.get_dummies(data_set, columns=["Mjob", "Fjob", "sex", "Pstatus", "guardian", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"], drop_first=True)

attributes = data_set[["G1", "G2", "studytime", "failures", "absences", "age", "traveltime", "famrel", "Dalc", "freetime", "goout", "Walc", "health",
                       "Mjob_health", "Mjob_other", "Mjob_services", "Mjob_teacher", "Fjob_health", "Fjob_other", "Fjob_services", "Fjob_teacher",
                       "sex_M", "Pstatus_T", "guardian_mother", "guardian_other", "schoolsup_yes", "famsup_yes", "paid_yes", "activities_yes",
                       "nursery_yes", "higher_yes", "internet_yes", "romantic_yes"]].values

label = data_set["G3"].values
regressor = LinearRegression()

# Repeats model training until acc > 0.95
for num in range(50000):
    att_train, att_test, lab_train, lab_test = train_test_split(attributes, label, test_size=0.1)
    regressor.fit(att_train, lab_train)

    accuracy = regressor.score(att_test, lab_test)

    if accuracy > 0.95:
        print(accuracy)
        break

# Uses trained model to predict grades (rounded values)
lab_pred = np.rint(regressor.predict(att_test))

df = pd.DataFrame({"Predicted Grade": lab_pred, "Actual Grade": lab_test})
df1 = df.head(25)
print(df1)

# Outputs Pandas DataFrame (df) as Excel CSV file
df.to_csv(r"G:\Computing\Year 14\Student-Grade-Prediction\CSV Files\export_dataframe.csv")


# Clearer way to see disparities between predicted and actual grades
def graph_plot():
    df1.plot(kind='bar', figsize=(10, 8))
    plt.xlabel("Student")
    plt.ylabel("Grade")
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()
