# Jira Test Cases Converter

This Python script converts Jira Test Cases from Manual to Generic type using the Jira REST API and browser automation.

## Repository

[https://github.com/Anatolii-Orynchak/JiraTestCasesConvertor/tree/single_issue_converter](https://github.com/Anatolii-Orynchak/JiraTestCasesConvertor/tree/single_issue_converter)

---

## Prerequisites

- Python 3.x installed on your system.
- A Jira account with API access and appropriate permissions.
- Chrome, Safari or Firefox installed.

---

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Anatolii-Orynchak/JiraTestCasesConvertor.git
   cd JiraTestCasesConvertor
   git checkout single_issue_converter

2. **Create and activate a Python virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   
3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   
4. **Configure the `converter.properties` file:**

   - `XRAY_BASE_URL`: Base URL for Jira test cases (e.g., `"https://jira.talos.cisco.com/browse/"`).
   - `BROWSER`: Browser to use for automation (e.g., `"Safari"`).
   - `DOWNLOADS_FOLDER_PATH`: Path where downloads will be saved.
   - `DOWNLOADING_DELAY`: Delay in seconds to wait for downloads.
   - `PRECONDITIONS_FILE_PATH`: Path to the preconditions text file.
   - `FINAL_TEST_TYPE`: The target test case type after conversion (e.g., `"Generic"`).
   - `JIRA_API_URL`: Jira API base URL.
   - `TICKET_KEY`: Jira ticket key to process.

5. **Set up the `.env` file with your credentials:**

   - `username`: Your Jira username.
   - `password`: Your Jira password.
   - `jira_token`: Your Jira API token.

6. **Run the script:**

   ```bash
   cd Convertion_POM
   python -m main.py
