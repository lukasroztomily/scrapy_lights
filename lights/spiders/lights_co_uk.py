import scrapy
import os
import platform
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from lights.items import LightsItem

class LightsCoUkSpider(scrapy.Spider):
    name = 'lights_co_uk'
    start_urls = ['https://www.lights.co.uk/philips-hue-white-color-impress-led-pillar-light.html']
    
    def __init__(self):

        base = os.path.dirname(__file__)
        
        if platform.system() == 'Windows':
            driver = "chromedriver.exe"
        
        elif platform.system() == 'Darwin':
            
            if platform.machine() == 'arm64':
               driver = "chromedriverMacOSM1"
            else:
                 driver = "chromedriverMacOS"
        
        elif platform.system() == 'Linux':
               driver = "chromedriverLinux"
        
        self.PATH = os.path.join(base, 'drivers', driver)
        self.urls_ = self.start_urls[0]
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(self.PATH, options=options)
        self.driver.get(self.urls_)

    def parse(self, response):

        try:
            arvs = self.driver.find_element(By.CLASS_NAME, 'cmpboxbtn.cmpboxbtnyes')
            arvs.click()
        except NoSuchElementException:
            print(0)


        try:
            element = self.driver.find_element(By.CSS_SELECTOR, 'div[class*="cursor-pointer cl-video-control-button cl-video-control-play"]')
            webdriver.ActionChains(self.driver).move_to_element(element ).click(element ).perform()
            elements = self.driver.find_element(By.TAG_NAME , 'video')
            video = elements.get_attribute("src")
        except NoSuchElementException:
            video = None


        try:
           element = self.driver.find_element(By.CSS_SELECTOR, 'a[class*="download-file__link"]')
           self.driver.execute_script("arguments[0].click();", element)
           pdf = element.get_attribute("href")
        except NoSuchElementException:
            pdf =  None


        try:
          if video is not None:
             self.driver.get(video)
             videolink = self.driver.find_element(By.TAG_NAME, 'source').get_attribute('src')
          else:
             videolink = None
        except NoSuchElementException:
           videolink = None

        self.driver.close()
        yield scrapy.Request(url=self.urls_, callback=self.parse_file,  meta={'pdf': pdf, 'video': videolink})


    def parse_file (self, response):
        item = LightsItem()
        files = list()
        pdfs = response.meta['pdf']
        videos = response.meta['video']
        files = response.css('div.swiper-wrapper').css('picture').css('source[type="image/jpeg"]::attr(data-srcset)').extract()
        if pdfs is not None:
              files.append(response.urljoin(pdfs))
        
        if videos is not None:
              files.append(response.urljoin(videos))

        if response.status == 200:
           item['file_urls'] = files
        return item
