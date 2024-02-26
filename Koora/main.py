import requests
from bs4 import BeautifulSoup
import pandas as pd


date = input("Please enter a date in the format : DD/MM/YYYY \n")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")

def main(page):
    data = []
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    champions = soup.find_all("div",{'class':'matchCard'})
    def get_matches_info(champions):
        champion_name = champions.contents[1].find("h2").text.strip()
        all_matches = champions.contents[3].find_all("div",{'class':'item future liItem'})
        for i in range (len(all_matches)):
            teamA = all_matches[i].find("div",{'class':"teamA"}).text.strip()
            teamB = all_matches[i].find("div",{'class':"teamB"}).text.strip()
            match_result = all_matches[i].find("div",{'class':'MResult'}).find_all("span",{'class':'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            time = all_matches[i].find("div",{'class':'MResult'}).find("span",{'class':'time'}).text.strip()
            data.append({
                "البطولة":champion_name,
                "الفريق الاول":teamA,
                "الفريق الثاني":teamB,
                "النتيجة":score,
                "الوقت":time
            })
    for i in range(len(champions)):
        get_matches_info(champions[i])

    file_path = f"d:/WEBSCARPING/Koora/matches_details_{date.replace("/","_")}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"File saved in {file_path}")
    
main(page)