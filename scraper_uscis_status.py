import os
import requests
from datetime import datetime
import csv

BASE_URL = 'https://egov.uscis.gov/csol-api/case-statuses/'

def get_case_data(receipt_num: str, name: str):
    response = requests.get(BASE_URL + receipt_num.upper())
    if response.status_code == 200:
        data = response.json()
        if data.get("CaseStatusResponse", {}).get("isValid"):
            details_eng = data["CaseStatusResponse"]["detailsEng"]
            
            case_status_eng = details_eng["actionCodeDesc"]
            case_title_eng = details_eng["actionCodeText"]
            
            # Return the values for the CSV
            return (name, receipt_num, case_title_eng, case_status_eng)
        else:
            return (name, receipt_num, "Invalid Receipt", "")
    else:
        return (name, receipt_num, "Failed to fetch data", "")

def file_data(directory="."):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(filename, 'r') as f:
                name = filename.replace('.txt', '')
                case_numbers = [line.strip() for line in f.readlines()]
                for case_number in case_numbers:
                    data.append((name, case_number))
    return data

if __name__ == "__main__":
    s_date = datetime.today().strftime('%Y-%m-%d')
    data = file_data()

    results = [get_case_data(case_number, name) for name, case_number in data]

    with open(f'case_status_{s_date}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Case Number', 'Case Status', 'Case Details'])
        writer.writerows(results)
