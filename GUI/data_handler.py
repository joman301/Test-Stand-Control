import time
import csv


class data_handler:
    def __init__(self):
        self.state = False

    def save(self, data):
        if self.state:
            data.append(time.asctime())
            with open("flight_data.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(data)

    def start(self):
        self.state = True
        print('Beginning data storage in csv at', time.process_time(), 'seconds')

    def stop(self):
        self.state = False
        print('Stopping data storage in csv at', time.process_time(), 'seconds')

