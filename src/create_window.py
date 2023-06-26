from models import TransacaoDAO, Transacao  

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class CreateWindow(tk.Toplevel):
    def __init__(self, master, dao):
        super().__init__(master)

        self.dao = dao
        self.titulo = tk.StringVar()
        self.valor = tk.DoubleVar()
        self.data = tk.StringVar()
        self.tipo = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.title("Criar Transação")
        self.geometry("200x250")

        titulo_label = tk.Label(self, text="Título:")
        titulo_label.pack()
        titulo_entry = tk.Entry(self, textvariable=self.titulo)
        titulo_entry.pack()

        valor_label = tk.Label(self, text="Valor:")
        valor_label.pack()
        valor_entry = tk.Entry(self, textvariable=self.valor)
        valor_entry.pack()

        data_label = tk.Label(self, text="Data:")
        data_label.pack()
        data_entry = DateEntry(self, textvariable=self.data, date_pattern='yyyy-mm-dd')
        data_entry.pack()

        tipo_label = tk.Label(self, text="Tipo:")
        tipo_label.pack()
        tipo_entry = ttk.Combobox(self, textvariable=self.tipo, values=["Entrada", "Saída"])
        tipo_entry.pack()

        save_button = tk.Button(self, text="Salvar", command=self.save_transacao)
        save_button.pack(pady=10)

    def save_transacao(self):
        titulo = self.titulo.get()
        valor = self.valor.get()
        data = str(datetime.strptime(self.data.get(), "%Y-%m-%d"))
        tipo = False if self.tipo.get() == 'Entrada' else True

        self.dao.insert_transacao(Transacao(None, titulo, valor, data.split()[0], tipo))

        self.master.update_table()
        self.master.update_saldo()
        self.destroy()