import logging
from html.parser import HTMLParser

logging.basicConfig(filename='status.log', format='%(asctime)s %(message)s', level=logging.NOTSET)
logging.info("Start logging")

class MyHTMLParser(HTMLParser):
    """This class perform scraping actions based on given url."""
    def __init__(self):
        try:
            HTMLParser.__init__(self)
            self.tbody_flag = False
            self.td_flag = False
            self.tr_flag = False
            self.abbr_flag = False
            self.td_counter = 0
            self.tr_counter = 0
            self.daily_temps = {}
            self.weather ={}
            self.day = ""
            self.year = ""
            self.month = ""
        except Exception as error:
            logging.error("WeatherScraper:init", error)

    def handle_starttag(self, tag, attrs):
        """This functiona handles the starting tags"""
        try:
            if tag == "tbody":
                self.tbody_flag = True
            if tag == "tr":
                self.tr_counter += 1
                self.tr_flag = True
            if tag == "td":
                self.td_counter += 1
                self.td_flag = True
            if tag == "abbr":
                self.abbr_flag = True
                for name, value in attrs:
                    try:
                        if name == "title" and self.tr_counter > 1:
                            self.day = value
                            if(self.day.find(',') >= 0):
                                self.year = self.day[self.day.find(',') + 1: ]
                                self.month = self.day[0:self.day.find(',') - 2]
                    except Exception as error:
                        print("WeatherScraper:handle_starttag:loop", error)

        except Exception as error:
            logging.error("WeatherScraper:handle_starttag", error)


    def handle_endtag(self, tag):
        """This function handles the end tags"""
        try:
            if tag == "tbody":
                self.tbody_flag = False
                self.tr_counter = 0
            if tag == "td":
                self.td_flag = False
            if tag == "tr":
                self.tr_flag = False
                self.td_counter = 0
                self.daily_temps = {}
            if tag == "abbr":
                self.abbr_flag = False
        except Exception as error:
            logging.error("WeatherScraper:handle_endtag", error)



    def handle_data(self, data):
        """This fuinction handles the data"""
        try:
            if self.tbody_flag and self.td_flag and self.tr_flag:
                self.temp = data
                if self.td_counter == 1:
                    self.daily_temps.update({"Max Temp": self.temp})
                if self.td_counter == 2:
                    self.daily_temps.update({"Min Temp": self.temp})
                if self.td_counter == 3:
                    self.daily_temps.update({"Mean Temp": self.temp})
                if (self.day != "Average") and (self.day != "Extreme") and (self.day != ''):
                    self.weather.update({self.day: self.daily_temps})
        except Exception as error:
            logging.error("WeatherScraper:handle_data", error)
