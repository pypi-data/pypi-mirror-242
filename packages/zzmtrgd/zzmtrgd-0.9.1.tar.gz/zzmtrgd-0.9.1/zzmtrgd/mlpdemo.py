from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
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

targets = df.columns[-6:].tolist()

# Factorize the columns data in the dataframe
#for i in df.columns:
#   df[i] = pd.factorize(df[i])[0]

X = df.drop(columns = targets, axis = 1)
y = pd.DataFrame(df[targets])

# Assuming X_train, y_train, X_test, y_test are your training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Create an MLPRegressor instance
model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=100, random_state=42)

# Fit the model to the training data
model.fit(X_train, y_train)

print(model.predict(X_test))

loss = np.mean(arrmse ((model.predict(X_test)),y_test))
print(loss)

