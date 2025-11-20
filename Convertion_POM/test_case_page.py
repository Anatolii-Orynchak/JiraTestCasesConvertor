from playwright.sync_api import Page, sync_playwright
import os
from utils import Utils

class TestCasePage():
    def __init__(self, page:Page, downloads_folder_path: str, issue_key: str):
        self.page = page   
        self.downloads_folder_path = downloads_folder_path
        self.issue_key = issue_key

        self.summary_h2 = page.locator("div#summary-val>h2")

        # self.activate_description_button = page.locator("div#description-val p")
        self.activate_description_button = page.locator("div#description-val div.user-content-block")
        self.description_iframe = page.frame_locator("iframe")
        self.description_div = self.description_iframe.locator("body#tinymce")
        self.save_description_button = page.locator("button.aui-button.aui-button-primary.submit")
        
        self.burger_button = page.locator("div#raven-test-steps-toolbar button[data-testid='raven-steps-import-export-button']")
        self.burger_menu_export_csv_button = page.locator("a#raven-to-csv-link")
        self.export_button = page.locator("form#raven-export-csv-file input#export-steps-csv-file-submit")
        self.change_type_button = page.locator("div#test-type-field span.edit-icon")
        
        self.include_attachments_checkbox = page.locator("input#withAttachLinks")
        self.show_type_options_button = page.locator("div#test-type-select-single-select>span")
        self.submit_change_type_button = page.locator("div#test-type-field div.save-options button.aui-button.submit[type='submit']")
        self.type_input_field = page.locator("div#test-type-select-single-select input#test-type-select-field")

        self.final_submit_change_type_button = page.locator("input#raven-confirm-dialog-form-submit")
        
    def parse_summary(self):
        return self.summary_h2.inner_text()
    
    def clean_description(self):
        self.description_div.fill("")
    
    def download_csv(self):
        self.burger_button.scroll_into_view_if_needed()
        self.burger_button.click()
        self.burger_menu_export_csv_button.click()
        if not self.include_attachments_checkbox.is_checked():
            self.include_attachments_checkbox.click()

        with self.page.expect_download() as download_info:
            self.export_button.click()
        
        download = download_info.value
        target_file_path = os.path.join(self.downloads_folder_path, f"{self.issue_key}.csv")
        download.save_as(target_file_path)
        print(f"Downloaded CSV to: {target_file_path}")
        return target_file_path

    def change_test_type(self, new_type):
        self.change_type_button.scroll_into_view_if_needed()
        Utils().click_with_js(self.page, self.change_type_button)
        self.type_input_field.wait_for(state="visible") 
        self.type_input_field.click()
        self.type_input_field.fill("")
        self.type_input_field.fill(new_type)
        self.type_input_field.press("Enter")
        self.submit_change_type_button.click()
        self.final_submit_change_type_button.scroll_into_view_if_needed()
        self.final_submit_change_type_button.click()

    def activate_description_editing(self):
        self.activate_description_button.click()

    def switch_to_description_iframe_fill_and_save(self, full_description):
        self.description_div.fill(full_description)
        self.save_description_button.click()

    def add_all_screenshots_as_attachments(self, screenshots_list):
        for screenshot in screenshots_list:
            self.page.locator(f"img[src='{screenshot}']").click()