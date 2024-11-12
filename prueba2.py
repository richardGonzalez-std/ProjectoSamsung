# team_scraper.py

import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
    
    def reader(self, path: str, sep: str):
        # Read CSV and select relevant columns
        file = pd.read_csv(path, sep=sep, low_memory=False)
        # Sort data by goals in descending order
        self.data = file.sort_values(by=['goals','position'], ascending=[False,False]).head(10)
        # Return a bar chart plot for the top 10 players by goals
        fig, ax = plt.subplots()
        self.data.plot(kind='bar',y='goals',y='players',ax=ax,color='skyblue')
        ax.set_title("Top 10 Player by Goals")
        ax.set_xlabel('Goals')
        ax.set_ylabel('Players')
        return fig
    
    def analyze_statistics(self)->pd.DataFrame:
            # Asegurarse de que los datos están cargados
            if self.data is None:
                raise ValueError("No data loaded. Please load a CSV file first.")
            
            # 1. Calcular correlaciones de estadísticas con el valor de mercado
            correlation_matrix = self.data[['age', 'games', 'goals', 'assists', 'value']].corr()

            # 2. Distribución de valores de mercado por posición
            position_market_value = self.data.groupby('position')['value'].mean()
            print("\nValor de mercado promedio por posición:")
            print(position_market_value)
            
            # 3. Análisis de valores por posición
            print("\nAnálisis comparativo de estadísticas por posición:")
            groupedMean = self.data.groupby('position')[['goals', 'assists', 'games', 'value']].mean()
            return pd.concat(data for data in [correlation_matrix,position_market_value,groupedMean])



# Display the visualization using Panel
#pn.serve(combined_visualization)  # For a standalone app

       
        

""""async def main():
    url = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop"
    csvReader = CSV_ReadIterator()
    combined_visualization = csvReader.read_csv_directory('soccer_data/')
    pn.serve(combined_visualization,show=True,blocking=True)
    input("Press enter to exit.....\n")"""
"""    players_data = scraper.players_data
    players_data = players_data.rename(columns={"Name":'player',"Value":"current_value"})
    df = pd.read_csv("soccer_data/transfermarkt_fbref_201920.csv", sep=';')
    df.columns = df.columns.str.strip()
    columns_to_extract = ['player','age','goals','value']
    selected_data = df[df['player'].isin(players_data['player'])][columns_to_extract]
    selected_data.re
    combined_data = selected_data.merge(players_data[['player','current_value']],on='player',how='left')
    combined_data.rename(columns={'value':'old_value'})"""

    





