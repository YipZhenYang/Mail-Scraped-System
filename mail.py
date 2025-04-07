import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import csv
import re
import dns.resolver

def is_valid_email(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except Exception:
        return False

def get_emails_from_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    
    driver = uc.Chrome()
    driver.get(search_url)
    
    time.sleep(0.2)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    print("Stemp 1")
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
    
    valid_emails = [email for email in emails if is_valid_email(email)]
    driver.quit()
    
    return valid_emails

input_file = "name.csv"
output_file = "emails.csv"

with open(input_file, "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  

    results = []

    keywords = ["ltd", "limited", "studio", "practice", "dental", "partner", "centre", "clinic"]

    for row in reader:
        name = row[0].strip()
        name_lower = name.lower()

        if any(keyword in name_lower for keyword in keywords):
            search_query = f"{name} email"
            print("[Bot] Searching For Company Mail")
        else:
            search_query = f"UK dentist {name} email"
            print("[Bot] Searching For Dentist Mail")

        emails = get_emails_from_google(search_query)

        for email in emails:
            results.append([name, email])

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Email"])
    writer.writerows(results)
print(f"Emails saved to {output_file}")
