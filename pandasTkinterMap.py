import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random

# Create the main Tkinter window
root = tk.Tk()
root.title("Chrome-Style Tabs with Close Button")
root.geometry("800x600")

# Create the Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Sample data for plotting
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [23, 45, 56, 78]
}
df = pd.DataFrame(data)

# Tab counter for unique tab names
tab_count = 1

# Function to add a new tab with a plot and a close button
def add_new_tab():
    global tab_count
    
    # Create a frame for the tab content
    new_tab = ttk.Frame(notebook)
    
    # Create a container frame for the title and close button
    tab_title_frame = ttk.Frame(notebook)
    
    # Create label for the tab name
    tab_label = tk.Label(tab_title_frame, text=f"Tab {tab_count}", padx=5)
    tab_label.pack(side=tk.LEFT)

    # Create close button for the tab
    close_button = tk.Button(tab_title_frame, text="X", command=lambda: close_tab(new_tab, tab_title_frame), padx=5)
    close_button.pack(side=tk.RIGHT)
    
    # Add the tab with a custom frame (tab_title_frame)
    notebook.add(new_tab, text=f"Tab {tab_count}")
    notebook.tab(new_tab, compound=tk.LEFT, text="", window=tab_title_frame)

    # Generate a Matplotlib plot
    fig, ax = plt.subplots()
    random_values = [random.randint(10, 100) for _ in df['Category']]
    ax.bar(df['Category'], random_values, color='skyblue')
    ax.set_title(f"Random Plot {tab_count}")
    ax.set_xlabel("Category")
    ax.set_ylabel("Values")

    # Embed the plot in the new tab
    canvas = FigureCanvasTkAgg(fig, new_tab)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    # Increment the tab count
    tab_count += 1

# Function to close the tab
def close_tab(tab_frame, title_frame):
    # Remove both the tab content and the title frame
    notebook.forget(tab_frame)
    title_frame.destroy()

# Button to add a new tab
add_tab_button = ttk.Button(root, text="Add New Tab", command=add_new_tab)
add_tab_button.pack(pady=10)

root.mainloop()
