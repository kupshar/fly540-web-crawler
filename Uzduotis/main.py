from datetime import date, timedelta
from crawler import *


city_from = 'nairobi'
city_to = 'mombasa'
date_from = str(date.today() + timedelta(10))
date_to = str(date.today() + timedelta(17))
csv_file_name = 'flight_data.csv'
append = False

start_crawler(city_from, city_to, date_from, date_to, csv_file_name, append)



date_from_two = str(date.today() + timedelta(20))
date_to_two = str(date.today() + timedelta(27))
append = True
start_crawler(city_from, city_to, date_from_two, date_to_two, csv_file_name, append)






