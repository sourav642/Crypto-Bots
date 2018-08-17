# -*- coding: utf-8 -*-
import scrapy
import csv
from os import path
import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time

def csv_output(spyder_name, dic):
        file_name = "%s.csv"%(spyder_name)
        if not path.exists(file_name):
            with open(file_name,'a+',newline='') as csv_file:
                writer=csv.writer(csv_file)
                writer.writerow(dic.keys())
        with open(file_name,'a+',newline='') as csv_file:
            writer=csv.writer(csv_file)
            writer.writerow(dic.values())
            

class BitstampBotSpider(scrapy.Spider):
    name = 'Bitstamp_Bot'
    allowed_domains = ['www.bitstamp.net']
    start_urls = ['https://www.bitstamp.net/']

    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        options.add_argument('window-size=1920x1080')
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)
        
    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url)
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="overview-pairs"]/li[7]/a').click()
        result=dict()
        mystr=self.driver.find_element_by_xpath('//*[@id="overview-pairs"]/li[7]/a').text
        s=mystr.split(' / ')

        result['Datetime']=datetime.datetime.now()
        
        result['Last Current price']=self.driver.find_element_by_xpath('//*[@id="ticker-price"]').text

        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id="price-change-pct"]').text+"%"

        result['24 Hr High Price']=self.driver.find_element_by_xpath('//*[@id="high-price"]').text

        result['24 Hr Low Price']= self.driver.find_element_by_xpath('//*[@id="low-price"]').text

        result['24 Hr Volume']= self.driver.find_element_by_xpath('//*[@id="low-price"]').text

        result['Coins']= s[0]

        result['Base Currency']=s[1]

        result['Exchanges URL']=response.url

        result['Exchanges']="Bitstamp"

        csv_output(self.name, result)

