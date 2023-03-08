# BBNS - Automate action on SWIM.

# 20230308 REPORT This demo allow login the SWIM site.
#   The site implementation is too complex for implementation with request (error like javascript support, cookies management).
#   we use selenium as abstraction.
#   needing chromium/firefox/edge browser and driver. Tested with firefox.
#   The first launch may fail (timeout).
###############################################################################
## INSTALL
# use pip with requirements.txt 
# unzip gecko driver archive and adapt webdriver_path variable.
# adapt credentials.

###############################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import time 

# Third party downloaded from github mozilla/gecko driver
webdriver_path = "C:\\Users\\Selso LIBERADO\\Downloads\\geckodriver-v0.32.0-win64"
os.environ["Path"] += os.pathsep + webdriver_path

# Set the URL and credentials for the login page
url = "http://bebesnageursstephanois.swim-community.fr/Pages/Login.aspx"
username = "xxxxxxxxxxxxxxxxx"
password = "xxxxxxxxxxxxxxxxx"

# Start a webdriver and navigate to the login page
#driver = webdriver.Chrome()
driver = webdriver.Firefox()
driver.get(url)

# Find the username and password input fields and enter the credentials
# Use browser tool to inspect the page.
driver.find_element(By.NAME, "ctl00$MainContent$UserName$tb").send_keys(username)
driver.find_element(By.NAME, "ctl00$MainContent$Password").send_keys(password)

# Find the login button and click it
#driver.find_element_by_name("login_button").click() --- does not work
driver.find_element(By.ID, "MainContent_btn_login").click()

# Wait for the page to load
driver.implicitly_wait(10)

# Print the page source
print(driver.page_source)

time.sleep(3)
driver.close()