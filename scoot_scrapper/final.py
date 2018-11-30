from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
now = datetime.datetime.now()
from time import sleep
import time
import re
import sys


source = sys.argv[1]
destination = sys.argv[2]
start_dt = sys.argv[3]
end_dt = sys.argv[4]
onward_date = start_dt
onward_year = int(onward_date[0:4])
onward_month = int(onward_date[4:6])
onward_day = int(onward_date[6:])
pax_num = 3

onward_clicks = 12*(onward_year - now.year) - now.month - 1 + onward_month

browser = webdriver.Chrome()
browser.set_page_load_timeout(50)
browser.get("https://www.alternativeairlines.com") ##load website

#select ony way radio button
browser.find_elements_by_class_name("iCheck-helper")[1].click()
time.sleep(2)

#set source
browser.find_element_by_id("flight-search-departure-input").send_keys(source)
time.sleep(3)
((browser.find_elements_by_class_name("autocomplete-suggestion-name"))[0]).click()
time.sleep(2)

#set destination
browser.find_element_by_id("flight-search-arrival-input").send_keys(destination)
time.sleep(3)
browser.find_element_by_xpath("//div[@class='autocomplete-suggestion-name' and @search_type='arrival']").click()
time.sleep(2)


#number of passengers
browser.find_element_by_id("flight-search-travellers-toggle").click()
pax_ele = browser.find_elements_by_class_name("flight-search-pax-control-plus")[0]
for i in range(pax_num-1):
    pax_ele.click()
    time.sleep(0.5)

browser.find_elements_by_class_name("flight-search-tooltip-close")[0].click()
time.sleep(0.5)

calender_forward = True

for date_ in range(int(start_dt), int(end_dt)+1):
    #set onward date
    browser.find_element_by_id("flight-search-outbound-input").click()
    time.sleep(2)
    
    if calender_forward:
        dep_cal = browser.find_elements_by_class_name("flight-search-calendar-scroll-right")
        for i in range(onward_clicks):
            dep_cal[0].click()
            time.sleep(0.5)
        calender_forward = False
        
    browser.find_element_by_xpath("//span[@data-seq='" + str(date_) + "']").click()
    time.sleep(2)

    #submit
    browser.find_element_by_name("submit").click()
    time.sleep(20)

    browser.find_element_by_id("airlines-more").click()
    time.sleep(2)

    browser.find_element_by_xpath("//label[@for='airlines-TR']").click()
    time.sleep(2)

    flights_out_ele = browser.find_elements_by_class_name("result-flight-times-out")
    flights_out_time = []
    for i in range(len(flights_out_ele)):
        flights_out_time.append(flights_out_ele[i].text)

    flights_in_ele = browser.find_elements_by_class_name("result-flight-times-in")
    flights_in_time = []
    for i in range(len(flights_in_ele)):
        flights_in_time.append(flights_in_ele[i].text)

    flights_dur_ele = browser.find_elements_by_class_name("result-flight-stops")
    flights_duration = []
    for i in range(len(flights_dur_ele)):
        flights_duration.append(flights_dur_ele[i].text)

    # Flight Cost
    results = browser.find_elements_by_class_name("result-flights")
    res_data = []
    for i in range(len(results)):
        number_of_flights = len(results[i].find_elements_by_xpath(".//img[@src='/images/global/airlinelogos/tr_logo.gif']"))
        if number_of_flights >0:
            res_data.append(number_of_flights)

    fare_ele = browser.find_elements_by_class_name("result-fare")
    fare = []
    for i in range(len(fare_ele)):
        fare.append(fare_ele[i].text)

    flights_out_time_extracted = [re.search(r'.+',x).group(0) for x in flights_out_time if re.match(r'.+',x)]
    flights_in_time_extracted = [re.search(r'.+',x).group(0) for x in flights_in_time if re.match(r'.+',x)]
    flights_duration_extracted = [re.search(r'\d{2}h \d{2}m',x).group(0) for x in flights_duration if re.match(r'\d.+',x)]
    fare_extracted = [re.search(r'\S+',x).group(0) for x in fare if re.match(r'.+',x)]

    fare_extracted_list_of_list = [n*[f] for n,f in zip(res_data,fare_extracted)]
    fare_extracted_list = [item for sublist in fare_extracted_list_of_list for item in sublist]
    
    date_list = [date_]*len(fare_extracted_list)
    
    print(date_list)
    print(flights_out_time_extracted)
    print(flights_in_time_extracted)
    print(flights_duration_extracted)
    print(fare_extracted_list)
    
    time.sleep(2)
    
    browser.find_elements_by_class_name("logo")[0].click()

time.sleep(7)
browser.quit()