#!/usr/bin/python3
import scrapy
from datetime import datetime
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


class gym_scheduler(scrapy.Spider):
    def __init__(self, email, password, package):
        self.name = 'gym_scheduler'
        self.start_urls = ['https://myflye.flyefit.ie/login']
        self.login_url = 'https://myflye.flyefit.ie/login'
        self.email = email
        self.password = password
        self.package = package
        options = {'user_1': self.user_1, 'user_2': self.user_2}
        if self.package in options:
            self.method = options[self.package]

    def parse(self, response):
        """
        Function which uses scrapy form request function
        to login into gym website

        Parameters:
        response: url response which is then passed into the parse function

        Returns
        site data from member page which is then parsed in
        start_crawl function
        """

        return [scrapy.FormRequest.from_response(response,
                formdata={'email_address': self.email,
                          'password': self.password,
                          'log_in': 'log in'},
                          callback=self.start_crawl)]

    def start_crawl(self, response):
        """
        Function which calls chosen method(user_1 or user_2) and then
        applies the this to the gym site and books desired classes

        Parameters:
        response: url response which is then passed into the parse function


        Returns
        Books desired classes
        """

        yield scrapy.Request('https://myflye.flyefit.ie/myflye/courses/1',
                             callback=self.method)

    def user_1(self, response):
        """
        Function detailing which classes to book

        Parameters:
        response: url response which is then passed into the parse function

        Returns
        books desired classes
        """

        day = datetime.datetime.today().weekday()
        if day in [4, 5, 6]:
            for x in response.xpath('//*[@class="class_bookable"]').extract():
                if ('SPIN') in x and ('7:00am') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/\
                                myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl, callback=self.book)
                if ('ASS') not in x and ('7:35am') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/\
                                myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl, callback=self.book)
        if day in [2, 3]:
            for x in response.xpath('//*[@class="class_bookable"]').extract():
                if ('SPIN') in x and ('12:00pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/\
                                myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl, callback=self.book)
                if ('SPIN') in x and ('12:30pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/\
                                myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl, callback=self.book)

    def user_2(self, response):
        """
        Function detailing which classes to book

        Parameters:
        response: url response which is then passed into the parse function

        Returns
        books desired classes
        """

        day = datetime.datetime.today().weekday()
        if day in [2, 3]:
            for x in response.xpath('//*[@class="class_bookable"]').extract():
                if ('SPIN') in x and ('12:00pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/\
                                myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl, callback=self.book)
                if ('SPIN') in x and ('12:30pm') in x:
                    y = x.split()[6].split('/')[-1][:-2]
                    spin_cl = f'https://myflye.flyefit.ie/\
                                myflye/course-book/{y}'
                    print(spin_cl)
                    yield scrapy.Request(spin_cl, callback=self.book)

    def book(self, response):
        """
        Function used to execute booking of a class

        Parameters:
        response: url response which is then passed into the parse function


        Returns
        books specific class by submitting scrapy form request
        """
        return [scrapy.FormRequest.from_response(response)]


configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    """
    Function to run multiple spiders

    Returns
    runs spiders in order given
    """
    yield runner.crawl(gym_scheduler, email='user_1_email',
                       password='user_1_pw', package='user_1')
    yield runner.crawl(gym_scheduler, email='user_2_email',
                       password='user_2_pw', package='user_2')
    reactor.stop()


def main():
    crawl()
    reactor.run()


if __name__ == '__main__':
    main()
