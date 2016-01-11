#!/usr/bin/env python

from datetime import date, time
from sagescrape.dpw.timemanagement import TimeManagement

if __name__ == "__main__":
    # datetime.time() gives the current time
    my_enter = time(9,23)
    my_exit = time(17,42)

    tm = TimeManagement()
    tm.launch()
    tm.fill_times(date.today(), my_enter, my_exit)

    tm.shutdown()

