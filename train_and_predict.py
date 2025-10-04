import pandas
import json
from sklearn import linear_model

df = pandas.read_csv("trainingset.csv")

X = df[['TargetTemperature', 'OutsideTemperature']]
y = df['Input']

model = linear_model.LinearRegression()
model.fit(X, y)

coefficients = {
    'coef': model.coef_.tolist(),
    'intercept': model.intercept_.tolist()
}

with open('model_params.json', 'w') as f:
    json.dump(coefficients, f)

#predictedInput = regr.predict([[21, 10]])

#print(predictedInput)