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



class GateioBotSpider(scrapy.Spider):
    name = 'Gateio_Bot'
    allowed_domains = ['gate.io']
    start_urls = ['https://gate.io/trade/BTG_USDT']
    
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        options.add_argument('window-size=1920x1080')
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)

    def parse(self, response):
        
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()

        result['Datetime']=datetime.datetime.now()

        result['Last Current price']="N/A"#self.driver.find_element_by_xpath('').text
  
        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id= "top_last_rate_change"]/em/span').text

        result['24 Hr High Price']="N/A"#self.driver.find_element_by_xpath('').text

        result['24 Hr Low Price']= "N/A"#self.driver.find_element_by_xpath('').text

        result['24 Hr Volume']= self.driver.find_element_by_xpath('//*[@id="currVol"]').text[9:]

        result['Coins']= "Bitcoin Gold"

        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="mianTlist"]/span[1]/strong').text[7:]

        result['Exchanges URL']=response.url

        result['Exchanges']="Gate.io"

        csv_output(self.name, result)
