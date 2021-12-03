from html.parser import HTMLParser
import urllib.request


class WeatherScraper(HTMLParser):
  
    def __init__(self):
      HTMLParser.__init__(self)
      self.tbody_flag = False
      self.a_flag = False

  
  
  
  
    def handle_starttag(self, tag, attrs):
        print("Found a start tag:", tag)

    def handle_endtag(self, tag):
        print("Found end tag :", tag)

    def handle_data(self, data):
        print("Found some data  :", data)


myparser = WeatherScraper()

with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2021&Month=11#') as response:
    html = str(response.read())

myparser.feed(html)
