#!/usr/bin/env python

from __future__ import print_function

import base64
from time import sleep
from datetime import date, time
import ConfigParser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

check_date = date.today()
#check_date = date(2015, 9, 7) # this is known to be a monday


config = ConfigParser.ConfigParser()
config.read(['sagescrape.cfg'])

url = config.get('global', 'host') + config.get('dpw', 'root_uri')
auth = config.get('global', 'user') + ':' + config.get('global', 'password') 

dpw_url="https://" + auth +  "@" + url 

def elem_info(elem):
    print("ELEMENT: ", elem.id, elem.get_attribute("id"), "element:", elem) #, "href:", elem.get_attribute("href")

driver = webdriver.Chrome()
driver.set_window_size(1120, 550)
#driver.implicitly_wait(30) # seconds
driver.get(dpw_url)
#driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
#driver.find_element_by_id("search_button_homepage").click()

sleep(3)

# switch context to dashboard iframe
dashboard_driver = driver.switch_to_frame("main")

# find link to timesheet data
timesheet_link = driver.find_element_by_link_text("Time sheet")
elem_info(timesheet_link)
timesheet_link.click()

sleep(3)
print("ENTERING TIMESHEET")

# switch to calender context
#dpw_frame = timesheet.switch_to_frame("main")
#elem_info(dpw_frame)

dpw_div = driver.find_element_by_id("dpwdiv")
elem_info(dpw_div)


def switch_times_calendar(root_element, select_date):
  # look at the set month / year
  date_selector = dpw_div.find_element_by_id("reg1monat")
  
  # show weekend days: saturday / sunday 
  date_selector.find_element_by_id("saso").click()

  year_select = Select(date_selector.find_element_by_id("jahr"))
  month_select = Select(date_selector.find_element_by_id("monat"))
  
  year_value = int(year_select.first_selected_option.get_attribute("value"))
  month_value = int(month_select.first_selected_option.get_attribute("value"))
  
  print("we want to see: %s" % select_date)
  print("year selected: %s, year requested: %s" % ( year_value, select_date.year ) )
  print("month selected: %s, month requested: %s" % (month_value, select_date.month) )


  # try to do minimal clicks(), therefore check and execute year/month change individually
  if(year_value != select_date.year):
    year_select.select_by_value(str(select_date.year))

  if(month_value != select_date.month):
    month_select.select_by_value(str(select_date.month))
  

switch_times_calendar(dpw_div, check_date)

def time_balance(driver):
  time_balance = driver.find_element(By.XPATH, "//div[@id='divsaldo1']/div[2]").text
  return float(time_balance.replace(',', '.'))

print("TIME BALANCE: %.2f" % time_balance(driver))
calendar_table = dpw_div.find_element(By.XPATH, "//div[@id='reg1kalender']")

# at this point we assume that the correct month/year is already loaded, we just search for the day
def find_current_day_element(calendar_table, check_date):
  elem_info(calendar_table)
  
  # Table cells, that represent days, each again containing tables
  day_outer_list = calendar_table.find_elements_by_name("kaltd")
  
  print("DAYS: ")
  #
  for day_outer in day_outer_list:
    #elem_info(day_outer)
    try:
        day_num_div = day_outer.find_element_by_name("divkaltag")
        day_num_link = day_num_div.find_element_by_tag_name("a")
        day_num = int(day_num_link.text)
       
        if(day_num == check_date.day):
          return day_num_div 
        #print("Day %i: " % day_num)
        #elem_info(day_num_div)
    
    except NoSuchElementException as nsee:
        # print("no day element found here.")
        pass
    except ValueError as ve:
        # print("cannot parse value: %s" % ve)
        pass
    
  #elem_info(day_outer.find_element_by_name("divkaltag"))
  return None 



day_element = find_current_day_element(calendar_table, check_date)
if(day_element is not None):
  print("the day you were looking for:")
  elem_info(day_element)
else:
  raise SystemExit("cannot find day we are looking for")



def fill_times(day_element, from_time=None, to_time=None):
  from_value = "%0i:%0i" % (from_time.hour, from_time.minute)
  to_value = "%0i:%0i" % (to_time.hour, to_time.minute)
  print("filling times: from '%s' to '%s'" % (from_value, to_value))
  
  from_input = day_element.find_element_by_id("pzbuchzvon")
  from_input.send_keys(from_value)

  to_input = day_element.find_element_by_id("pzbuchzbis")
  to_input.send_keys(to_value)
   
  # submits the whole form, doesn't matter on which element of the form
  #to_input.submit() 
  pass


# datetimel.time() gives the current time
my_enter = time(9,23)
my_exit = time (17,42)

day_element.click()
#day_driver = driver.switch_to_frame("main")

fill_times(driver, my_enter, my_exit)


## print driver.current_url
## 
## link_text="Zwei"
## terror_elements = driver.find_elements_by_partial_link_text(link_text)
## 
## if not (terror_elements):
##     print "NO Terror!"
## 
## for terror in terror_elements:
##     print "TERROR: ", terror.id, terror.get_attribute("id"), "link:", terror.get_attribute("href")

#driver.quit()

