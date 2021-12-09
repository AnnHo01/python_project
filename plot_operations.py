import matplotlib.pyplot as plt
from dateutil import parser
import statistics
import db_operations
import pprint

class PlotOperations():
    """Create a basic boxplot of mean temperatures in a date range supplied by the user."""
    def __init__(self):
        self.weather_data = {}
        self.data_list = []

    def process_data(self):
        """Loop through database and grab data."""
        db = db_operations.DBOperations("weather.sqlite")
        data_tuple = db.fetch_data()
        new_month = 0
        for x in data_tuple:
            date = str(x[1])
            month = int(date[5:7])
            day = int(date[8:])
            avg_temp = str(x[5])
            if month != new_month and new_month != 0:
                if month == 1:
                    # if month in self.weather_data:
                    self.weather_data[month] = [self.weather_data[month], self.data_list]
                    self.data_list = []
                if month == 2:
                    # if month in self.weather_data:
                    self.weather_data[month] = [self.weather_data[month], self.data_list]
                    self.data_list = []
            else:
                  self.append_data_to_list(avg_temp)

        return self.weather_data

    def append_data_to_list(self, avg_temp):
        if not avg_temp.isalpha():
          self.data_list.append(avg_temp)

        if key in d:
            d[key] = [d[key],val]
test = PlotOperations()
pprint.pprint(test.process_data())