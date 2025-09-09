import pandas
from sklearn import linear_model

df = pandas.read_csv("trainingset.csv")

X = df[['TargetTemperature', 'OutsideTemperature']]
y = df['Input']

regr = linear_model.LinearRegression()
regr.fit(X, y)

predictedInput = regr.predict([[21, 10]])

print(predictedInput)