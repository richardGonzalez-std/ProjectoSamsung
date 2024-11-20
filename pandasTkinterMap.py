import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Players_class import Players

class PlayerApp:
    def __init__(self, root):
        '''
        Esta es la función de inicialización de la clase PlayerApp. Configura la ventana principal, define el tamaño de pantalla,
        habilita el modo de pantalla completa, aplica el estilo visual, y crea el marco de presentación inicial (resume_frame).
        '''
        self.root = root
        self.root.title("Analisis de Jugadores")

        # Obtener el tamaño de la pantalla


        # 
        root.geometry('1200x800')
        root.bind('<F12>',self.open_in_fullscreen)
        root.bind('<Escape>',self.escape_fullscreen)
       
        self.style = ttk.Style("darkly")  # Applying a modern dark theme.
        self.style.configure("TFrame", background="black")
        
        self.create_resume_frame()

    def center_window(self,window):
        """
        Basado en https://stackoverflow.com/a/10018670.
        """
        window.update_idletasks()
        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2*frm_width
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth()//2 - win_width//2
        y = window.winfo_screenheight()//2 - win_height//2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()

    def open_in_fullscreen(self,event):
        self.root.attributes('-fullscreen',True)
    def create_resume_frame(self):
        """
        Crea el marco inicial de presentación que incluye un encabezado, una breve descripción del programa,
        una sección de agradecimientos con los nombres de los creadores, y botones para interactuar con la aplicación,
        como abrir el panel de análisis o mostrar información adicional.

        """

        self.resume_frame = ttk.Frame(self.root,padding=0)
        self.resume_frame.pack(fill=ttk.BOTH,expand=True)

        header_label = ttk.Label(
            self.resume_frame,
            text='Bienvenido al Analisis de datos de los jugadores',
            bootstyle = 'danger',
            background='black',
            font=('Helvetica',36,'bold'),
            padding=0
        )
        header_label.pack(pady=5,padx=10)

        description_label = ttk.Label(
            self.resume_frame,
            text = ('\tEsta aplicación provee un analisís profundo de las estadísticas de los jugadores. \n'
            "Explora metricas,tendencias, y datos acerca de los jugadores de futbol a traves de estas gráficas\n"
            ),
            bootstyle='danger',
            background='black',
            font=('Helvetica',18)
        )
        description_label.pack(pady=20)
        creator_label = ttk.Label(
            self.resume_frame,
            text=('Participantes / Creadores\n'
                  '\tRichard\n'
                  '\tDanny\n'
                  '\tVictor\n'
                  '\tLuis\n'),
            background='black',
            bootstyle='danger',
            font=('Helvetica',24,'bold')
        )
        creator_label.pack(pady=50,after=description_label)
        button_frame = ttk.Frame(self.resume_frame)
        button_frame.pack(pady=20)

        open_notebook_button = ttk.Button(
            button_frame,
            text="Open Analysis Dashboard",
            bootstyle="success",
            command=self.load_notebook
        )
        open_notebook_button.pack(side=LEFT, padx=10)

        more_info_button = ttk.Button(
            button_frame,
            text="More Information",
            bootstyle="info",
            command=self.show_more_info
        )
        more_info_button.pack(side=LEFT, padx=40)

        # Footer section
        footer_label = ttk.Label(
            self.resume_frame,
            text="© 2024 Player Data Analysis App",
            bootstyle="secondary",
            font=("Helvetica", 12)
        )
        footer_label.pack(side=BOTTOM, pady=10)

    def show_more_info(self):
        """
        Muestra una ventana emergente con información adicional sobre el propósito y las características del programa.
        Incluye un botón para cerrar esta ventana.


        """
        info_window = ttk.Toplevel(self.root)
        self.center_window(info_window)
        info_window.title("Mas info")
        info_window.geometry("1000x400")


        info_label = ttk.Label(
            info_window,
            text=(
                "El proyecto en cuestión tiene como premisa establecer a través de modelos lógico/matemáticos\n"
                "un medio de análisis, en este caso, para un mercado en particular\n el mercado en cuestión es el deportivo."
                "Se enfoco directamente al mercado\n del fútbol masculino, tomando en cuenta un análisis previo de los jugadores\n y sus valores de mercado actuales.\n"
                "Se plantea conseguir un medio por el cual, determinar si el desempeño de un jugador puede \ninfluir dentro de su valoración futura.\n"

            ),
            bootstyle="info",
            font=("Helvetica", 16)
        )
        info_label.pack(pady=20, padx=20)

        close_button = ttk.Button(
            info_window,
            text="Close",
            bootstyle="danger",
            command=info_window.destroy
        )
        close_button.pack(pady=10)

    '''def show_greetings(self):
        """
        Display a greeting message in a pop-up window.
        """
        greeting_window = ttk.Toplevel(self.root)
        greeting_window.title("Agradecimientos")
        greeting_window.geometry("800x200")

        greeting_label = ttk.Label(
            greeting_window,
            text="Hello! Thank you for using the Player Data Analysis App!",
            bootstyle="success",
            font=("Helvetica", 16)
        )'''
        

    def load_notebook(self):
        '''
        Elimina el marco inicial (resume_frame) y carga el cuaderno de pestañas (notebook). 
        Inicia la barra de progreso para indicar que se están cargando los datos.
        Llama al método check_data_ready para verificar si los datos están listos.
        '''
        self.resume_frame.destroy()
        self.notebook = ttk.Notebook(self.root, bootstyle="dark")
        self.notebook.pack(fill=BOTH, expand=True)
        self.style.configure('TLabel',font=('Helvetica',32,'bold'))
        self.status_progressBar = ttk.Progressbar(bootstyle="info-striped")
        self.text_progressBar = ttk.Label(master=self.notebook,text='Loading Data......',bootstyle='info',style='TLabel').place(x=self.root.winfo_width()-(self.root.winfo_width()-450),y=(self.root.winfo_height()//2)-100)
        self.status_progressBar.place(x=self.root.winfo_width()-(self.root.winfo_width()-100),y=(self.root.winfo_height()//2),width=self.root.winfo_width()-200)
       

        self.players = Players()  # Initialize Players class
        self.check_data_ready()  # Start checking for data readiness

    def apply_chart_style(self,ax):
        """
        Aplica un estilo personalizado a las gráficas de Matplotlib,
        como colores de fondo, etiquetas, y bordes de los ejes. 
        Esto asegura que las gráficas sean consistentes con el tema oscuro de la aplicación.
        """
        ax.set_facecolor("none")
        ax.title.set_color("black")
        ax.xaxis.label.set_color("black")
        ax.yaxis.label.set_color("black")
        ax.tick_params(axis="both", colors="black")
        for spine in ax.spines.values():
            spine.set_edgecolor("black")
            
    def escape_fullscreen(self,event):
        self.root.attributes('-fullscreen',False)

    def check_data_ready(self):
        """
        Comprueba periódicamente si la clase Players ha terminado de procesar los datos. Si no están listos, mantiene activa la barra de progreso. 
        Si los datos están listos, destruye la barra de progreso y llama al método add_tabs para mostrar las pestañas con las gráficas.
        """
        if not self.players.scraping_done:
            self.status_progressBar.start()
            self.root.after(10100, self.check_data_ready)
        else:
            self.status_progressBar.destroy()
            self.add_tabs()  # Retry after 500ms

    def add_tabs(self):
        """
        Crea una pestaña para cada análisis o visualización de datos. 
        Llama a add_tab para añadir cada pestaña con su respectiva figura.
        """
        self.add_tab("Player Value Change", self.players.get_player_data)
        self.add_tab("Historical Trends", self.players.analyze_historical_trends)
        self.add_tab("Metrics by Position", self.players.group_analysis_by_position)
        self.add_tab("Age vs Performance", self.players.age_vs_performance)
        self.add_tab("Market Value by Position", self.players.market_value_by_position)
        self.add_tab("Player Consistency", self.players.player_consistency)
    def add_tab(self, title, figure_method):
        """
        Crea una nueva pestaña en el cuaderno y genera una figura utilizando un método específico de la clase Players. 
        Aplica el estilo personalizado a la gráfica y la inserta en la pestaña.
        """
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text=title)
        tab.pack_propagate(False)
        # Create the figure
        fig, _ = figure_method()

        # Embed the figure in the tab
        self.apply_chart_style(fig.gca())
        self.embed_figure(tab, fig)

    def embed_figure(self, tab, figure):
        """
        Inserta una figura de Matplotlib en una pestaña específica.
        Utiliza la clase FigureCanvasTkAgg para integrar la gráfica dentro de la interfaz de usuario de Tkinter.
        """
        canvas = FigureCanvasTkAgg(figure, tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=BOTH, expand=True)
        canvas.draw_idle()
        # Bind a resize event to handle resizing the figure dynamically


        

# Main application setup
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = PlayerApp(root)
    app.center_window(root)
    root.mainloop()
