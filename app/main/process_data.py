import pandas as pd
import numpy as np

diff_to_colour = {0.0: 'success', 0.1: 'success', 0.2: 'info', 0.3: 'info', 0.4: 'warning', 0.5: 'warning'}


def process_file(file):
    data = pd.read_csv(file)
    data['Predicted'] = np.round(np.random.rand(len(data), 1), 3)
    data['diff'] = data.apply(lambda row: np.round(np.abs(row['Tree_cover']-row['Predicted']), 1), axis=1)
    data['class'] = data.apply(lambda row: diff_to_colour.get(row['diff'], 'danger'), axis=1)
    data.sort_values(by='diff', inplace=True)
    print(data)
    return data[['class', 'index_number', 'Coordinates', 'Tree_cover', 'Predicted']]



