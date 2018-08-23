## -*- coding: utf-8 -*-
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


class ReutersBotSpider(scrapy.Spider):
    name = 'Reuters_Bot'
    allowed_domains = ['www.reuters.com']
    start_urls = ['https://www.reuters.com/finance/currencies/quote?destAmt=&srcAmt=1.00&srcCurr=USD&destCurr=KRW']
    
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        options.add_argument('window-size=1920x1080')
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        result=dict()

        result['Datetime']=datetime.datetime.now()

        result['Open']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[4]/div').text

        result['High']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div').text

        result['Low']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]/div').text

        result['Close']= self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[5]/div').text

        result['Quote Currency']= self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/h5').text.split("/")[1]

        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/h5').text.split("/")[0]

        result['Exchanges URL']=response.url


        csv_output(self.name, result)
