# SageScrape
a simple tool for filling in your SAGE DPW time tracking.

this is very experimental.

###

### Dependencies
Python:

- datetime
- ConfigParser
- selenium

It might also need, as Selenium backend:
 
 - [Chromium ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/): `brew install chromedriver` or get it from homepage
 - [PhantomJS](http://phantomjs.org/): for headless mode

the backend / chromium driver can be set in the config file.

### Installation
It has a setup.py, so what SHOULD work:

    python setup.py install


### Usage:
You need do set your username, password, hostname in the config file.

see the sc_test.py example script
