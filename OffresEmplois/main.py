from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd



page = requests.get('https://www.emploi-public.ma/FR/index.asp')
joobs_data = []

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    emplois = soup.find_all("tr")
    def get_joob_info(href):
        page = requests.get(href)
        soup = BeautifulSoup(page.content,'lxml')
        joob_infos = soup.find_all("tr")
        joob_data = {}
        for i in range(len(joob_infos)):
            key = joob_infos[i].find("th").text.strip()
            value = joob_infos[i].find("td").text.strip()
            joob_data[key] = value
        joobs_data.append(joob_data)

    for i in range(len(emplois)):
        href = emplois[i].find("a")
        if href:
            href_value = href.get("href")
            href = f"https://www.emploi-public.ma/FR/{href_value}"
            get_joob_info(href)


    if(len(joobs_data) > 0):
        df = pd.DataFrame(joobs_data)
        todaydate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"d:/WEBSCARPING/OffresEmplois/joob_infos{todaydate}.xlsx"
        df.to_excel(file_path, index=False)
        print("File created successfully")

if __name__ == "__main__":
    main(page)

