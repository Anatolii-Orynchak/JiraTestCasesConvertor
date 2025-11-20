from main_flow import MainFlow
from playwright.sync_api import sync_playwright
import configparser

def main():
    config = configparser.ConfigParser()
    config.read('/Users/admin/Desktop/Work/Scripts/converter.properties') 
    browser_name = config.get('DEFAULT', 'BROWSER').strip('"') if config.has_option('DEFAULT', 'BROWSER') else "chromium"

    with sync_playwright() as p:
        browser = None
        if browser_name.lower() == 'chrome':
            browser = p.chromium.launch(headless=False)
        elif browser_name.lower() == 'firefox':
            browser = p.firefox.launch(headless=False)
        elif browser_name.lower() == 'safari':
            browser = p.webkit.launch(headless=False)
        else:
            print(f"Unsupported browser '{browser_name}' specified. Defaulting to Chromium.")
            browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        main_flow = MainFlow(page) 
        main_flow.run_convertion()
        print("Conversion completed successfully.")

if __name__ == "__main__":
    main()