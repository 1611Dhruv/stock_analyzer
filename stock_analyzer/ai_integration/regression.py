import pickle

import pandas as pd
from sklearn.linear_model import LinearRegression

# Step 1: Read CSV data into a pandas DataFrame
df = pd.read_csv("data.csv", names=["date", "close_price"])

# Step 2: Convert the 'date' column to datetime objects and then to numerical format (days since the start)
df["date"] = pd.to_datetime(df["date"])
df["days"] = (df["date"] - df["date"].min()).dt.days  # Days since the first date

# Step 3: Prepare data for training
X = df[["days"]]  # Features (days since start)
y = df["close_price"]  # Target (close prices)

# Step 4: Create and train the linear regression model
model = LinearRegression()
model.fit(X, y)

# Step 5: Save the trained model as a .pkl file
with open("predictor.pkl", "wb") as file:
    pickle.dump(model, file)

print("Pre-trained model saved as predictor.pkl")

# Step 6: Optionally, print some model details
print(f"Model Coefficient: {model.coef_[0]}")
print(f"Model Intercept: {model.intercept_}")
