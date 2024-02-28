import fastf1 as f1
import pandas as pd
import fastf1.plotting
import matplotlib.pyplot as plt

data = pd.read_csv('../Research/importancepoleposition.csv')

def importancepole(location, data = data):
    try:
        return round(list(data[data['location'] == location]['Frequency'])[0] * 100, 2)
    except:
        return -1

def comparefastestlaps(year, grandPrix ,n_first_driver, n_second_driver):
    try:
        fastf1.plotting.setup_mpl()
        plt.switch_backend('Agg')

        session = f1.get_session(year, grandPrix, 'Q')
        session.load()
        first_driver = session.laps.pick_driver(n_first_driver).pick_fastest()
        second_driver = session.laps.pick_driver(n_second_driver).pick_fastest()

        first_driver_data = first_driver.get_car_data()
        second_driver_data = second_driver.get_car_data()

        fig, ax = plt.subplots()
        ax.plot(first_driver_data['Time'], first_driver_data['Speed'], label=session.get_driver(n_first_driver)['Abbreviation'])
        ax.plot(second_driver_data['Time'], second_driver_data['Speed'], label = session.get_driver(n_second_driver)['Abbreviation'])
        ax.set_xlabel('Время')
        ax.set_ylabel('Скорость [Км/ч]')
        ax.set_title('Сравнение ' + session.get_driver(n_first_driver)['LastName'] + ' and ' + session.get_driver(n_second_driver)['LastName'])
        ax.legend()
        
        filename = 'comparison.png'
        plt.savefig(filename, format='png')
        return filename
    except:
        return -1
    