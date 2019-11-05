import pandas as pd
import numpy as np
from joblib import load

model_path = 'tree-cover/model.joblib'
diff_to_colour = {0.0: 'success', 0.1: 'success', 0.2: 'info', 0.3: 'info', 0.4: 'warning', 0.5: 'warning'}


def process_file(file):
    data = pd.read_csv(file)
    data['Predicted'] = get_prediction(data)  # np.round(np.random.rand(len(data), 1), 3)
    data['diff'] = data.apply(lambda row: np.round(np.abs(row['Tree_cover']-row['Predicted']), 1), axis=1)
    data['class'] = data.apply(lambda row: diff_to_colour.get(row['diff'], 'danger'), axis=1)
    data.sort_values(by='diff', inplace=True)
    print(data)
    return data[['class', 'index_number', 'Coordinates', 'Tree_cover', 'Predicted']]


def get_prediction(data):
    feat = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11', 'sr_aerosol', 'pixel_qa']
    model = load(model_path)
    return model.predict(data[feat])


