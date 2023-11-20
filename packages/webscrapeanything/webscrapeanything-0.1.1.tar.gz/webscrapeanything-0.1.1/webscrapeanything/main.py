import csv
import os
import time
import pickle
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class Scraper:
    def __init__(self, config):
        self.config = config
        self.driver = self.configure_webdriver()
        self.output_file = self.config.get('output_file', 'scraped_data.csv')

    @staticmethod
    def print_config_template():
        config_template = {
            "login": "Whether a login is required (true/false)",
            "loginURL": "The URL to the login page if login is required",
            "hide_browser": "Whether to run the browser in headless mode (true/false)",
            "website": "The main website URL to start scraping from",
            "output_file": "The path to the output file where the results will be saved",
            # Include all other config parameters with their descriptions
        }
        print(json.dumps(config_template, indent=4))

    def configure_webdriver(self):
        options = webdriver.ChromeOptions()
        # Set user agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.4567.789 Safari/537.36")
        # Check if login is required
        if self.config.get('login') and self.config.get('loginURL'):
            # Navigate to login URL and wait for the user to press 'Enter'
            driver = webdriver.Chrome(options=options)
            driver.get(self.config['loginURL'])
            input("Press Enter after logging in...")
            # Save cookies for future use
            cookies = driver.get_cookies()
            with open('cookies.pkl', 'wb') as cookies_file:
                pickle.dump(cookies, cookies_file)
            driver.quit()
        elif self.config.get('cookies'):
            # Load cookies if available
            try:
                with open('cookies.pkl', 'rb') as cookies_file:
                    cookies = pickle.load(cookies_file)
                    user_data_dir = os.path.abspath(self.config['user_data_dir'])
                    options.add_argument(f"user-data-dir={user_data_dir}")
                    for cookie in cookies:
                        options.add_argument(f"--cookie={cookie}")
                print("Loaded cookies:")
            except FileNotFoundError:
                print("Cookies file not found.")
            if self.config.get('hide_browser'):
                options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
        else:
            if self.config.get('hide_browser'):
                options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
        return driver

    def accept_cookies(self):
        if self.config.get('accept_cookies'):
            try:
                accept_cookies_button = self.driver.find_element(By.XPATH, self.config['accept_cookies_xpath'])
                accept_cookies_button.click()
            except NoSuchElementException:
                print("Accept cookies button not found.")

    def login(self):
        if self.config.get('login'):
            print(f"Please log in at {self.config['loginURL']} and press 'Enter' in the terminal.")
            input("Press 'Enter' when ready...")
            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def load_cookies(self):
        if os.path.exists('cookies.pkl') and self.config.get('cookies'):
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def handle_pagination(self, current_page):
        if current_page <= (self.config['total_elements'] - 1) // self.config['elements_per_page'] + 1:
            next_button = self.driver.find_element(By.XPATH, self.config['next_button_xpath'])
            next_button.click()

    def handle_infinite_scroll(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.config.get('infinite_scroll_wait', 2))
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scrape_spider_crawl(self):
        data_to_write = []
        for i in range(self.config['start_i'], self.config['start_i'] + self.config['elements_per_page']):
            element_xpath = self.config['target_element_xpath'].format(i=i)
            try:
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
                element.click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.config['spider_crawl_target_element_1'])))
                scraped_data = {fieldname: self.driver.find_element(By.XPATH, self.config[f'spider_crawl_target_element_{index}']).text
                                for index, fieldname in enumerate(['Element1', 'Element2', 'Element3'], start=1)}
                data_to_write.append(scraped_data)
                if self.config.get('spider_javascript_button'):
                    self.driver.back()
                else:
                    self.driver.execute_script("window.history.go(-1)")
            except NoSuchElementException:
                print(f"No such element: {element_xpath}")
        return data_to_write

    def scrape_group_data(self):
        data_to_write = []
        for i in range(self.config['start_i'], self.config['start_i'] + self.config['elements_per_page']):
            xpath1 = self.config['target_element_xpath'].format(i=i)
            xpath2 = self.config['target_element2_xpath'].format(i=i)
            try:
                element1 = self.driver.find_element(By.XPATH, xpath1)
                element2 = self.driver.find_element(By.XPATH, xpath2)
                data_to_write.append({'Element1': element1.text, 'Element2': element2.text})
            except NoSuchElementException:
                print(f"Elements at {xpath1} or {xpath2} not found.")
        return data_to_write
                
    def scrape_individual_elements(self):
        data_to_write = []
        start_index = self.config['start_i']
        elements_per_page = self.config.get('elements_per_page', 1)
        total_elements = self.config.get('total_elements', 1)
        
        for i in range(start_index, start_index + total_elements):
            xpath = self.config['target_element_xpath'].format(i=i)
            try:
                element = self.driver.find_element(By.XPATH, xpath)
                data_to_write.append({'Element': element.text})
            except NoSuchElementException:
                print(f"Element with XPath {xpath} not found.")
        return data_to_write


    def scrape_elements(self):
        self.driver.get(self.config['website'])
        self.load_cookies()
        self.accept_cookies()

        if self.config.get('initial_wait'):
            time.sleep(self.config['initial_wait_time'])

        with open(self.output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.config.get('fieldnames', ['Element1', 'Element2', 'Element3']))
            writer.writeheader()

            current_page = 1
            total_pages = (self.config['total_elements'] - 1) // self.config['elements_per_page'] + 1

            while current_page <= total_pages:
                if self.config.get('spider_crawl'):
                    data_to_write = self.scrape_spider_crawl()
                elif self.config.get('group_data'):
                    data_to_write = self.scrape_group_data()
                else:
                    data_to_write = self.scrape_individual_elements()

                for row in data_to_write:
                    writer.writerow(row)

                if self.config.get('pagination'):
                    self.handle_pagination(current_page)
                elif self.config.get('infinite_scroll'):
                    self.handle_infinite_scroll()

                current_page += 1

    def start_scraping(self):
        try:
            self.login()
            self.scrape_elements()
        finally:
            self.driver.quit()
