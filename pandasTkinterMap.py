import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Players_class import Players

class PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Data Analysis")

        # Get the screen dimensions
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates for the window to be centered

        # Set the geometry of the window
        root.geometry(f"{self.screen_width}x{self.screen_height}")
        root.attributes('-fullscreen',True)

        self.style = ttk.Style("darkly")  # Applying a modern dark theme.
        self.style.configure("TFrame", background="black")

        self.create_resume_frame()

    def create_resume_frame(self):
        """
        Create the initial presentation frame
        """

        self.resume_frame = ttk.Frame(self.root,padding=20)
        self.resume_frame.pack(fill=ttk.BOTH,expand=True)

        header_label = ttk.Label(
            self.resume_frame,
            text='Bienvenido al Analisis de datos de los jugadores',
            bootstyle = 'danger',
            background='black',
            font=('Helvetica',36,'bold')
        )
        header_label.pack(pady=20)

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
            font=('Helvetica',24,'italic')
        )
        creator_label.pack(pady=50)
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
        more_info_button.pack(side=LEFT, padx=10)

        greetings_button = ttk.Button(
            button_frame,
            text="Greetings!",
            bootstyle="secondary",
            command=self.show_greetings
        )
        greetings_button.pack(side=LEFT, padx=10)

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
        Show additional information about the program in a pop-up window.
        """
        info_window = ttk.Toplevel(self.root)
        info_window.title("More Information")
        info_window.geometry("1000x400")

        info_label = ttk.Label(
            info_window,
            text=(
                "This program is designed to analyze player statistics using data scraping and \n"
                "visualization techniques. You can explore trends, performance metrics, and much more!"
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

    def show_greetings(self):
        """
        Display a greeting message in a pop-up window.
        """
        greeting_window = ttk.Toplevel(self.root)
        greeting_window.title("Greetings")
        greeting_window.geometry("800x200")

        greeting_label = ttk.Label(
            greeting_window,
            text="Hello! Thank you for using the Player Data Analysis App!",
            bootstyle="success",
            font=("Helvetica", 16)
        )
        greeting_label.pack(pady=20)

        close_button = ttk.Button(
            greeting_window,
            text="Close",
            bootstyle="secondary",
            command=greeting_window.destroy
        )
        close_button.pack(pady=10)

    def load_notebook(self):
        self.resume_frame.destroy()
        self.notebook = ttk.Notebook(self.root, bootstyle="dark")
        self.notebook.pack(fill=BOTH, expand=True)
        self.style.configure('TLabel',font=('Helvetica',32,'bold'))
        self.status_progressBar = ttk.Progressbar(bootstyle="info-striped")
        self.text_progressBar = ttk.Label(master=self.notebook,text='Loading Data......',bootstyle='info',style='TLabel').place(x=700,y=(self.screen_height//2)-100)
        self.status_progressBar.place(x=100,y=(self.screen_height//2),width=self.screen_width-200)
       

        self.players = Players()  # Initialize Players class
        self.check_data_ready()  # Start checking for data readiness

    def apply_chart_style(self,ax):
        """
        Apply custom styles to a matplotlib chart.
        """
        ax.set_facecolor("none")
        ax.title.set_color("black")
        ax.xaxis.label.set_color("black")
        ax.yaxis.label.set_color("black")
        ax.tick_params(axis="both", colors="black")
        for spine in ax.spines.values():
            spine.set_edgecolor("black")
    def check_data_ready(self):
        """
        Periodically check if the Players instance has finished scraping.
        """
        if not self.players.scraping_done:
            self.status_progressBar.start()
            self.root.after(10100, self.check_data_ready)
        else:
            self.status_progressBar.destroy()
            self.add_tabs()  # Retry after 500ms

    def add_tabs(self):
        """
        Create tabs for each analysis/visualization figure.
        """
        self.add_tab("Player Value Change", self.players.get_player_data)
        self.add_tab("Historical Trends", self.players.analyze_historical_trends)
        self.add_tab("Metrics by Position", self.players.group_analysis_by_position)
        self.add_tab("Age vs Performance", self.players.age_vs_performance)
        self.add_tab("Market Value by Position", self.players.market_value_by_position)
        self.add_tab("Player Consistency", self.players.player_consistency)
    def add_tab(self, title, figure_method):
        """
        Add a tab with the specified title and figure from the given method.
        """
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text=title)

        # Create the figure
        fig, _ = figure_method()

        # Embed the figure in the tab
        self.apply_chart_style(fig.gca())
        self.embed_figure(tab, fig)

    def embed_figure(self, tab, figure):
        """
        Embed a Matplotlib figure in the given tab.
        """
        canvas = FigureCanvasTkAgg(figure, tab)
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        canvas.draw()


# Main application setup
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = PlayerApp(root)
    root.mainloop()
