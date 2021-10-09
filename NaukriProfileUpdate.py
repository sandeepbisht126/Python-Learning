# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 17:25:08 2021

@author: aitsa
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from io import StringIO
from keyboard import press
import re
from datetime import datetime


url_link='https://www.naukri.com/mnjuser/homepage'
options = Options()
options.headless = True
#browser = webdriver.Chrome(executable_path=r'C:\Users\aitsa\Downloads\chromedriver_win32\chromedriver.exe')
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url_link) 
login='#usernameField'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,login)))
elem=browser.find_element_by_css_selector(login)
elem.send_keys('sandeep.bisht126@gmail.com')
passwrd='#passwordField'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,passwrd)))
elem=browser.find_element_by_css_selector(passwrd)
elem.send_keys('Sandy@87')
elem.submit()
editprofile='#root > div > div > span > div > div > div > div.container > div > div.col.s4.sidebar > div.profile-section-wrapper > div > a.row > div.personal-info.col.s12.center > div.user-name.roboto-bold-text'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,editprofile)))
elem=browser.find_element_by_css_selector(editprofile)
elem.click()
editHeading='#lazyResumeHead > div > div > div > div.widgetHead > span.edit.icon'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,editHeading)))
elem=browser.find_element_by_css_selector(editHeading)
elem.click()
savechanges='body > div.ltCont > div.lightbox.profileEditDrawer.resumeHeadlineEdit.model_open.flipOpen > div:nth-child(2) > form > div:nth-child(3) > div > button'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,savechanges)))
elem=browser.find_element_by_css_selector(savechanges)
elem.submit()
'''
uploadresume='#attachCV'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,uploadresume)))
elem=browser.find_element_by_css_selector(uploadresume)
elem.submit()
'''
NaukriProfileUpdate.py