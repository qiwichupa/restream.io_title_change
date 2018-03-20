#!/usr/bin/env python3
''' 
If you need to change title (dash) on restream.io automatically, this script will help you.

You must create 'chrome_home_dir' and run this script with --manual key, 
it will opened chrome without virtual display and let you authorize 
on restream.io. It is neccessary because of captcha, and you will be forced
to repeat this procedure from time to time =(. But after that you can run
$ scriptname.py "new title"
and "new title" will be applied to your stream.

REQUIREMENTS:
modules: pyvirtualdisplay, selenium
soft: chromium-chromedriver, chromium-browser, xvfb

'''


import sys,os
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

############
# SETTINGS #
############
chromedriver_path = "/usr/lib/chromium-browser/chromedriver"
chrome_home_dir = "/var/www/garage.qiwichupa.net/docs/ownscripts/garage_shed2dash/Chrome_Profile/"
reio_url = "https://restream.io/"

def manual_login():
    '''Run chromium without virtual display'''
    driver = create_chrome_driver()
    # open login page
    driver.get(reio_url)
    # dirty hack, chrome remains opened until manually close (or if 'impossible_element' is found)
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "impossible_element"))
    )
    exit()


def create_chrome_driver():
    o = Options()
    o.add_argument("--user-data-dir=" + chrome_home_dir)
    driver = webdriver.Chrome(chromedriver_path,chrome_options=o)
    driver.implicitly_wait(1)
    return driver

def create_virt_display():
    display = Display(visible=0, size=(1203, 704))
    display.start()
    return display



#   MAIN   
os.system("killall chromium-browser")

if sys.argv[1] == "--manual":
    manual_login()

newDash = sys.argv[1]

display = create_virt_display()
driver = create_chrome_driver()
driver.get(reio_url)


# try to go to titles page
try:
    # check page (main page of restream.io) with ID "jsChannelList" is loaded
    element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "jsChannelList"))
    )
except:
    driver.close()
    os.system("killall chromium-browser")
finally:
    # click link of title change page
    reDashLinkSelector = "a[href='/titles']" 
    driver.find_element_by_css_selector(reDashLinkSelector).click()


# try to change title
try:
    # another check
    element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "jsChannelTitleList"))
    )
except:
    driver.close()
    os.system("killall chromium-browser")
finally:
    # select main title field 
    title = driver.find_element_by_name("all-titles")
    # click on it
    title.click()
    # send our title to field
    title.send_keys(newDash)
    # select  and click update button
    driver.find_element_by_css_selector("input[value='Update All']").click()
    title.send_keys(Keys.RETURN)
  
# close browser
driver.close()

# close virtual display
display.stop()
sleep(10)
os.system("killall chromium-browser")
