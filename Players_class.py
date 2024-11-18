import pandas as pd
import matplotlib.pyplot as plt
from ScrappingPlayers import TeamScraper
import seaborn as sns
import asyncio
import threading
class Players:
    def __init__(self):
        self.data = pd.DataFrame()
        self.historical_data = pd.read_csv('Scraped22-23.csv')
        self.scraping_done = False
        self.promedio_asistencias = None
        self.promedio_goles = None

        threading.Thread(target=self._run_scraping).start()

    def _run_scraping(self):
        asyncio.run(TeamScraper().scrape_team())
        self.data = TeamScraper().showPd()  # Load player data from CSV
        self._clean_data()
        self.promedio_goles = self.data['Goals'].head(10).mean()
        self.promedio_asistencias = self.data['Assists'].head(10).mean()
        self.scraping_done = True

    def _clean_data(self):
        """Clean and standardize data from both current and historical datasets."""
        for data in [self.data, self.historical_data]:
            data.columns = data.columns.str.strip()
            data["Market Value"] = data["Market Value"].apply(self.parse_market_value)
            data["Market Value"] = pd.to_numeric(data["Market Value"], errors="coerce")
            for col in ["Goals", "Assists", "Age", 'Matches']:
                data[col] = pd.to_numeric(data[col], errors="coerce")

    def parse_market_value(self, value):
        """Converts market value strings to numeric values in euros."""
        if isinstance(value, str):
            if "m" in value:
                return float(value.replace("€", "").replace("m", "")) * 1_000_000
            elif "k" in value:
                return float(value.replace("€", "").replace("k", "")) * 1_000
        return None

    def down_value_for_age(self, fila):
            # Return 1 if player is over 30, else 0
            return 1 if self.data.loc[fila, 'Age'] > 30 else 0

    def down_value_for_goals(self, fila):
            # Return 1 if goals are below average, else 0
            return 1 if self.data.loc[fila, 'Goals'] < self.promedio_goles else 0

    def down_value_for_assists(self, fila):
            # Return 1 if assists are below average, else 0
            return 1 if self.data.loc[fila, 'Assists'] < self.promedio_asistencias else 0

    def evaluate_player(self, fila):
            # Evaluate whether the player's value will go up or down
            list_of_capacity = [
                self.down_value_for_age(fila),
                self.down_value_for_goals(fila),
                self.down_value_for_assists(fila)
            ]
            # Count the number of "down" values
            capacity_for_download = sum(list_of_capacity)
            result = "down" if capacity_for_download > len(list_of_capacity) // 2 else "up"
            
            return result, list_of_capacity
    def analyze_historical_trends(self):
        merged_data = pd.merge(
            self.historical_data,
            self.data,
            on="Player",
            suffixes=("_historical", "_current")
        ).head(5)
        merged_data["Goals Per Match (Current)"] = merged_data["Goals_current"] / merged_data["Matches_current"]
        merged_data["Goals Per Match (Historical)"] = merged_data["Goals_historical"] / merged_data["Matches_historical"]
        merged_data["Assists Per Match (Current)"] = merged_data["Assists_current"] / merged_data["Matches_current"]
        merged_data["Assists Per Match (Historical)"] = merged_data["Assists_historical"] / merged_data["Matches_historical"]
        merged_data["Goals Change (Per Match)"] = (
            merged_data["Goals Per Match (Current)"] - merged_data["Goals Per Match (Historical)"]
        )
        merged_data["Assists Change (Per Match)"] = (
            merged_data["Assists Per Match (Current)"] - merged_data["Assists Per Match (Historical)"]
        )
        top_increases = merged_data.nlargest(5, "Goals Change (Per Match)")
        top_decreases = merged_data.nsmallest(5, "Goals Change (Per Match)")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            data=pd.concat([top_increases, top_decreases]),
            x="Player", y="Goals Change (Per Match)",orient='h', ax=ax
        )
        ax.set_title("Changes in Goals Per Match")
        ax.set_ylabel("Goals Change (Per Match)")
        ax.set_xlabel("Player")
        return fig, merged_data

    def group_analysis_by_position(self):
        position_stats = self.data.groupby("Position").agg({
            "Goals": "mean",
            "Assists": "mean",
            "Market Value": "mean",
        }).head(5)
        fig, ax = plt.subplots()
        melted_data = position_stats.reset_index().melt(id_vars='Position',var_name='Metric',value_name='Value')
        sns.barplot(data=melted_data,x='Position',y='Value',palette='coolwarm',hue='Metric',ax=ax)
        ax.set_xlabel("Position")
        ax.set_ylabel("Average Metrics")
        ax.set_title("Average Metrics by Position")
        return fig, position_stats

    def age_vs_performance(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=self.data,x='Age',y='Goals',ax=ax)
        ax.set_title("Age vs Performance (Goals)")
        ax.set_ylabel("Goals")
        ax.set_xlabel("Age")
        return fig, self.data

    def market_value_by_position(self):
        position_value = self.data.groupby('Position')['Market Value'].mean().reset_index().head(5)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            data=position_value, x='Market Value', y='Position',palette='coolwarm',ax=ax,orient='h'
        )
        ax.set_title("Market Value by Position")
        return fig, position_value

    def player_consistency(self):
        consistency = self.data.groupby('Position')[['Goals', 'Assists']].std().head(5)
        melted_consistency = consistency.reset_index().melt(id_vars="Position", var_name="Metric", value_name="STD")
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.barplot(
            data=melted_consistency,
            x="Position", y="STD", hue="Metric",palette='viridis',  ax=ax
        )
        ax.set_title("Player Consistency in Goals and Assists")
        ax.set_ylabel("Standard Deviation")
        return fig, consistency

    def get_player_data(self):
        results = []
        for fila in range(len(self.data)):
            result, capacities = self.evaluate_player(fila)
            player_info = {
                "Player": self.data.loc[fila, "Player"],
                "Position": self.data.loc[fila, "Position"],
                "Age": self.data.loc[fila, "Age"],
                "Matches": self.data.loc[fila, "Matches"],
                "Goals": self.data.loc[fila, "Goals"],
                "Assists": self.data.loc[fila, "Assists"],
                "Market Value": self.data.loc[fila, "Market Value"],
                "Value Change": result
            }
            results.append(player_info)
        df = pd.DataFrame(results)
        df["Value Change"] = df["Value Change"].map({"up": 1, "down": -1})
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df.head(5), y="Player", x="Value Change", palette=["green" if x > 0 else "red" for x in df["Value Change"]], ax=ax)
        ax.set_title("Player Value Change Analysis")
        return fig, df


# Generate plot

