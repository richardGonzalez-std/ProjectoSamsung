import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random

# Create the main Tkinter window
root = tk.Tk()
root.title("Dynamic Tabs with Plots")
root.geometry("800x600")

# Create the Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Sample data to use for random plots
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [23, 45, 56, 78]
}
df = pd.DataFrame(data)

# Counter for tab names
tab_count = 1

# Function to add a new tab with a plot
def add_new_tab():
    global tab_count

    # Create a new frame to be used as a tab
    new_tab = ttk.Frame(notebook)
    notebook.add(new_tab, text=f"Tab {tab_count}")
    
    # Generate a new figure for a random plot
    fig, ax = plt.subplots()
    
    # Create a new random plot for variety (e.g., bar plot with random values)
    random_values = [random.randint(10, 100) for _ in df['Category']]
    ax.bar(df['Category'], random_values, color='skyblue')
    ax.set_title(f"Random Plot {tab_count}")
    ax.set_xlabel("Category")
    ax.set_ylabel("Values")

    # Embed the plot in the new tab
    canvas = FigureCanvasTkAgg(fig, new_tab)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    # Update tab count
    tab_count += 1

# Button to add a new tab
add_tab_button = ttk.Button(root, text="Add New Tab", command=add_new_tab)
add_tab_button.pack(pady=10)

root.mainloop()
