# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException,TimeoutException
from lxml import html
from scrapy.utils.markup import remove_tags
import time,json,os,re
import timeit,sys,random
from collections import defaultdict
import urlparse
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

unwanted_Categories = ["Tobacco","Spring","Entertaining at Home","Liquor"]
driver = webdriver.PhantomJS()
# driver = webdriver.Chrome("/home/ashmit/chromedriver")
driver.set_page_load_timeout(30)

driver.get("https://shop.coles.com.au/a/a-nsw-metro-westmead/everything/browse")

print ([each.get_attribute("innerHTML") for each in driver.find_elements_by_xpath("//div")])

driver.close()
json.dump(data_samples,open("data.json","w"))

#         # print (data.get_attribute("text"))
#         final_urls += urls
#     final_urls = list(set(final_urls))

# # print (len(final_urls))
# # print (final_urls) 
# urllist = open("output.txt","r").read().split("\n")
# for url in urllist[:20]:
#     

# https://shop.coles.com.au/online/a-nsw-metro-alexandria
# print (json.dumps(cat_dict,indent=4))