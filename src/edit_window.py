from models import Transacao

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry

class EditWindow(tk.Toplevel):

    def __init__(self, master, dao, item_id, titulo, valor, data, tipo):
        super().__init__(master)

        self.dao = dao
        self.item_id = item_id
        self.titulo = tk.StringVar(value=titulo)
        self.valor = tk.DoubleVar(value=valor)
        self.data_transacao = data
        self.data = tk.StringVar(value=data)
        self.tipo = tk.StringVar(value=tipo)

        self.create_widgets()

    def create_widgets(self):
        self.title("Editar Transação")
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
        data_entry = DateEntry(self, textvariable=self.data, date_pattern="yyyy-mm-dd")
        data_entry.set_date(datetime.strptime(self.data_transacao, "%Y-%m-%d"))        
        data_entry.pack()

        tipo_label = tk.Label(self, text="Tipo:")
        tipo_label.pack()
        tipo_entry = ttk.Combobox(self, textvariable=self.tipo, values=["Entrada", "Saída"])
        tipo_entry.pack()

        save_button = tk.Button(self, text="Salvar", command=self.save_changes)
        save_button.pack(pady=10)

    def save_changes(self):
        titulo = self.titulo.get()
        valor = self.valor.get()
        data = datetime.strptime(self.data.get(), "%Y-%m-%d")
        tipo = False if self.tipo.get() == 'Entrada' else True
        
        self.dao.update_transacao(Transacao(self.item_id, titulo, valor, str(data).split()[0], tipo))
        self.destroy()