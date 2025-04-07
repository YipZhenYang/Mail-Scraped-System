import tkinter as tk
from tkinter import Text
from tkinter import ttk

import subprocess


#page 1
from function import save_name
#page 2
from function import read_email_csv
#page 3
from function import unwanted_substrings
from function import clean_data
#page 4
from function import download_email_csv

class MailScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MailScraper3000")
        self.root.geometry("700x700")
        self.root.resizable(False, False)  #Disable window resizing
        self.current_page = 0
        self.pages = []

        self.protected_substrings = [] 

        self.create_page1()
        self.create_page2()
        self.create_page3()
        self.create_page4()

        self.show_page(0)
#---Page 1---
    def create_page1(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        
        self.text_area = Text(frame, height=30, width=78)  
        self.text_area.pack(pady=20)
        
        btn_next = tk.Button(
                    frame, text="Next", font=("Arial", 12), bg="blue", fg="white",
                    command=lambda: save_name(self, self.text_area)
                )        
        btn_next.place(x=620, y=650)
        
        self.pages.append(frame)
    
#---Page 2---
    def refresh_page2_TextArea(self):
        self.text_area2.config(state=tk.NORMAL)
        self.text_area2.delete("1.0", tk.END)
        try:
            with open("name.csv", "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area2.insert("1.0", content)
        except FileNotFoundError:
            self.text_area2.insert("1.0", "File not found: name.csv")
        self.text_area2.config(state=tk.DISABLED)


    def create_page2(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.text_area2 = Text(frame, height=30, width=78)
        self.text_area2.pack(pady=20)

        try:
            with open("name.csv", "r", encoding="utf-8") as file:
                content= file.read()
                self.text_area2.insert("1.0", content) 
        except FileNotFoundError:
            content = ""
            self.text_area2.insert("1.0", "File not found: name.csv")
        self.text_area2.config(state=tk.DISABLED)

        
        num_lines = content.count("\n")
        estimated_runtime = num_lines * 8  # in seconds
        runtime_text = f"Estimated Runtime: {estimated_runtime} seconds"


        try:
            with open("country.txt", "r", encoding="utf-8") as file:
                country_options = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            country_options = ["File not found"] 

        self.combo_box = ttk.Combobox(frame, values=country_options, state="readonly")
        self.combo_box.place(x=40, y=530)

        self.runtime_label = tk.Label(frame, text=runtime_text, font=("Arial", 11), fg="gray")
        self.runtime_label.place(x=40, y=500)


        btn_back = tk.Button(frame, text="Back", font=("Arial", 12), command=lambda: self.show_page(0))
        btn_back.place(x=560, y=650)

        btn_next = tk.Button(
            frame, text="Next", font=("Arial", 12), bg="blue", fg="white", 
            command=lambda: self.run_main_with_country()
        )
        btn_next.place(x=620, y=650)

        self.pages.append(frame)

    def run_main_with_country(self):
        selected_country = self.combo_box.get()  # Get selected country
        if not selected_country:
            print("[Error] No country selected!")
            return

        # Mapping of country to unwanted_substring values
        country_to_substring = {
            "UK": ".uk",
            "US": ".us",
            "Indonesia": ".id",
        }

        if selected_country in country_to_substring:
            self.protected_substrings.append(country_to_substring[selected_country])  # Add to protected list

        subprocess.run(["python", "main.py", selected_country])  # Run main script
        self.show_page(2)

#---Page 3---
    
    def refresh_page3(self):
        self.text_area3.config(state=tk.NORMAL)
        self.text_area3.delete("1.0", tk.END)
        try:
            with open("emails.csv", "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area3.insert("1.0", content)
        except FileNotFoundError:
            self.text_area3.insert("1.0", "File not found: email.csv")
        
        self.filtered_unwanted_substrings = [sub for sub in unwanted_substrings if sub not in self.protected_substrings]

        self.text_area3.config(state=tk.DISABLED)


    def create_page3(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.text_area3 = Text(frame, height=30, width=78)
        self.text_area3.pack(pady=20)

        self.filtered_unwanted_substrings = [sub for sub in unwanted_substrings if sub not in self.protected_substrings]
        btn_back = tk.Button(frame, text="Back", font=("Arial", 12), command=lambda: self.show_page(1))
        btn_back.place(x=560, y=650)

        btn_next = tk.Button(frame, text="Next", font=("Arial", 12), bg="blue", fg="white",
                            command=self.clean_and_proceed)
        btn_next.place(x=620, y=650)

        self.pages.append(frame)

    def remove_selected_item(self):
        """Removes the selected item from the listbox and unwanted_substrings."""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_value = self.listbox.get(selected_index)
            unwanted_substrings.remove(selected_value)
            self.listbox.delete(selected_index)

    def clean_and_proceed(self):
        """Cleans data and moves to the next page, ensuring protected substrings are respected."""
        clean_data(self.protected_substrings)
        self.show_page(3)

            
#---Page 4---

    def refresh_page4(self):
        self.text_area4.config(state=tk.NORMAL)
        self.text_area4.delete("1.0", tk.END)
        try:
            with open("emails.csv", "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area4.insert("1.0", content)
        except FileNotFoundError:
            self.text_area4.insert("1.0", "File not found: email.csv")
        
        self.filtered_unwanted_substrings = [sub for sub in unwanted_substrings if sub not in self.protected_substrings]

        self.text_area4.config(state=tk.DISABLED)

    def create_page4(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.text_area4 = Text(frame, height=30, width=78)
        self.text_area4.pack(pady=20)

        btn_download = tk.Button(frame, text="Download", font=("Arial", 12), bg="green", fg="white", 
                                command=download_email_csv)
        btn_download.place(x=40, y=650)

        btn_back = tk.Button(frame, text="Back", font=("Arial", 12), command=lambda: self.show_page(2))
        btn_back.place(x=560, y=650)

        btn_finish = tk.Button(frame, text="Finish", font=("Arial", 12), bg="blue", fg="white", command=self.root.quit)
        btn_finish.place(x=630, y=650)

        self.pages.append(frame)

    def show_page(self, page_index):
        for frame in self.pages:
            frame.pack_forget()
        self.pages[page_index].pack(fill="both", expand=True)
        self.current_page = page_index
        if page_index == 1:
            self.refresh_page2_TextArea()
        elif page_index == 2:
            self.refresh_page3()
        elif page_index == 3:
            self.refresh_page4()

if __name__ == "__main__":
    root = tk.Tk()
    app = MailScraperApp(root)
    root.mainloop()
