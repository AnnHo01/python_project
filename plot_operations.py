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
        if month != new_month:
          if self.data_list != []:
            if str(month) in self.weather_data:
              self.weather_data[str(month)] = [self.weather_data[str(month)], self.data_list]
            else:
              self.weather_data.update({str(new_month): self.data_list})
          new_month = month
          self.data_list = []
          if not avg_temp.isalpha():
            self.data_list.append(avg_temp)
        else:
          if not avg_temp.isalpha():
            self.data_list.append(avg_temp)
        # print(month)
        # print(x[5])
      return self.weather_data


test = PlotOperations()
pprint.pprint(test.process_data())