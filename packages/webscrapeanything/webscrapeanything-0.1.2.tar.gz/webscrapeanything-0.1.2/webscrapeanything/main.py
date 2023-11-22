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
import pkg_resources
from setuptools import setup, find_packages  # if you're writing your setup.py
import shutil
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import boto3
from botocore.exceptions import ClientError





class Scraper:
    def __init__(self, config):
        self.config = config
        self.driver = self.configure_webdriver()
        self.output_file = self.config.get('output_file', 'scraped_data.csv')

    def deploy_api_to_aws(self, lambda_function_name, api_name, db_credentials, query_parameters):
        """
        Deploy an API to AWS that will extract data from an SQL database on AWS RDS.
        """
        lambda_client = boto3.client('lambda')
        api_gateway_client = boto3.client('apigateway')

        # Lambda function code that interacts with the SQL database
        lambda_function_code = """
import json
import pymysql

def lambda_handler(event, context):
    # Connect to the database
    connection = pymysql.connect(
        host=event['host'],
        user=event['user'],
        password=event['password'],
        database=event['database']
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # Construct the query based on event parameters
    query = "SELECT * FROM your_table WHERE "
    query += " AND ".join(f"{key} = %s" for key in event['query_parameters'])
    
    # Execute the query
    cursor.execute(query, list(event['query_parameters'].values()))
    
    # Fetch the results
    result = cursor.fetchall()
    
    # Close the connection
    cursor.close()
    connection.close()
    
    # Return the result
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
"""
        try:
            # Deploy the Lambda function
            response = lambda_client.create_function(
                FunctionName=lambda_function_name,
                Runtime='python3.8',
                Role='arn:aws:iam::account-id:role/lambda_basic_execution',
                Handler='index.lambda_handler',
                Code={'ZipFile': lambda_function_code}
            )
            lambda_arn = response['FunctionArn']
            
            # Deploy the API Gateway
            api_response = api_gateway_client.create_rest_api(
                name=api_name,
                description='API for accessing SQL data from AWS RDS'
            )
            root_resource_id = api_response['id']
            
            # Create a new resource (endpoint)
            resource_response = api_gateway_client.create_resource(
                restApiId=root_resource_id,
                parentId=root_resource_id,
                pathPart='{proxy+}'
            )
            resource_id = resource_response['id']
            
            # Create a GET method on the new resource
            method_response = api_gateway_client.put_method(
                restApiId=root_resource_id,
                resourceId=resource_id,
                httpMethod='GET',
                authorizationType='NONE'
            )
            
            # Set the Lambda function as the GET method's backend integration
            integration_response = api_gateway_client.put_integration(
                restApiId=root_resource_id,
                resourceId=resource_id,
                httpMethod='GET',
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=f'arn:aws:apigateway:region:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
            )
            
            # Deploy the API to make it publicly accessible
            deployment_response = api_gateway_client.create_deployment(
                restApiId=root_resource_id,
                stageName='prod'
            )
            print("API deployed! Access it at:")
            print(f"https://{root_resource_id}.execute-api.region.amazonaws.com/prod/")
        except ClientError as e:
            print(f"An error occurred: {e}")

            
    @staticmethod
    def list_available_templates():
        """
        Lists all .json files in the templates directory.
        """
        templates_dir = pkg_resources.resource_filename(__name__, 'templates')
        templates = [f for f in os.listdir(templates_dir) if f.endswith('.json')]
        print("Available templates:")
        for template in templates:
            print(template)

    @staticmethod
    def download_template(template_name):
        """
        Copies the specified template JSON file to the user's current working directory.
        """
        templates_dir = pkg_resources.resource_filename(__name__, 'templates')
        template_path = os.path.join(templates_dir, template_name)
        download_dir = os.getcwd()  # Current working directory
        if os.path.isfile(template_path):
            shutil.copy(template_path, download_dir)
            print(f"Template '{template_name}' has been copied to {download_dir}")
        else:
            print(f"Template '{template_name}' does not exist in the templates directory.")

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

    def upload_to_google_sheets(self, data, sheet_name):
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']

        # The file token.json should be in the same directory as your script,
        # or provide the full path to the file
        creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
        client = gspread.authorize(creds)

        # Open the spreadsheet by name
        sheet = client.open(sheet_name).sheet1

        # Assuming `data` is a list of dictionaries, where keys are column headers
        # First row of the spreadsheet will be headers
        fieldnames = data[0].keys()
        all_values = [list(fieldnames)] + [list(item.values()) for item in data]

        # Update the sheet with data
        sheet.update('A1', all_values)



    def schedule_script_on_aws(self, lambda_function_name, schedule_expression):
        lambda_client = boto3.client('lambda')
        events_client = boto3.client('events')

        try:
            # Create or update the Lambda function
            # You'd need to have your function zipped and uploaded to S3 or defined inline
            # This is a placeholder for the function's code.
            lambda_client.create_function(
                FunctionName=lambda_function_name,
                Runtime='python3.8',
                Role='arn:aws:iam::account-id:role/lambda_basic_execution',
                Handler='script.handler',
                Code={
                    'S3Bucket': 'bucket-name',
                    'S3Key': 'function-code.zip'
                }
            )
            
            # Grant the necessary permissions
            lambda_client.add_permission(
                FunctionName=lambda_function_name,
                StatementId='scheduler-statement',
                Action='lambda:InvokeFunction',
                Principal='events.amazonaws.com',
                SourceArn='arn:aws:events:region:account-id:rule/rule-name'
            )
            
            # Schedule the function
            rule_response = events_client.put_rule(
                Name='my-scheduled-rule',
                ScheduleExpression=schedule_expression, # e.g., 'rate(1 hour)' or 'cron(0 18 ? * MON-FRI *)'
                State='ENABLED'
            )
            
            # Connect the rule to the Lambda function
            target_response = events_client.put_targets(
                Rule='my-scheduled-rule',
                Targets=[
                    {
                        'Id': '1',
                        'Arn': f'arn:aws:lambda:region:account-id:function:{lambda_function_name}'
                    },
                ]
            )
            print(rule_response, target_response)
        except Exception as e:
            print(e)



    def upload_sql_to_aws_rds(self, db_instance_identifier, db_name, master_username, master_password):
        rds_client = boto3.client('rds')

        try:
            response = rds_client.create_db_instance(
                DBInstanceIdentifier=db_instance_identifier,
                DBName=db_name,
                MasterUsername=master_username,
                MasterUserPassword=master_password,
                DBInstanceClass='db.t2.micro', # Change as per requirement
                Engine='mysql', # For MySQL, change as needed for other engines
                AllocatedStorage=20 # Minimum is 20GB for MySQL
            )
            print(response)
        except Exception as e:
            print(e)



    def configure_webdriver(self):
        options = webdriver.ChromeOptions()
        # Set user agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.4567.789 Safari/537.36")
        # Proxy settings for Bright Data
        if self.config.get('use_bright_data_proxy'):
            proxy_host = "zproxy.lum-superproxy.io"  # Bright Data proxy host
            proxy_port = 22225  # Bright Data proxy port
            proxy_user = self.config['bright_data_username']  # Your Bright Data username
            proxy_pass = self.config['bright_data_password']  # Your Bright Data password
            proxy_string = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
            options.add_argument(f'--proxy-server={proxy_string}')
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
                current_url = self.driver.current_url  # Capture the current URL
                scraped_data = {fieldname: self.driver.find_element(By.XPATH, self.config[f'spider_crawl_target_element_{index}']).text
                                for index, fieldname in enumerate(['Element1', 'Element2', 'Element3'], start=1)}
                scraped_data['URL'] = current_url  # Add the URL to the scraped data
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

        # Add 'URL' to the list of fieldnames
        fieldnames = self.config.get('fieldnames', ['Element1', 'Element2', 'Element3']) + ['URL']

        with open(self.output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
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
                    current_page += 1
                elif self.config.get('infinite_scroll'):
                    self.handle_infinite_scroll()

    def start_scraping(self):
        try:
            self.login()
            self.scrape_elements()
        finally:
            self.driver.quit()