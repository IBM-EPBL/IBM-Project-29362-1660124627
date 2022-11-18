import numpy as np
import pickle


from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

from Prediction import *

regressor = RandomForestRegressor(n_estimators=1000, max_depth=10, random_state=34)
print(regressor)
regressor.fit(X_train, np.ravel(Y_train, order='C'))
print(regressor)
y_pred = regressor.predict(X_test)

print(r2_score(Y_test, y_pred))

filename = 'resale_model.sav'
pickle.dump(regressor, open(filename, 'wb'))