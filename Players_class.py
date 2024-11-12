import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Players:
    def __init__(self, file_path="Players.csv"):
        self.data = pd.read_csv(file_path)  # Load player data from CSV
        # Calculate the averages for goals and assists based on top 5 players
        self.promedio_goles = self.data['Goals'].head(5).mean()
        self.promedio_asistencias = self.data['Assists'].head(5).mean()

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

    def get_player_data(self):
        # Collect player evaluation results
        results = []
        for fila in range(len(self.data)):
            result, capacities = self.evaluate_player(fila)
            player_info = {
                "Player": self.data.loc[fila, "Player_name"],
                "Age": self.data.loc[fila, "Age"],
                "Goals": self.data.loc[fila, "Goals"],
                "Assists": self.data.loc[fila, "Assists"],
                "Value Change": result
            }
            results.append(player_info)

        # Create DataFrame
        df = pd.DataFrame(results).head(5)
        # Convert "up" and "down" to numeric values
        df["Value Change"] = df["Value Change"].map({"up": 1, "down": -1})

        # Generate plot
        fig, ax = plt.subplots()
        df.plot(kind='bar', x='Player', y='Value Change', ax=ax, color='red')
        ax.set_title('Changing Market Value')
        ax.set_xlabel('Player')
        ax.set_ylabel('Value Change')
        return fig
