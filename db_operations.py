import scrape_weather
import dbcm

class DBOperations():

    def __init__(self, filename):
        self.weather = None
        self.filename = filename


    def initialize_db(self, weather):
        """This function will initialize the database and create the table."""
        try:
            self.weather = weather
            with dbcm.DBCM(self.filename) as db:
                db.execute("""create table if not exists samples (id integer primary key autoincrement not null,
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
            with dbcm.DBCM(self.filename) as db:
                self.purge_data()
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
                    db.execute(sql,data)

        except Exception as e:
            print("DBOperation:save_db:error: ", e)


    def fetch_data(self):
        try:
            """This function will print the data"""
            list = []
            with dbcm.DBCM(self.filename) as db:
                for row in db.execute("select * from samples"):
                    list.append(row)
                return tuple(list)
        except Exception as e:
            print("DBOperation:fetch_db:error: ", e)


    def purge_data(self):
        try:
            with dbcm.DBCM(self.filename) as db:
                db.execute("DELETE FROM samples")
                print("Delete successfully")
        except Exception as e:
            print("DBOperation:purge_data:error: ", e)


"""Inputing data to database"""
# weather = scrape_weather.get_weather()
# test = DBOperations("weather.sqlite")
# test.initialize_db(weather)
# test.save_data()
# print(test.fetch_data())
