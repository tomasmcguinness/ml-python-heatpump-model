import pandas
import json
from sklearn import linear_model

df = pandas.read_csv("trainingset.csv")

X = df[['FlowTemp', 'FlowRate', 'OutsideTemp']]
y = df['Input']

model = linear_model.LinearRegression()
model.fit(X, y)

# Save the model coefficients to a JSON file
coefficients = {
    'coef': model.coef_.tolist(),
    'intercept': model.intercept_.tolist()
}

with open('model_params.json', 'w') as f:
    json.dump(coefficients, f)

predictedInput = model.predict([[32, 14, 8]])

print(predictedInput)