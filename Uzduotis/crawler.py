from time import sleep
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By


s = Service(r'C:\Users\kupsar\Desktop\chromedriver.exe')


def start_crawler(city_from, city_to, date_from, date_to, csv_file_name, append):
    driver = webdriver.Chrome(service=s)
    url = ('https://www.fly540.com/flights/' + city_from + '-to-' + city_to + '?isoneway=0&currency=EUR&depairportcode=NBO&arrvairportcode=MBA&date_from=' + date_from + '&date_to=' + date_to + '&adult_no=1&children_no=0&infant_no=0&searchFlight=&change_flight=')
    driver.get(url)
    sleep(2)
    flights_df = __page_scrape(driver)
    __write_to_csv(flights_df, csv_file_name, append)
    driver.quit()


def __page_scrape(driver):

    # all outbound departure airports
    xpath_out_dep_airports = '//*[@id="book-form"]/div[1]//*[@data-title="Departs"]//*[@class="flfrom"]'
    outbound_departure_airports = driver.find_elements(By.XPATH, xpath_out_dep_airports)
    out_dep_airport_list = [value.text.replace('\n', ' ').replace('(NBO)', 'NBO') for value in
                            outbound_departure_airports]
    out_dep_airport_codes = []
    for n in out_dep_airport_list:
        out_dep_airport_codes.append(''.join(n.split()[5:]))

    # all outbound arrival airports
    xpath_out_arr_airports = '//*[@id="book-form"]/div[1]//*[@data-title="Arrives"]//*[@class="flfrom"]'
    out_arrival_airports = driver.find_elements(By.XPATH, xpath_out_arr_airports)
    out_arr_airport_list = [value.text.replace('\n', ' ').replace('(MBA)', 'MBA') for value in out_arrival_airports]
    out_arr_airport_codes = []
    for n in out_arr_airport_list:
        out_arr_airport_codes.append(''.join(n.split()[5:]))

    # all outbound departure dates
    xpath_out_departure_dates = '//*[@id="book-form"]/div[1]//*[@data-title="Departs"]//*[@class="fldate"]'
    outbound_departure_dates = driver.find_elements(By.XPATH, xpath_out_departure_dates)
    out_dep_date_list = [value.text.replace(',', '') for value in outbound_departure_dates]

    # all outbound departure times
    xpath_out_departure_times = '//*[@id="book-form"]/div[1]//*[@data-title="Departs"]//*[@class="fltime ftop"]'
    outbound_departure_times = driver.find_elements(By.XPATH, xpath_out_departure_times)
    out_dep_time_list = [value.text for value in outbound_departure_times]

    # adding time with date
    out_dep_date_time_list = []
    for i in range(0, len(out_dep_date_list)):
        out_dep_date_time_list.append(out_dep_date_list[i] + ' ' + out_dep_time_list[i])
    #
    # all outbound arrival dates
    xpath_out_arrival_dates = '//*[@id="book-form"]/div[1]//*[@data-title="Arrives"]//*[@class="fldate"]'
    outbound_arrival_dates = driver.find_elements(By.XPATH, xpath_out_arrival_dates)
    out_arr_dates_list = [value.text.replace(',', '') for value in outbound_arrival_dates]

    # all outbound arrival times
    xpath_out_arrival_times = '//*[@id="book-form"]/div[1]//*[@data-title="Arrives"]//*[@class="fltime ftop"]'
    outbound_arrival_times = driver.find_elements(By.XPATH, xpath_out_arrival_times)
    out_arr_times_list = [value.text for value in outbound_arrival_times]

    # adding time with date
    out_arr_dates_times_list = []
    for i in range(0, len(out_arr_dates_list)):
        out_arr_dates_times_list.append(out_arr_dates_list[i] + ' ' + out_arr_times_list[i])

    # all inbound departure airports
    xpath_in_departure_airports = '//*[@id="book-form"]/div[2]//*[@data-title="Departs"]//*[@class="flfrom"]'
    inbound_departure_airports = driver.find_elements(By.XPATH, xpath_in_departure_airports)
    in_dep_airport_list = [value.text.replace('\n', ' ').replace('(MBA)', 'MBA') for value in
                           inbound_departure_airports]
    in_dep_airport_codes = []
    for n in in_dep_airport_list:
        in_dep_airport_codes.append(''.join(n.split()[5:]))

    # all inbound arrival airports
    xpath_in_arrival_airports = '//*[@id="book-form"]/div[2]//*[@data-title="Arrives"]//*[@class="flfrom"]'
    inbound_arrival_airports = driver.find_elements(By.XPATH, xpath_in_arrival_airports)
    in_arr_airport_list = [value.text.replace('\n', ' ').replace('(NBO)', 'NBO') for value in inbound_arrival_airports]
    in_arr_airport_codes = []
    for n in in_arr_airport_list:
        in_arr_airport_codes.append(' '.join(n.split()[5:]))

    # all inbound departure dates
    xpath_in_departure_dates = '//*[@id="book-form"]/div[2]//*[@data-title="Departs"]//*[@class="fldate"]'
    inbound_departure_dates = driver.find_elements(By.XPATH, xpath_in_departure_dates)
    in_dep_dates_list = [value.text.replace(',', '') for value in inbound_departure_dates]

    # all inbound departure times
    xpath_in_departure_times = '//*[@id="book-form"]/div[2]//*[@data-title="Departs"]//*[@class="fltime ftop"]'
    inbound_departure_times = driver.find_elements(By.XPATH, xpath_in_departure_times)
    in_dep_times_list = [value.text for value in inbound_departure_times]

    # adding times with dates
    in_dep_dates_times_list = []
    for i in range(0, len(in_dep_dates_list)):
        in_dep_dates_times_list.append(in_dep_dates_list[i] + ' ' + in_dep_times_list[i])

    # all inbound arrival dates
    xpath_in_arrival_dates = '//*[@id="book-form"]/div[2]//*[@data-title="Arrives"]//*[@class="fldate"]'
    inbound_arrival_dates = driver.find_elements(By.XPATH, xpath_in_arrival_dates)
    in_arr_dates_list = [value.text.replace(',', '') for value in inbound_arrival_dates]

    # all inbound arrival times
    xpath_in_arrival_times = '//*[@id="book-form"]/div[2]//*[@data-title="Arrives"]//*[@class="fltime ftop"]'
    inbound_arrival_times = driver.find_elements(By.XPATH, xpath_in_arrival_times)
    in_arr_times_list = [value.text for value in inbound_arrival_times]

    # adding tiems with dates
    in_arr_dates_times_list = []
    for i in range(0, len(in_arr_dates_list)):
        in_arr_dates_times_list.append(in_arr_dates_list[i] + ' ' + in_arr_times_list[i])

    # all outbound lowest fares
    xpath_lowest_fare_out = '//*[@id="book-form"]/div[1]//*[@data-title="Lowest Fare"]//*[@class="flprice"]'
    lowest_fare_out = driver.find_elements(By.XPATH, xpath_lowest_fare_out)
    lowest_fare_list_out = [value.text for value in lowest_fare_out]

    # all inbound lowest fares
    xpath_lowest_fare_in = '//*[@id="book-form"]/div[2]//*[@data-title="Lowest Fare"]//*[@class="flprice"]'
    lowest_fare_in = driver.find_elements(By.XPATH, xpath_lowest_fare_in)
    lowest_fare_list_in = [value.text for value in lowest_fare_in]

    # adding price lists to get total price
    total_price = []
    for i in range(0, len(lowest_fare_list_out)):
        total_price.append(float(lowest_fare_list_out[i]) + float(lowest_fare_list_in[i]))


    cols = (
        ['outbound_departure_airport', 'outbound_arrival_airport',
         'outbound_departure_time', 'outbound_arrival_time',
         'inbound_departure_airport', 'inbound_arrival_airport',
         'inbound_departure_time', 'inbound_arrival_time', 'total_price'])  # 'taxes'])

    flights_df = pd.DataFrame({'outbound_departure_airport': out_dep_airport_codes,
                               'outbound_arrival_airport': out_arr_airport_codes,
                               'outbound_departure_time': out_dep_date_time_list,
                               'outbound_arrival_time': out_arr_dates_times_list,
                               'inbound_departure_airport': in_dep_airport_codes,
                               'inbound_arrival_airport': in_arr_airport_codes,
                               'inbound_departure_time': in_dep_dates_times_list,
                               'inbound_arrival_time': in_arr_dates_times_list,
                               'total_price': total_price})[cols]
    # 'taxes': taxes})[cols]

    return flights_df

def __write_to_csv(flights_df, csv_file_name, append):
    if append == True:
        write_mode = 'a'
        header_mode = False
    else:
        write_mode = 'w'
        header_mode = True
    flights_df.to_csv(csv_file_name, mode=write_mode, header=header_mode, index=False, sep=';')


