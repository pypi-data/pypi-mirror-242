from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from scipy.io import arff
import pandas as pd
import numpy as np

def arrmse(y_true, y_pred):
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    mean_true = np.mean(y_true)
    arrmse_value = rmse / mean_true
    return arrmse_value

data = arff.loadarff('dataset/cal_housing.arff')
df = pd.DataFrame(data[0])

targets = df.columns[-3:].tolist()

# Factorize the columns data in the dataframe
#for i in df.columns:
#   df[i] = pd.factorize(df[i])[0]

X = df.drop(columns = targets, axis = 1)
y = pd.DataFrame(df[targets])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
# Create a Ridge regression model
model = Ridge(alpha=1.0)

# Fit the model to the training data
model.fit(X_train, y_train)

print(model.predict(X_test))
# Make predictions on new data
loss = np.mean(arrmse ((model.predict(X_test)),y_test))
print(loss)