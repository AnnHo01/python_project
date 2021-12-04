from html.parser import HTMLParser
from re import match
import urllib.request
from decimal import Decimal
from datetime import date, datetime

"""This module scrapes the data from the website colorhexa.com and prints out the colors"""

class WeatherScraper(HTMLParser):
  
  def __init__(self):
    HTMLParser.__init__(self)
    self.tbody_flag = False
    self.td_flag = False
    self.tr_flag = False
    self.abbr_flag = False
    self.td_counter = 0
    self.daily_temps = {}
    self.weather ={}
    self.day = ""
    self.year = ""
    self.month = ""


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
          if(self.day.find(',') >= 0):
            self.year = self.day[self.day.find(',') + 1: ]
            self.month = self.day[0:self.day.find(',') - 2]


  def handle_endtag(self, tag):
    if tag == "tbody":
      self.tbody_flag = False
      # for name, value in self.weather.items():
      #   print(name, value)   
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
 

def early_year(type):
  
  today = date.today()
  input = today.year
  url = f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={input}&Day=1&Year=1840'
  myparser = WeatherScraper()
  with urllib.request.urlopen(url) as response:
      html = str(response.read())
  myparser.feed(html)
  year = myparser.year
  month = myparser.month
  if(type=="y"):
    return year
  elif(type=="m"):
    return month

def get_weather():
  # input will be the 
  today = date.today()
  input = today.year
  early = early_year("y")
  eMonth = early_year("m")
  
  for i in range((int(input) - int(early) + 1)):
    year_to_loop = input - i
    for j in range(12):
      month = 12 - j
      myparser = WeatherScraper()
      with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={input}&Day=1&Year={year_to_loop}&Month={month}#') as response:
          html = str(response.read())

      myparser.feed(html)
      datetime_object = datetime.strptime(eMonth.strip(), "%B")
      month_num = datetime_object.month
   
      for key, value in myparser.weather.items():
        if year_to_loop == int(early):
          if month >= int(month_num):
            print(key, value)
          #  print(month_num)
        else:
          print(key, value)

get_weather()