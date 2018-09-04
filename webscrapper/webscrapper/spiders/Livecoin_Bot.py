# -*- coding: utf-8 -*-
#WEBSITE doesn't contain the required datas,hence NULL is used for them.

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



class LivecoinBotSpider(scrapy.Spider):
    name = 'Livecoin_Bot'
    allowed_domains = ['www.livecoin.net']
    start_urls = ['http://www.livecoin.net/']
    handle_httpstatus_list = [404]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        #options.add_argument('window-size=1366x168')
        #options.addArgument("--start-maximized");
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)
        self.driver.maximize_window()

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(10)
        result=dict()
        result['Datetime']=datetime.datetime.now()
        result['Last Current price']="NA"
        
        result['24 Hr Price Change']="NA"
        
        result['24 Hr High Price']="NA"
        
        result['24 Hr Low Price']= "NA"
        
        result['24 Hr Volume']= "NA"
        
        result['Coins']= "Tezos"
        
        result['Base Currency']="USDT"
        
        result['Exchanges URL']=response.url
        
        result['Exchanges']="LiveCoin"
        
        csv_output(self.name, result)