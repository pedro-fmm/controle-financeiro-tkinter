import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GraphWindow(tk.Toplevel):
    def __init__(self, master, dao):
        super().__init__(master)
        self.title("Gráficos")
        self.dao = dao
        
        self.filter_var = tk.StringVar()
        self.filter_var.set("1 mês")
        self.filter_tipo = tk.StringVar()
        self.filter_tipo.set("Entrada")
        

        filter_frame_var = tk.Frame(self)
        filter_frame_var.pack(pady=5)

        filter_label = tk.Label(filter_frame_var, text="Filtrar por:")
        filter_label.pack(side=tk.LEFT)

        filter_combobox = ttk.Combobox(filter_frame_var, textvariable=self.filter_var, values=["1 mês", "3 meses", "6 meses"])
        filter_combobox.pack(pady=5)

        filter_frame_tipo = tk.Frame(self)
        filter_frame_tipo.pack(pady=5)

        filter_label = tk.Label(filter_frame_tipo, text="Filtrar por:")
        filter_label.pack(side=tk.LEFT)        

        filter_tipo = ttk.Combobox(filter_frame_tipo, textvariable=self.filter_tipo, values=["Entrada", "Saida"])
        filter_tipo.pack(pady=5)
        
        self.figure = Figure(figsize=(6, 4), dpi=150)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(padx=5)
         
        show_button = tk.Button(self, text="Mostrar Gráfico", command=self.show_graph)
        show_button.pack(pady=10)
        
    def show_graph(self):
        selected_filter_meses = self.filter_var.get()
        selected_filter_tipo = self.filter_tipo.get()

        meses = selected_filter_meses.split()[0]
        tipo = selected_filter_tipo

        transacoes = self.dao.get_transacoes_graph(meses, tipo)
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if int(meses) == 1:    
            x = transacoes["datas"]; x.sort()
            y = transacoes["valores"]; y.sort()
            if len(transacoes) == 1:
               ax.bar(x, y)
            else:
                ax.plot(x, y)
        else:
            x = [ i for i in transacoes.keys()]; x.sort()
            y = [ transacoes[i] for i in x ]
            ax.bar(x, y)
        
        ax.set_xlabel("Datas")
        ax.set_ylabel("Valores")

        self.canvas.draw()