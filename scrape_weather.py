from html.parser import HTMLParser
from re import match
import urllib.request
from decimal import Decimal


class WeatherScraper(HTMLParser):
  


  def __init__(self):
    HTMLParser.__init__(self)
    self.tbody_flag = False
    self.th_flag = False
    self.td_flag = False
    self.tr_flag = False
    self.abbr_flag = False
    self.td_counter = 0
    self.daily_temps = {}
    self.temp = 0
    self.weather ={}
    self.day = ""



  def handle_starttag(self, tag, attrs):
    if tag == "tbody":
      self.tbody_flag = True
    if tag == "tr":
      self.tr_flag = True
    if tag == "td":
      self.td_counter += 1
      self.td_flag = True
    if tag == "abbr":
      self.abbr_flag = True
      for name, value in attrs:
        if name == "title":
          self.day = value


  def handle_endtag(self, tag):
    if tag == "tbody":
      self.tbody_flag = False
      for name, value in self.weather.items():
        print(name, value)   
      # print(self.weather)
    if tag == "td":
          self.td_flag = False
    if tag == "tr":
      self.tr_flag = False
      self.td_counter = 0
      self.daily_temps = {}
    if tag == "abbr":
      self.abbr_flag = False


  def handle_data(self, data):
    if self.tbody_flag and self.td_flag and self.tr_flag:
      self.temp = data
      if self.td_counter == 1:
        self.daily_temps.update({"Max Temp": self.temp})
      if self.td_counter == 2:
        self.daily_temps.update({"Min Temp": self.temp})
      if self.td_counter == 3:
        self.daily_temps.update({"Mean Temp": self.temp})
      if (self.day != "Average") and (self.day != "Extreme"):
        self.weather.update({self.day: self.daily_temps})
 


    # def handle_starttag(self, tag, attrs):
    #     print ("Encountered the beginning of a %s tag" % tag)

    # def handle_endtag(self, tag):
    #     print ("Encountered the end of a %s tag" % tag)



myparser = WeatherScraper()

with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2021&Month=11#') as response:
    html = str(response.read())

myparser.feed(html)
