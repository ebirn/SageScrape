from __future__ import print_function

from datetime import date, time
import time as systime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from common.base import Scraper


class TimeManagement(Scraper):
    def __init__(self):
        super(TimeManagement, self).__init__("dpw")
        self.use_weekends = False
        self.dpw_div = None

    def launch(self):
        super(TimeManagement, self).launch()
        systime.sleep(3)
        self.driver.switch_to.frame("main")
        self.dpw_div = self.driver.find_element(By.ID, "dpwdiv")
        self.elem_info(self.dpw_div)

        # find link to timesheet data
        timesheet_link = self.driver.find_element_by_link_text("Time sheet")
        self.elem_info(timesheet_link)
        timesheet_link.click()
        self.driver.switch_to.frame("main")
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
        date_selector = self.dpw_div.find_element(By.ID, "reg1monat")

        # show weekend days: saturday / sunday
        date_selector.find_element(By.ID, "saso").click()

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
        time_balance = self.dpw_div.find_element(By.XPATH, "//div[@id='divsaldo1']/div[2]").text
        return float(time_balance.replace(',', '.'))


    # at this point we assume that the correct month/year is already loaded, we just search for the day
    def _find_current_day_element(self, check_date):
        calendar_table = self.dpw_div.find_element(By.XPATH, "//div[@id='reg1kalender']")
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
            from_input = self.driver.find_element(By.ID, "pzbuchzvon")
            self._fill_time_field(from_input, from_time)

        if to_time:
            to_input = self.driver.find_element(By.ID, "pzbuchzbis")
            self._fill_time_field(to_input, to_time)


        # submits the whole form, doesn't matter on which element of the form
        if not self.demo_mode:
            to_input.submit()

        pass


if __name__ == "main":
    # datetimel.time() gives the current time
    my_enter = time(9,23)
    my_exit = time(17,42)

    tm = timemanagement()
    tm.launch()
    tm.fill_times(date.today(), my_enter, my_exit)