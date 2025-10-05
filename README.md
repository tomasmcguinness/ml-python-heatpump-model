# Simple Heat Pump Machine Learning Model

This repo contains some Machine Learning experiments I'm doing in an effort to build a simple input prediction model.

The goal is to build a dataset using data from HeatPumpMonitor.org and use that to train a model. The model can then predict the power consumption of a heat pump at given indoor and outdoor temperatures.

I want to use this model in my work on Matter Device Energy Management.

> [!NOTE]
> This model is *very* simple as I'm an ML novice. I hope to make it richer as I understand more.

## Running it.

Everything is done using Python 3. 

To get started, install the Python libraries. 

```
pip install -r requirements.txt
```

Then, generate the trainingset.csv file by running build_trainingset.py. This will pull down data for all public Vaillant aroTHERM 5kW heat pumps into a file called trainingset.csv.

```
python build_trainingset.py
```

To then run a prediction, execute train_and_predict.py. The code will build a multiple regression model and predict the input based on 21°C inside temp and a 10°C outside temp.

```
python train_and_predict.py
```

Play around with the values to test different combinations.

## Save

I have include some code to save the model as JSON, so I could use it in another project https://github.com/tomasmcguinness/matter-js-heat-pump 

