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

driver.get("https://shop.coles.com.au/a/a-nsw-metro-alexandria/everything/browse")

categories = driver.find_elements_by_xpath("/html/body/div[10]/div[2]/div[1]/div/div[2]/nav/div/div/div[2]/ul/li/a")
urls = []
cat_dict = {}
for category in categories:
    url = category.get_attribute("href")
    urls.append(url)
    cat_name = category.get_attribute("innerHTML")
    sel = html.fromstring(cat_name)

    cat = sel.xpath("//span[@class='item-title']/text()")[0]
    if cat in unwanted_Categories:
        continue
    cat_dict[cat] = {"url":url}
    # print (remove_tags(cat_name),url)

for cat,cat_details in cat_dict.items():
    driver.get(cat_details["url"])
    driver.set_page_load_timeout(30)
    sub_cats = driver.find_elements_by_xpath("/html/body/div[9]/div[2]/div[1]/div/div[2]/nav/div/div/div[3]/ul/li/a")
    sub_cats_urls = [sub_cat.get_attribute("href") for sub_cat in sub_cats]
    sub_cats_name = []
    for sub_cat in sub_cats:
        sub_cat_url = sub_cat.get_attribute("href")
        sub_cat_html = sub_cat.get_attribute("innerHTML")
        sub_cat_selector = html.fromstring(sub_cat_html)
        sub_cat_text = sub_cat_selector.xpath("//span[@class='item-title']/text()")[0]

        cat_dict[cat][sub_cat_text] = {"url":sub_cat_url}

def get_data(urls):
    data = []
    for url in urls:
        driver.get(url)
        time.sleep(5)
        title = ""
        try:
            title = driver.find_element_by_xpath('//*[@id="pdp-product-title"]/span/span[3]').get_attribute("innerHTML")
            title = remove_tags(title).replace("&amp;","&")
        except:
            title = ""
        text = ""
        try:
            text = driver.find_element_by_xpath('//*[@id="main-content-inside"]/div[2]/div/section/div[2]/div/div[2]/p').get_attribute("innerHTML")
            text = remove_tags(text).replace("&amp;","&")
            # //*[@id="main-content-inside"]/div[2]/div/section/div[2]/div/div[2]/p
        except:
            text = ""
        if len(text.split()) > 8:
            data.append({"description":text,"title":title,"category":cat+"_"+sub_cat})
    return data

data_samples = []
for cat,cat_details in cat_dict.items():
    counter = 0
    for sub_cat,sub_cat_dict in cat_details.items():
        if "url" in sub_cat_dict:
            try: 
                driver.get(sub_cat_dict["url"])
                driver.set_page_load_timeout(30)
                time.sleep(5)
                data = driver.find_elements_by_xpath('//div[@class="colrs-animate tile-animate"]/div/div/div/header/h3/a')
                urls = [url.get_attribute("href") for url in data]
                data_list = get_data(urls)
                data_samples += data_list
                if len(urls) < 48:
                    continue
                else:
                    for idx in range(2,10):
                        response_url = sub_cat_dict["url"].replace("?pageNumber=1","?pageNumber="+str(idx))
                        driver.get(response_url)
                        driver.set_page_load_timeout(30)
                        time.sleep(5)
                        urls_page = []
                        try:
                            data = driver.find_elements_by_xpath('//div[@class="colrs-animate tile-animate"]/div/div/div/header/h3/a')
                            urls_page = [url.get_attribute("href") for url in data]
                            data_list = get_data(urls_page)
                            data_samples += data_list
                        except:
                            pass
                        if len(urls_page) < 48:
                            break
            except:
                pass

driver.close()
json.dump(data_samples,open("data2.json","w"))

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