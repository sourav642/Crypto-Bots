# -*- coding: utf-8 -*-
import scrapy
import csv
from os import path
import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time
from googletrans import Translator

def csv_output(spyder_name, dic):
        file_name = "%s.csv"%(spyder_name)
        if not path.exists(file_name):
            with open(file_name,'a+',newline='') as csv_file:
                writer=csv.writer(csv_file)
                writer.writerow(dic.keys())
        with open(file_name,'a+',newline='') as csv_file:
            writer=csv.writer(csv_file)
            writer.writerow(dic.values())
            
class UpbitBotSpider(scrapy.Spider):
    name = 'Upbit_Bot'
    allowed_domains = ['upbit.com']
    start_urls = ['https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC']
    
    def __init__(self):
        #options = Options()
        #options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("E:/chromedriver.exe")#,chrome_options=options)
    
    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(10)
        result=dict()
        translator = Translator()
        result['Datetime']=datetime.datetime.now()

        result['Last Current price']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[1]/span[1]/strong').text

        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[1]/span[2]/strong[1]').text

        result['24 Hr High Price']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[3]/dl[1]/dd[1]/strong').text

        result['24 Hr Low Price']= self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[3]/dl[1]/dd[2]/strong').text

        result['24 Hr Volume']= self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[3]/dl[2]/dd[1]/strong').text

        result['Coins']= translator.translate(self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/span/a/strong').text, dest='en')

        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[1]/span[1]/em').text

        result['Exchanges URL']=response.url

        result['Exchanges']="Upbit"

        csv_output(self.name, result)
