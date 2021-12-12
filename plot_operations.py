from datetime import datetime
import matplotlib.pyplot as plt
import statistics
import collections

class PlotOperations():
    """Create a basic boxplot of mean temperatures in a date range supplied by the user."""
    def __init__(self, data_tuple):
        self.weather_data = {}
        self.data_list = []
        self.data_tuple = data_tuple

    def process_data(self, start_year = None, end_year = None, input_month = None, input_year = None):
        """Loop through database and grab data."""
        data_tuple = self.data_tuple
        new_month = 0
        choice = None
        for x in data_tuple:
            date = str(x[1])
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:])
            avg_temp = str(x[5])
            if start_year != None:
                if (int(start_year) <= year and year <= int(end_year)) or (year > int(end_year) and month == 1):
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
                    choice = "box"
            elif input_month != None:
                if int(input_month) == month and int(input_year) == year:
                    if not avg_temp.isalpha() and avg_temp != '\xa0':
                        self.data_list.append(float(avg_temp))


        if choice == "box":
            self.box_plotting(self.weather_data, start_year, end_year)
        else:
            self.line_plotting(self.data_list, input_month, input_year)

    def box_plotting(self, data, start_year, end_year):
        """Plot the box graph using given data. Data accepted is a dictionary."""
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
            plt.ylabel("Mean Temp")
            plt.xlabel(f"{start_year} to {end_year}")
            plt.title(f"Monthly temperature for years: {start_year} to {end_year}")
            plt.show()
        except Exception as e:
            print("PlotOperations:plotting:Error: ", e)

    def line_plotting(self, data, month, year):
        """Plot the line graph using given data. Data accepted is a list."""
        try:
            datetime_object = datetime.strptime(month, "%m")
            month_name = datetime_object.strftime("%B")
            plt.plot(data)
            plt.ylabel("Mean Temp")
            plt.xlabel(month_name + f", {year}")
            plt.show()
        except Exception as e:
            print("PlotOperations:line_plotting:Error: ", e)
