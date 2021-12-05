import sqlite3
import scrape_weather


class DBOperations():

    def __init__(self, weather):
        self.weather = weather


    def initialize_db():
        """This function will initialize the database and create the table."""
        try:
            conn = sqlite3.connect("weather.sqlite")
            cur = conn.cursor()
            cur.execute("""create table if not exists samples (id integer primary key autoincrement not null,
                                                sample_date text not null UNIQUE,
                                                location text not null,
                                                min_temp real not null,
                                                max_temp real not null,
                                                avg_temp real not null);""")
        except Exception as e:
            print("DBOperation:init_db:error: ", e)

    def save_data(self):
        """This function will insert the data into the table."""
        try:
            self.purge_data()
            conn = sqlite3.connect("weather.sqlite")
            cur = conn.cursor()
            sql = """insert into samples (sample_date, location, min_temp, max_temp, avg_temp) values (?,?,?,?,?)"""
            for date, temp_data in weather.items():
                data_date = date
                data_location = 'Winnipeg, MB'
                for temp,  value in temp_data.items():
                    if temp == 'Max Temp':
                        max_temp = value
                    elif temp == 'Min Temp':
                        min_temp = value
                    elif temp == 'Mean Temp':
                        mean_temp = value

                data = (data_date,data_location,max_temp,min_temp,mean_temp)
                cur.execute(sql,data)
                conn.commit()
                
        except Exception as e:
            print("DBOperation:save_db:error: ", e)


    def fetch_data():
        try:
            """This function will print the data"""

            conn = sqlite3.connect("weather.sqlite")
            cur = conn.cursor()
            for row in cur.execute("select * from samples"):
                print(row)
            cur.close()
            conn.close()
        except Exception as e:
            print("DBOperation:fetch_db:error: ", e)
            
            
    def purge_data(self):
        try:
            conn = sqlite3.connect("weather.sqlite")
            cur = conn.cursor()
            cur.execute("DELETE FROM samples")
            print("Delete successfully")
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("DBOperation:purge_data:error: ", e)
            


"""Main Code"""

DBOperations.initialize_db()
weather = scrape_weather.get_weather()
DBOperations.save_data(weather)
DBOperations.fetch_data()
