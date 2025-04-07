import csv
import sys
from function import get_emails_from_google

input_file = "name.csv"
output_file = "emails.csv"
selected_country = sys.argv[1] if len(sys.argv) > 1 else ""


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
            search_query = f"{selected_country} dentist {name} email"
            print(f"[Bot] Searching For Dentist Mail in {selected_country}")

        emails = get_emails_from_google(search_query)

        for email in emails:
            results.append([name, email])

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Email"])
    writer.writerows(results)

print(f"Emails saved to {output_file}")
