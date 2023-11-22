import pandas as pd
from scipy.io import arff
import numpy as np
from zzmtrgd.gdmtr import GDMTR


def arrmse(y_true, y_pred):
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    mean_true = np.mean(y_true)
    arrmse_value = rmse / mean_true
    return arrmse_value

data = arff.loadarff('dataset/cal_housing.arff')
df = pd.DataFrame(data[0])

# Factorize the columns data in the dataframe
#for i in df.columns:
#   df[i] = pd.factorize(df[i])[0]
   
# Add the target colums to the list
targets = df.columns[-2:].tolist()

segmentation = 0.6
# Separate the features (X) and targets (y)
X = df.drop(columns = targets, axis = 1)
y = pd.DataFrame(df[targets])

X_train, X_test = np.split(X, [int(segmentation * len(X))]) 
y_train, y_test = np.split(y, [int(segmentation * len(y))])
# Initilizing the model with some parameters
model = GDMTR(epochs=100, verbose=True, learning_rate=0.001)
model.fit(X_train,y_train)
print(y_test.iloc[10])
prediction = model.predict(X_test.iloc[10])
print(prediction)
end_loss = 0

for i in range(len(X_test)):
    prediction = model.predict(X_test.iloc[i])
    end_loss = end_loss + arrmse(prediction,y_test.iloc[i])

print(f'Unseen data :{end_loss/len(X_test)}')

