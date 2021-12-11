import matplotlib.pyplot as plt
from dateutil import parser
import statistics
import db_operations
import pprint
import collections

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
                        for item in self.data_list:
                            self.weather_data[int(month)].append(float(item))
                    else:
                        self.weather_data.update({int(month): self.data_list})
                new_month = month
                self.data_list = []
                if not avg_temp.isalpha() and avg_temp != '\xa0':
                    self.data_list.append(float(avg_temp))
            else:
                if not avg_temp.isalpha() and avg_temp != '\xa0':
                    self.data_list.append(float(avg_temp))
        return self.weather_data

    def plotting(self, data):
        """Plot the box graph using given data. Data accepted is a dictionary"""
        try:
            list_plot = []
            ordered_dict = collections.OrderedDict(sorted(data.items()))
            for key, value in ordered_dict.items():
                flier_low = min(value)
                flier_high = max(value)
                median = statistics.median(value)
                spread = flier_high - flier_low

                g_data = [spread, median, flier_high, flier_low]
                list_plot.append(g_data)

            plt.figure()
            plt.boxplot(list_plot)
            plt.show()
        except Exception as e:
            print("PlotOperations:plotting:Error: ", e)


test = PlotOperations()
test.plotting(test.process_data())

