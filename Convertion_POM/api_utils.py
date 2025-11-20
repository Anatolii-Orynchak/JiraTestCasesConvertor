import requests
import os
import io
import configparser
from dotenv import load_dotenv
import os


class ApiUtils():
    def __init__(self):
        load_dotenv()
        config = configparser.ConfigParser()
        config.read('/Users/admin/Desktop/Work/Scripts/converter.properties')
        self.jira_token = os.getenv("jira_token")
        self.api_url = config.get('DEFAULT', 'JIRA_API_URL').strip('"')
        self.issue_id = config.get('DEFAULT', 'TICKET_KEY').strip('"')

    def add_attachment_to_test_in_jira(self, attachment_url):
        auth_headers = {
            'Authorization': f'Bearer {self.jira_token}'
        }
        try:
            download_response = requests.get(attachment_url, headers=auth_headers, stream=True)
            download_response.raise_for_status()
            file_content = download_response.content
            print("Attachment downloaded successfully.")
        except Exception as e:
            print(f"Error: {e}")

        filename = os.path.basename(attachment_url)
        if not filename:
            filename = "downloaded_attachment"

        file_object = io.BytesIO(file_content)

        upload_url = f'{self.api_url}issue/{self.issue_id}/attachments'

        upload_headers = {
            'Authorization': f'Bearer {self.jira_token}',
            'X-Atlassian-Token': 'no-check' 
        }

        files = {'file': (filename, file_object, 'application/octet-stream')}
        response = requests.post(upload_url, headers=upload_headers, files=files)

        if response.status_code == 200:
            print(f'Attachment "{filename}" added successfully to {self.issue_id}')
        else:
            print(f'Failed to add attachment. Status Code: {response.status_code}, Response: {response.text}')