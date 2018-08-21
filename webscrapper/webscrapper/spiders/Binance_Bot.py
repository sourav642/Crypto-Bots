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




class BinanceBotSpider(scrapy.Spider):
    name = 'Binance_Bot'
    allowed_domains = ["www.binance.com"]
    start_urls = ["https://www.binance.com/en/trade/BTC_USDT"]
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    
    def __init__(self):
        options = Options()
        #options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        #options.add_argument('window-size=1366x168')
        #options.addArgument("--start-maximized");
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)
        self.driver.maximize_window()

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()
        result['Datetime']=datetime.datetime.now()
        
        result['Last Current price']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span').text
        
        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]/span[2]').text.split()[0]
        
        result['24 Hr High Price']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/span').text
        
        result['24 Hr Low Price']= self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/span').text
        
        result['24 Hr Volume']= self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[5]/span').text.split()[0]
        
        result['Coins']= self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/h2/div/a').text
        
        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/h2/span[2]').text.split()[1]
        
        result['Exchanges URL']=response.url
        
        result['Exchanges']="Binance"
        
        csv_output(self.name, result)


