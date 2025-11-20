from utils import Utils
from login_page import LoginPage
from playwright.sync_api import Page
import configparser
from dotenv import load_dotenv
import os

class MainFlow():
    def __init__(self, page: Page): 
        load_dotenv()
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.jira_token = os.getenv("jira_token")
        config = configparser.ConfigParser()
        config.read('/Users/admin/Desktop/Work/Scripts/converter.properties')
        self.xray_base_url = config.get('DEFAULT', 'XRAY_BASE_URL').strip('"')
        self.downloads_folder_path = config.get('DEFAULT', 'DOWNLOADS_FOLDER_PATH').strip('"')
        self.downloading_delay = int(config.get('DEFAULT', 'DOWNLOADING_DELAY').strip('"'))
        self.preconditions_file_path = config.get('DEFAULT', 'PRECONDITIONS_FILE_PATH').strip('"')
        self.final_test_type = config.get('DEFAULT', 'FINAL_TEST_TYPE').strip('"')
        self.browser_name = config.get('DEFAULT', 'BROWSER').strip('"')
        self.issue_key = config.get('DEFAULT', 'TICKET_KEY').strip('"')
        self.url = f"{self.xray_base_url}{self.issue_key}"
        self.utils = Utils()
        self.page = page 

    def terminate(self):
        pass

    def run_convertion(self):
        self.page.goto(self.url) 
        self.login_page = LoginPage(self.page)
        self.test_case_page = self.login_page.login(self.username, self.password, self.downloads_folder_path, self.issue_key)
        
        self.summary = self.test_case_page.parse_summary()
        self.preconditions = self.utils.get_preconditions(self.preconditions_file_path)
        
        self.csv_file_path = self.test_case_page.download_csv()

        self.test_steps_text = ""
        self.test_steps_text = self.utils.convert_xray_csv_to_text(self.csv_file_path, self.test_steps_text)
        self.full_description = self.utils.format_full_description(self.summary, self.preconditions, self.test_steps_text)
        
        self.test_case_page.activate_description_editing()
        self.test_case_page.clean_description()
        self.test_case_page.switch_to_description_iframe_fill_and_save(self.full_description)
        self.page.wait_for_load_state('networkidle') 
        self.test_case_page.change_test_type(self.final_test_type)