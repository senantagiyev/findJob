import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from bs4 import BeautifulSoup
import threading

class JobScraperApp:
    def __init__(self, master):
        self.master = master
        master.title("İş Axtarış Sistemi")
        master.geometry("600x400")

        tk.Label(master, text="Açar söz:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.keyword_entry = tk.Entry(master, width=40)
        self.keyword_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.search_button = tk.Button(master, text="Axtar", command=self.start_search)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.hellojob_tab = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.busyaz_tab = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.smartjob_tab = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)

        self.notebook.add(self.hellojob_tab, text="HelloJob.az")
        self.notebook.add(self.busyaz_tab, text="Busy.az")
        self.notebook.add(self.smartjob_tab, text="SmartJob.az")

        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(1, weight=1)

    def start_search(self):
        keyword = self.keyword_entry.get()
        if not keyword:
            return

        self.hellojob_tab.delete('1.0', tk.END)
        self.busyaz_tab.delete('1.0', tk.END)
        self.smartjob_tab.delete('1.0', tk.END)

        threading.Thread(target=self.search_hellojob, args=(keyword,)).start()
        threading.Thread(target=self.search_busyaz, args=(keyword,)).start()
        threading.Thread(target=self.search_smartjob, args=(keyword,)).start()

    def search_hellojob(self, keyword):
        url = f"https://www.hellojob.az/search?query={keyword}&search_type=keyword&searched="
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all('a', class_='vacancies__item')
            
            if not jobs:
                self.hellojob_tab.insert(tk.END, "Heç bir nəticə tapılmadı.\n")
                return
                
            for job in jobs:
                title = job.find('h3')
                company = job.find('p', class_='vacancy_item_company')
                salary = job.find('span', class_='vacancies__price')
                date = job.find('span', class_='vacancy_item_time')
                
                result = ""
                if title:
                    result += f"Vəzifə: {title.text.strip()}\n"
                if company:
                    result += f"Şirkət: {company.text.strip()}\n"
                if salary:
                    result += f"Maaş: {salary.text.strip()}\n"
                if date:
                    result += f"Tarix: {date.text.strip()}\n"
                result += "-" * 50 + "\n"
                
                self.hellojob_tab.insert(tk.END, result)

        except Exception as e:
            self.hellojob_tab.insert(tk.END, f"HelloJob.az xətası: {e}\n")

    def search_busyaz(self, keyword):
        url = f"https://busy.az/skills/{keyword}"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all('div', class_='job-listing')
            
            if not jobs:
                self.busyaz_tab.insert(tk.END, "Heç bir nəticə tapılmadı.\n")
                return
                
            for job in jobs:
                title = job.find('h3', class_='job-listing-title')
                company = job.find('i', class_='icon-material-outline-business')
                if company:
                    company = company.find_next('a')
                date = job.find('i', class_='icon-material-outline-access-time')
                if date:
                    date = date.parent
                
                result = ""
                if title:
                    result += f"Vəzifə: {title.text.strip()}\n"
                if company:
                    result += f"Şirkət: {company.text.strip()}\n"
                if date:
                    result += f"Tarix: {date.text.strip()}\n"
                result += "-" * 50 + "\n"
                
                self.busyaz_tab.insert(tk.END, result)

        except Exception as e:
            self.busyaz_tab.insert(tk.END, f"Busy.az xətası: {e}\n")

    def search_smartjob(self, keyword):
        url = f"https://smartjob.az/vacancies?search={keyword}"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all('div', class_='brows-job-list')
            
            if not jobs:
                self.smartjob_tab.insert(tk.END, "Heç bir nəticə tapılmadı.\n")
                return
                
            for job in jobs:
                title = job.find('h3')
                company = job.find('span', class_='company-title')
                salary = job.find('div', class_='salary-val')
                date = job.find('div', class_='created-date')
                
                result = ""
                if title:
                    result += f"Vəzifə: {title.text.strip()}\n"
                if company:
                    result += f"Şirkət: {company.text.strip()}\n"
                if salary:
                    result += f"Maaş: {salary.text.strip()}\n"
                if date:
                    result += f"Tarix: {date.text.strip()}\n"
                result += "-" * 50 + "\n"
                
                self.smartjob_tab.insert(tk.END, result)

        except Exception as e:
            self.smartjob_tab.insert(tk.END, f"SmartJob.az xətası: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = JobScraperApp(root)
    root.mainloop()