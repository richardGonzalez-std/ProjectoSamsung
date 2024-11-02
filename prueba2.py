# team_scraper.py

import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import os
import hashlib
class TeamScraper:
    def __init__(self):
        self.players_data = pd.DataFrame(columns=["Name","Value"])

    async def get_html(self, url):
        headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Error al acceder a la página: {response.status_code}")
                    return None
    async def get_players(self,url):
        html = await self.get_html(url)

        if not html:
            print("Error: No se pudo acceder a la información de la pagina web")
            return None
        
        soup = BeautifulSoup(html,'html.parser')
        player_table = soup.find('table',{'class':'items'})
        player_data_list = []
        for row in player_table.find_all('tr',{'class':['odd','even']}):
            name_td = row.find('td',{'class':'hauptlink'})
            name = name_td.text.strip()
            market_value = row.find('td', {'class':'rechts'}).text.strip()
            player_data_list.append({"Name":name,"Value":market_value})
        new_player_df = pd.DataFrame(player_data_list)
        self.players_data = pd.concat([self.players_data,new_player_df],ignore_index=True)
    
    async def scrape_team(self, url):
        await self.get_players(url)
    
    def showPd(self)->pd.DataFrame:
        return self.players_data


class CSV_ReadIterator:
    def __init__(self) -> None:
      self.data = None
    
    def reader(self,path:str,sep:str)->pd.DataFrame:
        file = pd.read_csv(path,sep=sep,low_memory=False)
        self.data = file[['id','player','age','WinCL','nationality','position','games','league','goals','assists','value','shots_total','shots_on_target','goals_per_shot','xa','passes_completed']].head(10)
        self.data = self.data.sort_values(by='goals',ascending=False)
        return self.data
    def read_csv_directory(self,directory:str)->list:
        dataframes = []
        for filenames in os.listdir(directory):
            if filenames.endswith('.csv'):
                path = os.path.join(directory,filenames)
                df = self.reader(path=path,sep=';')
                dataframes.append(df)
        return dataframes

       
        

async def main():
    url = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop"
    print(CSV_ReadIterator().read_csv_directory('soccer_data/'))
"""    players_data = scraper.players_data
    players_data = players_data.rename(columns={"Name":'player',"Value":"current_value"})
    df = pd.read_csv("soccer_data/transfermarkt_fbref_201920.csv", sep=';')
    df.columns = df.columns.str.strip()
    columns_to_extract = ['player','age','goals','value']
    selected_data = df[df['player'].isin(players_data['player'])][columns_to_extract]
    selected_data.re
    combined_data = selected_data.merge(players_data[['player','current_value']],on='player',how='left')
    combined_data.rename(columns={'value':'old_value'})"""

    

asyncio.run(main())



