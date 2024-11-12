import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from prueba2 import CSV_ReadIterator

# Instantiate CSV_ReadIterator
csv_reader = CSV_ReadIterator()

# Tkinter setup
root = tk.Tk()
root.title("Data Visualization")
root.geometry("800x600")

# Create Notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Function to add new tab with a plot
def add_new_tab():
    new_tab = ttk.Frame(notebook)
    directory = "soccer_data/"
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    if csv_files:
        print(csv_files)
        for i in range(len(csv_files)):
            notebook.add(new_tab,text=f" Tab {csv_files[i]}")

    # Get the next CSV file in the directory (for demonstration purposes)
    
        # Use the first CSV file in the directory
        csv_path = os.path.join(directory, csv_files[0])
        fig = csv_reader.reader(csv_path, sep=';')  # Generate the Matplotlib figure

        # Embed Matplotlib figure in Tkinter tab
        canvas = FigureCanvasTkAgg(fig, new_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

# Button to add a new tab with a plot
add_tab_button = ttk.Button(root, text="Add New Tab", command=add_new_tab)
add_tab_button.pack(pady=10)

root.mainloop()
