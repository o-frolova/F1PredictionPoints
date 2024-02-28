import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from loaddata import get_information
import seaborn as sns
import matplotlib.pyplot as plt
import os


df_drivers = pd.read_csv('../DataCollection/archive/drivers.csv')
model = CatBoostClassifier()   
model.load_model('../model_predict')

def get_prediction(year, grandPrix):
    inputs, GrandPrixName = get_information(year, grandPrix)
    try:
        probability = model.predict_proba(inputs.drop('TeamColor', axis = 1))
        results = []
        for index, row in inputs.iterrows():
            results.append(df_drivers[df_drivers['driverId'] == row['DriverId']]['code'].tolist()[0])

        output = []
        for i in range(len(results)):
            output.append((results[i], round(100 * probability[i][1], 2), inputs['TeamColor'][i]))
        
        output = sorted(output, key=lambda x: x[1])
        output = pd.DataFrame(output, columns=['Driver', 'Probability of points', 'TeamColor'])

        return output, GrandPrixName
    except:
        return 'К сожалению, данные не доступны.', 0

def visualization_of_the_results(data, grandPrix):
    plt.rcdefaults()
    plt.switch_backend('Agg')
    sns.set_style('darkgrid')
    sns.set(font_scale=1.3)

    colors = ['#' + color if color != '' else sns.color_palette("husl", n_colors=len(data['TeamColor']))[index] for index, color in enumerate(data['TeamColor'])]

    for index, row in data.iterrows():
        plt.hlines(y=index, xmin=0, xmax=row['Probability of points'], color=colors[index], alpha=0.7, linewidth=10)
        plt.text(row['Probability of points'], index, f'{str(row["Probability of points"]) + "%"}', va='center', fontsize=10, color='black')

    plt.yticks(range(len(data)), data['Driver'])
    plt.title('Вероятность получения очков на ' + grandPrix)

    filename = 'prediction.png'
    plt.savefig(filename, format='png')
    return filename

def get_visual_prediction(year, grandPrix):
    data, GrandPrixName = get_prediction(year, grandPrix)
    if isinstance(data, str):
        return -1
    else:
        return visualization_of_the_results(data, GrandPrixName)