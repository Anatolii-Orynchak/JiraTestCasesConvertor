from playwright.sync_api import Page
from test_case_page import TestCasePage

class LoginPage():
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("input#username-field")
        self.password_input = page.locator("input#password-field")
        self.login_button = page.locator("button#login-button")

    def login(self, username, password, downloads_folder_path, issue_key):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return TestCasePage(self.page, downloads_folder_path, issue_key)