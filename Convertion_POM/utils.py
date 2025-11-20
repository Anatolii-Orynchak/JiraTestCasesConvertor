from playwright.sync_api import Page, Locator
import platform
import csv
from api_utils import ApiUtils

class Utils():
    def __init__(self):
        pass

    def get_preconditions(self, file_path):
        with open(file_path, "r", encoding="Latin1") as preconditions_file:
            preconditions = preconditions_file.read()
        return preconditions

    def clear_field(self, element):
        select_all_key = "Meta" if platform.system() == "Darwin" else "Control"
        element.press(select_all_key + "A")
        element.press("Backspace")

    def scroll_to_element(self, page:Page, element):
        page.evaluate("arguments[0].scrollIntoView(true);", element)

    def click_with_js(self, page:Page, element: Locator):
        element_handle = element.element_handle()
        if element_handle:
            page.evaluate("element => element.click();", element_handle)
        else:
            print(f"Warning: Could not get ElementHandle for {element}. Skipping JS click.")

    def clear_with_js(self, page:Page, element):
        page.evaluate("arguments[0].innerHTML = '';", element)

    def format_full_description(self, summary, preconditions, test_steps):
        full_description = f"Headline: {summary}\n{preconditions}\nTest Steps:\n{test_steps}"
        return full_description

    def proceed_step(self, csv_line, line_number, test_text):
        test_text += f"{line_number}. {csv_line[0]}\n"
        if csv_line[1]:
            test_text += f"Data: {csv_line[1]}\n"
        if csv_line[2]:
            test_text += f"Expected result:\n{csv_line[2]}\n"
        if csv_line[3]:
            api_utils = ApiUtils()
            attachment_urls = csv_line[3].split('|') 
            if len(attachment_urls) > 1:
                test_text += f"Attachments:\n"
                for url in attachment_urls: 
                    api_utils.add_attachment_to_test_in_jira(attachment_url=url.strip()) 
                    test_text += f"{url.strip()}\n"
            else:
                single_url = attachment_urls[0].strip()
                test_text += f"Attachment:\n{single_url}\n"
                api_utils.add_attachment_to_test_in_jira(attachment_url=single_url)
        test_text += "\n"
        return test_text

    def convert_xray_csv_to_text(self, file_path, result):
        with open(file_path, "r", encoding="Latin1")  as input_file:
            csv_reader = csv.reader(input_file, dialect='excel')
            next(csv_reader, None) 
            for i, row in enumerate(csv_reader):
                result = self.proceed_step(row, i + 1, result)
        return result