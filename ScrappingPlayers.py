from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio


class TeamScraper:
    def __init__(self):
        self.players_data = pd.DataFrame(columns=["Player",'Position', "Age", "Matches", "Goals", "Assists", "Market Value"])
        self.url = "https://www.transfermarkt.com/scorer/topscorer/statistik/2024/plus/1/galerie/0?saison_id=2024&selectedOptionKey=6&land_id=0&altersklasse=&ausrichtung=&spielerposition_id=&filter=0&yt0=Show"
       
    async def get_html(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Error accessing page: {response.status}")
                    return None
    
    async def get_players(self):
        html = await self.get_html()

        if not html:
            print("Error: Unable to fetch web page data.")
            return None

        soup = BeautifulSoup(html, 'html.parser')

        # DEBUG: Print a portion of the HTML


        player_table = soup.find('table', {'class': 'items'})
        if not player_table:
            print("Error: Unable to find player table.")
            return None

        player_data_list = []

        # DEBUG: Print the table structure


        # Iterate through rows with class 'odd' or 'even'
        for row in player_table.find_all('tr', {'class': ['odd', 'even']}):
            try:
                # DEBUG: Print the row being processed
                

                # Extract Name
                inline_table = row.find('table', {'class': 'inline-table'})
                name_td = inline_table.find('td', {'class': 'hauptlink'}) if inline_table else None
                name = name_td.text.strip() if name_td else "N/A"
                
                position = inline_table.find_all('tr')[1].text.strip()

                # Extract Age
                age_td = row.find_all('td', {'class': 'zentriert'})
                age = age_td[1].text.strip() if len(age_td) > 1 else "N/A"


                # Extract Matches
                matches = age_td[3].text.strip() if len(age_td) > 2 else "N/A"


                # Extract Goals
                goals = age_td[4].text.strip() if len(age_td) > 3 else "N/A"
 

                # Extract Assists
                assists = age_td[5].text.strip() if len(age_td) > 4 else "N/A"


                # Extract Points
               


                # Extract Market Value
                market_value_td = row.find('td', {'class': 'hauptlink rechts'})
                market_value = market_value_td.text.strip() if market_value_td else "N/A"
                

                # Append extracted data to the list
                player_data_list.append({
                    "Player": name,
                    "Age": age,
                    'Position':position,
                    "Matches": matches,
                    "Goals": goals,
                    "Assists": assists,
                    "Market Value": market_value
                })
            except Exception as e:
                print(f"Skipping row due to missing data: {e}")

        # Convert the data into a DataFrame
        new_player_df = pd.DataFrame(player_data_list)
        self.players_data = pd.concat([self.players_data, new_player_df], ignore_index=True)
        

    async def scrape_team(self):
        await self.get_players()

    def showPd(self) -> pd.DataFrame:
        asyncio.run(self.scrape_team())
        return self.players_data


# Usage Example