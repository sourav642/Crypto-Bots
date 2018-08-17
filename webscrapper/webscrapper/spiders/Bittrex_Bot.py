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

class BittrexBotSpider(scrapy.Spider):
    name = 'Bittrex_Bot'
    allowed_domains = ['www.bittrex.com']
    start_urls = ['https://www.bittrex.com/home/markets/']
    
    
        
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        options.add_argument('window-size=1920x1080')
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()
        result['Datetime']=datetime.datetime.now()
        i=0
        
        while self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']').get_attribute("title")!="Go to USDT-TRX (TRON)...":
            i+=1
        
        result['Last Current price']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr[12]/td[5]').text
        
        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr[12]/td[4]/span[1]').text
        
        result['24 Hr High Price']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[6]').text+"%"
        
        result['24 Hr Low Price']= self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[7]').text
        
        result['24 Hr Volume']= self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[3]').text
        
        result['Coins']= self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[2]').text
        
        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/div/div/h2/span[1]').text
        
        result['Exchanges URL']=response.url
        
        result['Exchanges']="Bittrex"
        csv_output(self.name, result)
       
        
 
 
        
        
