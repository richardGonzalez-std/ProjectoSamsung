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
style = ttk.Style()
style.configure('TLabel',font=("Arial", 16, "bold"), fg="blue")
# Create Notebook
notebook = ttk.Notebook(root)

def load_notebook():
    summary_frame.destroy()
    summary_label.pack_forget()
    create_nootebook_button.pack_forget()
    notebook.pack(expand=True, fill="both")


    add_tab_button.pack(pady=10)
    # Function to add a new tab with a plot for each CSV file in the directory

def add_new_tabs():
        directory = "soccer_data/"
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

        for i, csv_file in enumerate(csv_files):
            # Create a new frame for each tab
            new_tab = ttk.Frame(notebook, width=100, height=100)
            notebook.add(new_tab, text=f"Tab {csv_file}")

            # Generate the Matplotlib figure for the current CSV file
            csv_path = os.path.join(directory, csv_file)
            fig = csv_reader.reader(csv_path, sep=';')

            # Embed Matplotlib figure in the current tab
            canvas = FigureCanvasTkAgg(fig, new_tab)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            canvas.draw()

summary_frame = ttk.Frame(root)
summary_label = ttk.Label(root,text='Este el proyecto de analisis de jugadores en base a su valor futuro',style='TLabel')
summary_frame.pack(pady=5)
summary_label.pack(pady=40)
# Button to add tabs with plots for each CSV file

add_tab_button = ttk.Button(root, text="Add Tabs for All CSVs", command=add_new_tabs)
create_nootebook_button = ttk.Button(root,text='open Charts',command=load_notebook)
create_nootebook_button.pack(pady=10)

root.mainloop()
