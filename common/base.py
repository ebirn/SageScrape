
from __future__ import print_function

import ConfigParser

from selenium import webdriver

class Scraper(object):
    def __init__(self, sage_module=None):
        self.config = ConfigParser.ConfigParser()
        self.config.read(['sagescrape.cfg'])

        self.auth = self.config.get('global', 'user') + ':' + self.config.get('global', 'password')

        self.url = "https://" + self.auth +  "@" + self.config.get('global', 'host') + self.config.get(sage_module, 'root_uri')
        self.driver = None
        pass

    def elem_info(self, elem):
        print("ELEMENT: ", elem.id, elem.get_attribute("id"), "element:", elem) #, "href:", elem.get_attribute("href")

    def launch(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1120, 550)
        #self.driver.implicitly_wait(30) # seconds
        self.driver.get(self.url)



