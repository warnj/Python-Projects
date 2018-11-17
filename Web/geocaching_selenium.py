from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time, json

data = json.loads(open('../personal_data.json').read())
driver = webdriver.Firefox()

driver.get("https://www.geocaching.com/login/")
assert "Geocaching" in driver.title

elem = driver.find_element_by_name("ctl00$ContentBody$tbUsername")
elem.send_keys(data["geocaching_username"])
elem = driver.find_element_by_name("ctl00$ContentBody$tbPassword")
elem.send_keys(data["geocaching_password"])
elem = driver.find_element_by_name("ctl00$ContentBody$cbRememberMe")
elem.click()
elem.send_keys(Keys.RETURN)


driver.get("https://www.geocaching.com/seek/nearest.aspx?t=m&origin_lat=46.671341&origin_long=-120.621282&dist=100&submit3=Search")
driver.maximize_window()
# insanely long path through the html to the link of the first result
for i in range(1, 11): # for each increment of i, we go to 2 search results
    elem = driver.find_element_by_xpath("/html/body/form[@id='aspnetForm']/section[@id='Content']/div[@class='container']/div[@id='divContentMain']/div[@id='ctl00_ContentBody_ResultsPanel']/table[@class='SearchResultsTable Table']/tbody/tr[@class='SolidRow Data BorderTop'][" + str(i) + "]/td[@class='Merge']")
    elem.click()
    elem = driver.find_element_by_xpath("/html")
    elem.send_keys(Keys.ALT, Keys.LEFT) #go back
    time.sleep(.1)
    #parse some html
    elem = driver.find_element_by_xpath("/html/body/form[@id='aspnetForm']/section[@id='Content']/div[@class='container']/div[@id='divContentMain']/div[@id='ctl00_ContentBody_ResultsPanel']/table[@class='SearchResultsTable Table']/tbody/tr[@class='AlternatingRow Data BorderTop'][" + str(i) + "]/td[@class='Merge']")
    elem.click()
    elem = driver.find_element_by_xpath("/html")
    elem.send_keys(Keys.ALT, Keys.LEFT) #go back
    time.sleep(.1)
    #parse some html


#driver.close()