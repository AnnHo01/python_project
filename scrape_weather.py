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
    self.tr_counter = 0
    self.daily_temps = {}
    self.weather ={}
    self.day = ""
    self.year = ""
    self.month = ""


  def handle_starttag(self, tag, attrs):
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
        if name == "title" and self.tr_counter > 1:
          self.day = value
          if(self.day.find(',') >= 0):
            self.year = self.day[self.day.find(',') + 1: ]
            self.month = self.day[0:self.day.find(',') - 2]


  def handle_endtag(self, tag):
    if tag == "tbody":
      self.tbody_flag = False
      self.tr_counter = 0
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
      if (self.day != "Average") and (self.day != "Extreme") and (self.day != ''):
        self.weather.update({self.day: self.daily_temps})


def early_year(type):
  """This function is finding out the earliest yearon the website"""

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

def get_weather(latest_year = None, latest_month = None):
  """This function scrapes the data"""
  result = {}
  today = date.today()
  input = today.year
  new_month = 0
  early = None
  eMonth = None
  if latest_year != None:
    early = latest_year
    eMonth = str(latest_month)
  else:
    early = early_year("y")
    eMonth = early_year("m")

  for i in range((int(input) - int(early) + 1)):
    year_to_loop = int(early) + i
    for j in range(12):
      month = j + 1
      myparser = WeatherScraper()
      with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={input}&Day=1&Year={year_to_loop}&Month={month}#') as response:
          html = str(response.read())

      myparser.feed(html)
      if not eMonth.isnumeric():
          datetime_object = datetime.strptime(eMonth.strip(), "%B")
          month_num = datetime_object.month
      else:
          month_num = int(eMonth)

      for key, value in myparser.weather.items():
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



  return result

# print(get_weather())