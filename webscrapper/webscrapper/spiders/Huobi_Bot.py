# -*- coding: utf-8 -*-
import scrapy
import csv
from os import path
import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time
from string import digits

def csv_output(spyder_name, dic):
        file_name = "%s.csv"%(spyder_name)
        if not path.exists(file_name):
            with open(file_name,'a+',newline='') as csv_file:
                writer=csv.writer(csv_file)
                writer.writerow(dic.keys())
        with open(file_name,'a+',newline='') as csv_file:
            writer=csv.writer(csv_file)
            writer.writerow(dic.values())


class HuobiBotSpider(scrapy.Spider):
    name = 'Huobi_Bot'
    allowed_domains = ['www.huobi.com']
    start_urls = ['http://www.huobi.com/xrp_usdt/exchange//']
    
        
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()    
        mystr=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dt').text
        remove_digits = str.maketrans('', '', digits)
        data=mystr.translate(remove_digits)
        s=data.split('/')
        result['Datetime']=datetime.datetime.now()

        result['Last Current price']=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dt/span').text

        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[2]/span').text

        result['24 Hr High Price']=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[3]/span').text

        result['24 Hr Low Price']= self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[4]/span').text

        result['24 Hr Volume']= (self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[5]/span').text).split()[0]

        result['Coins']= s[0]

        result['Base Currency']=s[1]

        result['Exchanges URL']=response.url

        result['Exchanges']="Huobi"

        csv_output(self.name, result)


   
