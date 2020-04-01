# -*- coding: utf-8 -*-
import scrapy
from collections import defaultdict
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd
import openpyxl
import sys 
import requests
from lxml import html
from datetime import datetime
import time
import numpy as np
import os
from datetime import date
from scrapy.spiders import BaseSpider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import Crawler
from scrapy.utils.log import configure_logging
#from scrapy.utils.project import get_project_settings
import ssl
from functools import wraps
import pandas as pd
import os
import requests
import traceback
import logging
import datetime
import scrapy
from scrapy.utils.response import open_in_browser

class gym_scheduler(scrapy.Spider):

    def __init__(self, email, password, package):
        self.name = 'gym_scheduler'
        self.start_urls = ['https://myflye.flyefit.ie/login']
        self.login_url = 'https://myflye.flyefit.ie/login'
        self.email = email
        self.password = password
        self.package= package
        options = {'user_1': self.user_1, 'user_2': self.user_2}
        if self.package in options:
            self.method = options[self.package]

    def parse(self, response):
        return [scrapy.FormRequest.from_response(response,
            formdata={'email_address': self.email, 'password': self.password, 'log_in': 'log in'}, callback=self.start_crawl)]

    def start_crawl(self, response):
        yield scrapy.Request('https://myflye.flyefit.ie/myflye/courses/1',callback=self.method)
    
    def package_1(self, response):
        day = datetime.datetime.today().weekday()
        if day in [4,5,6]:
            for x in response.xpath('//*[@class="class_bookable"]').extract():
                if ('SPIN') in x and ('7:00am') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl,callback=self.book)
                if ('ASS') not in x and ('7:35am') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl,callback=self.book)
        if day in [2, 3]: 
            for x in response.xpath('//*[@class="class_bookable"]').extract():
                if ('SPIN') in x and ('12:00pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl,callback=self.book)
                if ('SPIN') in x and ('12:30pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl,callback=self.book)

    def package_2(self, response):
        day = datetime.datetime.today().weekday()
        if day in [2, 3]:
            for x in response.xpath('//*[@class="class_bookable"]').extract():
                if ('SPIN') in x and ('12:00pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl,callback=self.book)
                if ('SPIN') in x and ('12:30pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl,callback=self.book)
    def book(self, response):
        return [scrapy.FormRequest.from_response(response)]

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(gym_scheduler, email='user_1_email', password='user_1_password', package='user_gym_package')
    yield runner.crawl(gym_scheduler, email='user_1_email', password='user_2_password', package='user_gym_package')
    reactor.stop()

def main():
   crawl()
   reactor.run() # the script will block here until the last crawl call is finished

if __name__ == '__main__':
    main()
