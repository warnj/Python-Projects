from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import firefox
from selenium.webdriver.common.keys import Keys
import time, datetime, sys, csv, json

# https://github.com/clickthisnick/CraigLister/blob/master/craiglister.py


data = json.loads(open('../personal_data.json').read())

EMAIL = data["email"]
ZIP_CODE = data["zipcode"]
CL_AREA = 'seattle-tacoma'
# CL_AREA = 'yakima, WA'
AREA = 'Bellevue'


def fillOutListing(d, line):
    d.find_element_by_name("FromEMail").send_keys(EMAIL)
    d.find_element_by_name("ConfirmEMail").send_keys(EMAIL)
    d.find_element_by_name("PostingTitle").send_keys(line[0])
    print('posting: ' + line[0])
    d.find_element_by_name("postal").send_keys(ZIP_CODE)
    d.find_element_by_name("GeographicArea").send_keys(AREA)
    d.find_element_by_name("PostingBody").send_keys(line[2])
    d.find_element_by_name("price").send_keys(line[1])
    d.find_element_by_name('go').click()


def parse(line):
    line[0] = line[0].strip()  # TITLE
    line[1] = line[1].strip()  # PRICE
    line[2] = line[2].strip()  # DESCRIPTION
    if line[1].startswith('$'):
        line[1] = line[1][1:]
    return line


file = csv.reader(open('D:\OneDrive\Documents\lego.csv'), delimiter=',')
for line in file:
    if len(line) != 3 and len(line[0] < 2):
        continue
    line = parse(line)

    binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    d = webdriver.Firefox(firefox_binary=binary)

    d.get("https://post.craigslist.org")
    d.find_element_by_xpath("//select[@name='n']/option[text()='" + CL_AREA + "']").click()  # post to cl location
    d.find_element_by_name('go').click()

    if 'seattle' in CL_AREA:
        d.find_element_by_xpath(
            "//input[2]").click()  # area within seattle-tacoma CL, the first [1] input box is 'seattle', 2nd i.e. [2] is eastside

    d.find_element_by_xpath("//*[text()[contains(.,'for sale by owner')]]").click()  # select category
    d.find_element_by_xpath("//*[text()[contains(.,'toys & games')]]").click()

    fillOutListing(d, line)
    d.find_element_by_class_name("continue.bigbutton").click()  # go through map

    input('continuing with next posting on enter')

print('done')
