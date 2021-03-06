"""This module scrapes the data from the Environment Canada website and prints returns the dictionary of dictionaries of data"""
import urllib.request
from datetime import date, datetime
import logging
import html_parser as parser


logging.basicConfig(filename='status.log', format='%(asctime)s %(message)s', level=logging.NOTSET)
logging.info("Start logging")


class WeatherScraper():
    """This class parses the HTML and returns the data"""
    def early_year(self, date_type):
        """This function is finding out the earliest year on the website"""
        try:
            result = None
            today = date.today()
            today_year = today.year
            url = f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={today_year}&Day=1&Year=1840'
            myparser = parser.MyHTMLParser()
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            myparser.feed(html)
            year = myparser.year
            month = myparser.month
            if date_type=="y":
                result = year
            elif date_type=="m" :
                result = month
            return result
        except Exception as error:
            logging.error("WeatherScraper:early_year", error)


    def get_weather(self, latest_year = None, latest_month = None):
        """This function scrapes the data"""
        try:
            result = {}
            today = date.today()
            today_year = today.year
            new_month = 0
            early = None
            e_month = None
            if latest_year is not None:
                early = latest_year
                e_month = str(latest_month)
            else:
                early = self.early_year("y")
                e_month = self.early_year("m")

            for i in range((int(today_year) - int(early) + 1)):
                try:
                    year_to_loop = int(early) + i
                    for j in range(12):
                        month = j + 1
                        myparser = parser.MyHTMLParser()
                        with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={today_year}&Day=1&Year={year_to_loop}&Month={month}#') as response:
                            html = str(response.read())

                        myparser.feed(html)
                        if not e_month.isnumeric():
                            datetime_object = datetime.strptime(e_month.strip(), "%B")
                            month_num = datetime_object.month
                        else:
                            month_num = int(e_month)

                        for key, value in myparser.weather.items():
                            try:
                                date_format = datetime.strptime(str(key), '%B %d, %Y' )
                                right_format = date_format.strftime('%Y-%m-%d')
                                if year_to_loop == int(early):
                                    if month >= int(month_num):
                                        result.update({right_format: value})
                                        if month != new_month:
                                            print("Processing: " + key[:key.find(',') - 2] + f" {year_to_loop}")
                                            new_month = month
                                else:
                                    result.update({right_format: value})
                                    if month != new_month:
                                        print("Processing: " + key[:key.find(',') - 2] + f" {year_to_loop}")
                                        new_month = month
                            except Exception as error:
                                logging.error("WeatherScraper:get_weather:loop_3", error)
                except Exception as error:
                    logging.error("WeatherScraper:get_weather:loop_1", error)
            return result
        except Exception as error:
            logging.error("WeatherScraper:get_weather", error)
