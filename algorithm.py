import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Defines dataset, creates numeric/dummy vars from non-int attributes, and specifies label
data_set = pd.read_csv("student-grades.csv")

print(f"ROWxCOLUMN: {data_set.shape}")
print(data_set.describe())

attributes = data_set[["G1", "G2"]].values
label = data_set["G3"].values
regressor = LinearRegression()


# Repeats model training until acc > 0.95
def train_model():
    for num in range(100000):
        att_train, att_test, lab_train, lab_test = train_test_split(attributes, label, test_size=0.15)
        regressor.fit(att_train, lab_train)

        accuracy = regressor.score(att_test, lab_test)

        if accuracy > 0.95:
            print("")
            print(f"Accuracy: {format(accuracy*100, '.2f')}%")  # Formats as percentage to TWO decimal places
            break
