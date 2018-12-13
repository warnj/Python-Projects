from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import time, json


def main():
    data = json.loads(open('../personal_data.json').read())

    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    d = webdriver.Firefox(firefox_binary=binary)
    d.get("http://library.morningstar.com.ezproxy.spl.org/portfolio/InstantXRayEntry")
    d.maximize_window()
    time.sleep(.2)
    elem = d.find_element_by_name("user")
    elem.send_keys(data['library_username'])
    elem = d.find_element_by_name("pass")
    elem.send_keys(data['library_pin'])
    elem.send_keys(Keys.RETURN)

    # TODO: enter asset allocation


if __name__ == "__main__":
    main()
