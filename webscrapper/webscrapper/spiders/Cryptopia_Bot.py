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


class CryptopiaBotSpider(scrapy.Spider):
    name = 'Cryptopia_Bot'
    allowed_domains = ['www.cryptopia.co.nz']
    start_urls = ['https://www.cryptopia.co.nz/Exchange?market=EOS_BTC']
    
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
        time.sleep(10)
        result=dict()

        result['Datetime']=datetime.datetime.now()

        result['Last Current price']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/b').text

        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[3]/div/b[1]').text+"%"

        result['24 Hr High Price']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/div/b').text

        result['24 Hr Low Price']= self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[5]/div/b').text

        result['24 Hr Volume']= self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[2]/td/b[2]').text

        result['Coins']= self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[1]/div/div[2]/span[1]').text

        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[1]/div/div[2]/span[2]').text

        result['Exchanges URL']=response.url

        result['Exchanges']="Cryptopia"

        csv_output(self.name, result)

