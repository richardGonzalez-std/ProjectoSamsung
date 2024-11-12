import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
from prueba2 import CSV_ReadIterator
from Players_class import Players

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
    new_tab = ttk.Frame(notebook,width=300,height=300)
    notebook.add(new_tab,text=f'Valores de Mercado')
    fig,df = Players().get_player_data()
    # Embed Matplotlib figure in the current tab
    canvas = FigureCanvasTkAgg(fig, new_tab)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    add_tab_button.pack(pady=10)
    # Function to add a new tab with a plot for each CSV file in the directory

def add_new_tabs():
        #playersList = players()
        new_tab = ttk.Frame(notebook,width=300,height=600)
        notebook.add(new_tab,text='Tabla jugadores')
        figure,playersDf = Players().get_player_data()
    
        playersDf.rename(columns={"Player":'Nombre de Jugador','Age':'Edad','Goals':'Goles'},inplace=True)
        fig,ax= plt.subplots()
        ax.axis('off')
        table = ax.table(cellText=playersDf.values,colLabels=playersDf.columns,cellLoc='center',loc='center')
        canvas = FigureCanvasTkAgg(fig,new_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)
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
