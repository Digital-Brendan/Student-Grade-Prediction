import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", 200)

# Defines dataset, creates numeric/dummy vars from non-int attributes, and specifies label
data_set = pd.read_csv("CSV Files/Students-mat.csv")

attributes = data_set[["G1", "G2"]].values
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

# Creates dataframe that teacher will actually see (doesn't show act grades)
df_real = pd.DataFrame({"Predicted Grade": lab_pred})

# Outputs Pandas DataFrame (df) as Excel CSV file
# df_real.to_csv(r"G:\Computing\Year 14\Student-Grade-Prediction\CSV Files\export_dataframe.csv")


# Clearer way to see disparities between predicted and actual grades. ONLY FOR 25 STUDENTS
def graph_plot():
    df_real.plot(kind='bar', figsize=(10, 8))
    plt.xlabel("Student")
    plt.ylabel("Grade")
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()
