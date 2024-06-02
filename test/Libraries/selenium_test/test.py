from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Edge()

driver.get('https://paderewski-konkurs-hnol.vercel.app')

#search_box = driver.find_element(By.NAME, 'q')

#search_box.send_keys('Selenium Python')

#search_box.send_keys(Keys.RETURN)

time.sleep(15)

driver.quit()
 