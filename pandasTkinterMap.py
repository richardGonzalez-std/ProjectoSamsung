import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from Players_class import Players  # Import the modified Players class

# Initialize the Players class
players_data = Players("Players.csv")
player_summary = players_data.get_player_data()

# Tkinter setup
root = tk.Tk()
root.title("Player Evaluation")
root.geometry("800x600")

# Create Notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Add a summary tab with player evaluation data
def add_summary_tab():
    summary_tab = ttk.Frame(notebook)
    notebook.add(summary_tab, text="Summary")

    # Create a figure for the summary data
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=player_summary.values, colLabels=player_summary.columns, cellLoc="center", loc="center")
    
    # Embed the figure in the tab
    canvas = FigureCanvasTkAgg(fig, summary_tab)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Add individual evaluation tabs for each metric
def add_evaluation_tabs():
    metrics = ["Age", "Goals", "Assists"]
    for metric in metrics:
        metric_tab = ttk.Frame(notebook)
        notebook.add(metric_tab, text=f"{metric} Evaluation")

        # Generate the evaluation plot for each metric
        fig, ax = plt.subplots()
        if metric == "Age":
            down_values = player_summary["Age"] > 30
            ax.bar(player_summary["Player"], down_values, color="red")
            ax.set_title("Age Evaluation: Red = Decrease in Value")
        elif metric == "Goals":
            down_values = player_summary["Goals"] < players_data.promedio_goles
            ax.bar(player_summary["Player"], down_values, color="blue")
            ax.set_title("Goals Evaluation: Blue = Decrease in Value")
        elif metric == "Assists":
            down_values = player_summary["Assists"] < players_data.promedio_asistencias
            ax.bar(player_summary["Player"], down_values, color="green")
            ax.set_title("Assists Evaluation: Green = Decrease in Value")
        ax.set_xlabel("Player")
        ax.set_ylabel("Value Change Indicator")

        # Embed the figure in the tab
        canvas = FigureCanvasTkAgg(fig, metric_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

# Add the tabs to the notebook
add_summary_tab()
add_evaluation_tabs()

root.mainloop()
