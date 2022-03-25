#-------------------------------------------------------------------------
# SocialTool App
# Easy module To Use, based on selenium to controle on your multi accounts on the social media platforms.
# Version : 1.0.0
# Developed By : Ahmed Hanfy Bekheet
# Python Version : 3.9.0
# Date : 3/25/2022
#-------------------------------------------------------------------------



import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class Browser():
    options = Options()

    def get_proxies(self,num_of_proxies:int) -> list[str]: 
        '''
        get_proxies(num_of_proxies:int) -> list[str]
        Fuction Used To Get no.proxies As Set With Its Ports (e.g: ["1.0.0.0:80"])
        You Can Use It To Get proxies Only That Has Good Connetions
        Parameters
        ----------
            num_of_proxies : int
            Number Of Proxies depend on num_of_proxies param.

        '''
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        pareser = etree.HTML(response.content)
        proxies = list()
        count = 1
        while len(proxies) < num_of_proxies:
                ip = pareser.xpath(f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{count}]/td[1]')[0].text
                port = pareser.xpath(f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{count + 1 }]/td[2]')[0].text
                proxies.append(f"{ip}:{port}")
                count += 1            
        return proxies

    def using_proxy(self):
        '''add proxy to option instance to used it in driver later'''
        proxy = self.get_proxies(1)[0]
        self.options.add_argument(f"--proxy-server={proxy}")

    def hide(self):
        '''add arguments to hide windows'''
        self.options.add_argument("--headless") ##Use HeadLess Mode
        self.options.add_argument('--no-sandbox') 
        self.options.add_argument('--disable-gpu')  
        self.options.add_argument('log-level=3')  ##Hide Concole Warning/Errors 
        
    def launch_driver(self,driver_path):
        self.options.add_argument('--enable-popup-blocking')  
        self.s = Service(driver_path)
        self.driver = webdriver.Chrome(service = self.s,options=self.options) #create driver

    def open_facebook_acc(self,email,password):
        
        #Get facebook page
        self.driver.get("https://www.facebook.com/login")

        ##Initialize Fields
        email_field = self.driver.find_element(By.XPATH,'//*[@id="email"]')
        password_field = self.driver.find_element(By.XPATH,'//*[@id="pass"]')
        login_button = self.driver.find_element(By.XPATH,'//*[@id="loginbutton"]')

        ## Pass Acc Detail To Fields   ===Login To Account
        email_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()
        
        
        ## Check Successfully Of Login
        try:
            self.driver.find_element(By.XPATH,'//*[@id="login_form"]')
        except:
            self.login_success = True
        else:
            raise ValueError( "The password that you've entered is incorrect")

    def comment_on_post(self,post_url,comment):
        self.driver.get(post_url)  ##Get Post 
        comment_field = self.driver.find_element(By.CSS_SELECTOR,'div[aria-label="Write a comment"]') 
        comment_field.send_keys(comment,Keys.ENTER)

    def comment_as_spam(self,post_url,comment, no_times):
        self.driver.get(post_url)
        comment_field = self.driver.find_element(By.CSS_SELECTOR,'div[aria-label="Write a comment"]')
        for i in range(no_times):
            comment_field.send_keys(comment,Keys.ENTER)

    def share_post(self,post_url):
        self.driver.get(post_url)
        page_id = self.driver.find_element(By.XPATH,'/html/body/div[1]')
        self.driver.find_element(By.XPATH,'/html/body').click()
        share_button = self.driver.find_element(By.CSS_SELECTOR,'div[aria-label="Send this to friends or post it on your timeline."]')
        share_button.click()
        time.sleep(2)
        share_now_button = self.driver.find_element(By.XPATH,f'//*[@id="{page_id.get_attribute("id")}"]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div/div/span/span')
        share_now_button.click()