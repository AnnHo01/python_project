import plot_operations as plot
import db_operations as db
import scrape_weather



"""This module handles the user interaction for and provides the data based on the requirements."""
class WeatherProcessor():
    """Present user with menu of choices to check weather data."""
    def __init__(self):
        try:
            choice = input("Fetch all the available data, update the existing or skip? ([F]ull/[U]pdate/[S]kip): ")
            if choice.upper() == 'F':
                self.full()
            elif choice.upper() == 'U':
                self.update()
            elif choice.upper() == 'S':
                self.skip()
            else:
                choice = input("Sorry, please run the program again and select the correct input.")
        except Exception as error:
            print("WeatherProcessor:init", error)



    def update(self):
        """Update only neccessary data"""
        try:
            dataBase = db.DBOperations("weather.sqlite")
            data_tuple = dataBase.fetch_data(True)
            for item in data_tuple:
                latest_date = str(item[1])
                latest_year = int(latest_date[:4])
                latest_month = int(latest_date[5:7])
            scrape = scrape_weather.get_weather(latest_year,latest_month)
            dataBase.initialize_db(scrape)
            dataBase.save_data()
            data = dataBase.fetch_data()
            self.graph(data)
        except Exception as error:
            print("WeatherProcessor:update", error)


    def full(self):
        """Call purge and then save_data"""
        try:
            weather = scrape_weather.get_weather()
            dataBase = db.DBOperations("weather.sqlite")
            dataBase.purge_data()
            dataBase.initialize_db(weather)
            dataBase.save_data()
            data = dataBase.fetch_data()
            self.graph(data)
        except Exception as error:
            print("WeatherProcessor:full", error)


    def skip(self):
        """Call fetch all and ask for what plot type"""
        try:
            dataBase = db.DBOperations("weather.sqlite")
            data = dataBase.fetch_data()
            self.graph(data)
        except Exception as error:
            print("WeatherProcessor:skip", error)

    def graph(self, data):
        """Prompt user for graph type and show corresponded graph."""
        try:
            graph = plot.PlotOperations(data)
            choice = input("Enter plotting choice ([B]ox or [L]ine): ").upper()
            if choice == "B":
                start_year = input("Enter start year: ")
                end_year = input("Enter end year: ")

                graph.process_data(start_year, end_year)
            elif choice == "L":
                month = input("Enter a month (number): ")
                year = input("Enter a year: ")
                graph.process_data(None, None, month, year)
        except Exception as error:
            print("WeatherProcessor:graph", error)



if __name__ == "__main__":
    test = WeatherProcessor()