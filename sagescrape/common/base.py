
from __future__ import print_function

import ConfigParser

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper(object):
    def __init__(self, sage_module=None):
        self.config = ConfigParser.ConfigParser()
        self.config.read(['sagescrape.cfg'])

        self.auth = self.config.get('global', 'user') + ':' + self.config.get('global', 'password')

        self.url = "https://" + self.auth +  "@" + self.config.get('global', 'host') + self.config.get(sage_module, 'root_uri')
        self.driver = getattr(webdriver, self.config.get('global', 'driver'))()
        self.demo_mode = self.config.get('global', 'demo_mode')
        pass

    def elem_info(self, elem):
        print("ELEMENT: ", elem.id, elem.get_attribute("id"), "element:", elem) #, "href:", elem.get_attribute("href")

    def launch(self):
        self.driver.set_window_size(1120, 550)
        #self.driver.implicitly_wait(30) # seconds
        self.driver.get(self.url)


    def find(self, locator, root=None, timeout=30):
        root_element = root if root else self.driver

        # wait for up to timeout seconds for DOM element to appear and return it when found
        element = WebDriverWait(root_element, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element



    def shutdown(self):
        if self.driver is not None:
            self.driver.quit()
