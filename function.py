import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import csv
import re
import dns.resolver

import pandas as pd

import os
import shutil
from tkinter import messagebox
#page 1
def save_name(app, text_widget):
    text_content = text_widget.get("1.0", "end-1c").strip()
    lines = text_content.split("\n")

    with open("name.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for line in lines:
            if line:
                writer.writerow([line])

    text_widget.delete("1.0", "end")
    app.show_page(1)

#page 2
def is_valid_email(email):
    """Checks if an email has valid MX records."""
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except Exception:
        return False

def get_emails_from_google(query):
    """Scrapes Google search results to find emails related to a query."""
    search_url = f"https://www.google.com/search?q={query}"
    
    print(f"Searching: {query}")
    driver = uc.Chrome()
    driver.get(search_url)
    
    time.sleep(0.2)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    print("Step 1")
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
    
    valid_emails = [email for email in emails if is_valid_email(email)]
    driver.quit()
    
    return valid_emails

def read_email_csv():
    """Reads email.csv and returns the content as a string to display in the text area."""
    try:
        with open("email.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            content = "\n".join([", ".join(row) for row in reader])  # Join rows by commas
        return content
    except FileNotFoundError:
        return "[Error] email.csv not found!"
    
#page 3
unwanted_substrings = [
    ".my", ".um.edu", ".ukm.edu", ".upm.edu", ".utp.edu", ".tarc.edu", ".sunway", ".ucsiuniversity.edu",
    ".au", ".za", ".ir", ".ke", ".ie", ".cn", ".ca", ".kh", ".es", ".ng", ".np", ".nl", ".tw",
    ".us", ".in", ".jp", ".kr", ".sg", ".th", ".vn", ".id", ".ph", ".fr", ".de", ".it", ".ru",
    ".br", ".ar", ".cl", ".mx", ".se", ".no", ".dk", ".fi", ".pl", ".cz", ".hu", ".ro", ".tr",
    ".gr", ".pt", ".lt", ".lv", ".ee", ".sk", ".si", ".bg", ".rs", ".hr", ".ua", ".by",
    ".il", ".ae", ".sa", ".eg", ".ma", ".dz", ".tn", ".pk", ".bd", ".lk", ".mm", ".af",
    ".la", ".mn", ".kz", ".uz", ".tj", ".tm", ".az", ".am", ".ge", ".md", ".kg", ".al", ".ba",
    ".mk", ".me", ".mt", ".cy", ".is", ".li", ".ch", ".be", ".lu", ".at", ".nz", ".fj", ".pg",
    ".ws", ".to", ".vu", ".sb", ".tv", ".ki", ".nr", ".fm", ".pw", ".mh", ".cc", ".tk", ".nu",
    ".gf", ".pf", ".nc", ".gp", ".re", ".yt", ".pm", ".mf", ".bl", ".wf", ".tf", ".io", ".sh",
    ".gs", ".aq", ".bv", ".hm", ".cx", ".nf", ".ms", ".ky", ".vg", ".ai", ".bm", ".tc", ".fk",
    ".gi", ".gg", ".je", ".im", ".as", ".mp", ".gu", ".vi", ".pr", ".um", ".pn", ".uk","xxx"
]

def remove_unwanted_substring(substring):
    """Removes a selected substring from the unwanted list."""
    global unwanted_substrings
    if substring in unwanted_substrings:
        unwanted_substrings.remove(substring)
        print(f"[Bot] Removed '{substring}' from filtering list.")

def clean_data(protected_substrings=[]):
    try:
        file_path = "emails.csv"
        df = pd.read_csv(file_path)

        # Remove duplicates based on the second column
        df[df.columns[1]] = df[df.columns[1]].str.lower()
        df_cleaned = df.drop_duplicates(subset=df.columns[1], keep='first')

        # ✅ Ensure ".uk" is NOT removed if it's in protected_substrings
        filtered_unwanted_substrings = [sub for sub in unwanted_substrings if sub not in protected_substrings]
        pattern = "|".join(map(re.escape, filtered_unwanted_substrings))
        df_cleaned = df_cleaned[~df_cleaned[df_cleaned.columns[1]].str.contains(pattern, na=False)]

        # Remove the word "email" from all rows in column 1
        df_cleaned[df_cleaned.columns[0]] = df_cleaned[df_cleaned.columns[0]].str.replace("email", "", regex=False).str.strip()

        df_cleaned = df_cleaned[~df_cleaned[df_cleaned.columns[1]].str.contains(r'^[a-zA-Z]@', na=False)]

        # Save the cleaned data back to the file
        df_cleaned.to_csv(file_path, index=False)
        print("[Bot] Data cleaned successfully.")
    except FileNotFoundError:
        print("[Bot] The file emails.csv does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
#page 4


def download_email_csv():
    """Downloads the emails.csv file to the user's Downloads folder and shows a pop-up message."""
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    source_file = "emails.csv"
    destination_file = os.path.join(downloads_folder, "emails.csv")

    if os.path.exists(source_file):
        shutil.copy(source_file, destination_file)
        messagebox.showinfo("Download Complete", f"File saved to: {destination_file}")
    else:
        messagebox.showerror("Download Failed", "emails.csv not found!")

