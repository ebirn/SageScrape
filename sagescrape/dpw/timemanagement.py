from __future__ import print_function

from datetime import date, time
import time as systime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sagescrape.common.base import Scraper


class TimeManagement(Scraper):
    def __init__(self):
        super(TimeManagement, self).__init__("dpw")
        self.use_weekends = False
        self.dpw_div = None

    def launch(self):
        super(TimeManagement, self).launch()
        print("timemanagement::launch: switch_to.frame()")

        main_frame = WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'main')))
        #self.driver.switch_to.frame("main")

        self.dpw_div = self.find((By.ID, "dpwdiv"))
        self.elem_info(self.dpw_div)

        # find link to timesheet data
        timesheet_link = self.find((By.LINK_TEXT, "Time sheet"))
        self.elem_info(timesheet_link)
        timesheet_link.click()
        #
        print("ENTERING TIMESHEET")

    @property
    def weekends(self):
        return self.use_weekends

    @weekends.setter
    def weekends(self, value):
        self.use_weekends = value

    # load page that displays calendar for the given date
    def _switch_times_calendar(self, select_date):
        # look at the set month / year
        date_selector = self.find((By.ID, "reg1monat"), root=self.dpw_div)

        # show weekend days: saturday / sunday
        date_selector.find((By.ID, "saso")).click()

        year_select = Select(date_selector.find_element(By.ID, "jahr"))
        month_select = Select(date_selector.find_element(By.ID, "monat"))

        year_value = int(year_select.first_selected_option.get_attribute("value"))
        month_value = int(month_select.first_selected_option.get_attribute("value"))

        print("we want to see: %s" % select_date)
        print("year selected: %s, year requested: %s" % (year_value, select_date.year))
        print("month selected: %s, month requested: %s" % (month_value, select_date.month))

        # try to do minimal clicks(), therefore check and execute year/month change individually
        if (year_value != select_date.year):
            year_select.select_by_value(str(select_date.year))

        if (month_value != select_date.month):
            month_select.select_by_value(str(select_date.month))

    # get working time balance when in calendar view
    def time_balance(self):
        time_balance_str = self.dpw_div.find_element(By.XPATH, "//div[@id='divsaldo1']/div[2]").text
        time_balance = None
        try:
            time_balance = float(time_balance_str.replace(',', '.'))
        except ValueError:
           # when we are unable to parse the value
           time_balance = None
           pass
        return time_balance

    # at this point we assume that the correct month/year is already loaded, we just search for the day
    def _find_current_day_element(self, check_date):
        calendar_table = self.find((By.XPATH, "//div[@id='reg1kalender']"))
        self.elem_info(calendar_table)

        # Table cells, that represent days, each again containing tables
        day_outer_list = calendar_table.find_elements_by_name("kaltd")

        print("DAYS: ")
        #
        for day_outer in day_outer_list:
            # elem_info(day_outer)
            try:
                day_num_div = day_outer.find_element_by_name("divkaltag")
                day_num_link = day_num_div.find_element_by_tag_name("a")
                day_num = int(day_num_link.text)

                if (day_num == check_date.day):
                    return day_num_div
                    # print("Day %i: " % day_num)
                    # elem_info(day_num_div)

            except NoSuchElementException as nsee:
                # print("no day element found here.")
                pass
            except ValueError as ve:
                # print("cannot parse value: %s" % ve)
                pass

        # elem_info(day_outer.find_element_by_name("divkaltag"))
        return None

    def _fill_time_field(self, element, time_value):
        value_str = "%0i:%0i" % (time_value.hour, time_value.minute)
        element.send_keys(value_str)

    def fill_times(self, fill_date, from_time=None, to_time=None):

        day_element = self._find_current_day_element(fill_date)
        day_element.click()

        if from_time:
            from_input = self.find((By.ID, "pzbuchzvon"))
            self._fill_time_field(from_input, from_time)

        if to_time:
            to_input = self.find((By.ID, "pzbuchzbis"))
            self._fill_time_field(to_input, to_time)


        # submits the whole form, doesn't matter on which element of the form
        if not self.debug_mode:
            to_input.submit()

        pass
	
    def get_times(self, the_date):
        day_element = self._find_current_day_element(the_date)
        from_str = day_element.find_element_by_id("pzbuchzvon").get_attribute('value')
        to_str = day_element.find_element_by_id("pzbuchzbis").get_attribute('value')
        from_time = None
        to_time = None
 
        try:
            from_time = datetime.strptime(from_str, '%H:%M')
        except ValueError:
            pass
 
        try:
            to_time = datetime.strptime(to_str, '%H:%M')
        except ValueError:
            pass
 
        return (from_time.time(), to_time.time())
 


if __name__ == "main":
    # datetimel.time() gives the current time
    my_enter = time(9,23)
    my_exit = time(17,42)

    tm = timemanagement()
    tm.launch()
    tm.fill_times(date.today(), my_enter, my_exit)
