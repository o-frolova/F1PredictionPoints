import fastf1 as f1
import pandas as pd
import numpy as np
import math
import os

data = pd.read_csv('../f1dataset.csv')
df_drivers = pd.read_csv('../DataCollection/archive/drivers.csv')
df_teams = pd.read_csv('../DataCollection/archive/constructors.csv')
df_circuits = pd.read_csv('../DataCollection/archive/circuits.csv')

def timestamp_to_milliseconds(timestamp):
  time = timestamp.total_seconds() * 1000
  if not math.isnan(time):
    return int(time)
  else:
    return np.inf

def get_info_drivers(session):
    info_driver = []
    for driver in session.drivers:
        info_driver.append(session.get_driver(driver))
    return info_driver

def get_information(year, grandPrix):
    try:
        if year > 2021 and (grandPrix == 'Sochi' or grandPrix == 'Russia'):
            print('Tut')
            return 0, 0
        else:
            print(year, grandPrix)
            session = f1.get_session(year, grandPrix, 'Q')
            GranPrixName = session.event['EventName']
            session.load(telemetry=False, laps=False, weather=False)
            info_driver = get_info_drivers(session)
            dataset = []
            for i in range(len(info_driver)):
                
                drivers_res = {}
                id_driver = df_drivers[df_drivers['code'] == info_driver[i]['Abbreviation']]['driverId'].tolist()
                id_team = df_teams[df_teams['constructorRef'] == info_driver[i]['TeamId']]['constructorId'].tolist()
                id_race = df_circuits[df_circuits['circuitRef'] == grandPrix.lower()]['circuitId'].tolist()

                drivers_res['DriverId'] = id_driver[0]
                drivers_res['TeamId'] = id_team[0]
                drivers_res['CountryRaceId'] = id_race[0] if id_race != [] else -1
                drivers_res['QualificationPosition'] = info_driver[i]['Position']
                drivers_res['Q1'] = timestamp_to_milliseconds(info_driver[i]['Q1'])
                drivers_res['Q2'] = timestamp_to_milliseconds(info_driver[i]['Q2'])
                drivers_res['Q3'] = timestamp_to_milliseconds(info_driver[i]['Q3'])
                drivers_res['TeamColor'] = info_driver[i]['TeamColor']
                dataset.append(drivers_res)
            
            return pd.DataFrame(dataset), GranPrixName
    except:
        return 0, 0

