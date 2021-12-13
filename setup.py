from setuptools import setup

setup(
  name = "Weather Processing App",
  version = "1.0",
  description = "Scrapes the weather data from the web site and plots the mean temperature based on the user input.",
  author = "Chau Thanh An Ho, Stacie(Anastasya) Zolotarevsky",
  author_email = "cho107@academic.rrc.ca, azolotarevsky@rrc.ca",
  py_modules = ["db_operations","dbcm","plot_operations","scrape_weather","weather_processor"]
)