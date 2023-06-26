from models import Transacao, TransacaoDAO
from edit_window import EditWindow
from create_window import CreateWindow
from graph_window import GraphWindow

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import date

class MainWindow(tk.Frame):
    def __init__(self, master, dao):
        super().__init__(master)
        self.dao = dao
        self.create_widgets()

    def create_widgets(self):
        padding = 10

        header_label = tk.Label(self, text="Lista de Transações", font=("Arial", 16, "bold"))
        header_label.pack(pady=padding)

        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=padding)

        filter_label = tk.Label(filter_frame, text="Filtrar por:")
        filter_label.pack(side=tk.LEFT)

        self.filter_var = tk.StringVar()
        self.filter_var.set("Todas")
        filter_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["Todas", "Entrada", "Saída"])
        filter_combobox.pack(side=tk.LEFT, padx=5)

        filter_button = tk.Button(filter_frame, text="Filtrar", command=self.filter_transacoes)
        filter_button.pack(side=tk.LEFT)

        self.treeview = ttk.Treeview(self, columns=("id", "titulo", "valor", "data", "is_saida"), show="headings")
        self.treeview.pack(pady=padding)

        self.treeview.heading("id", text="id")
        self.treeview.heading("titulo", text="Título")
        self.treeview.heading("valor", text="Valor")
        self.treeview.heading("data", text="Data")
        self.treeview.heading("is_saida", text="Tipo")

        action_frame = tk.Frame(self)
        action_frame.pack(pady=10)

        create_button = tk.Button(action_frame, text="Criar Transação", command=self.open_create_window)
        create_button.grid(row=0, column=0, padx=5)

        edit_button = tk.Button(action_frame, text="Editar", command=self.edit_selected)
        edit_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(action_frame, text="Deletar", command=self.delete_selected)
        delete_button.grid(row=0, column=2, padx=5)

        graph_button = tk.Button(action_frame, text="Abrir Gráficos", command=self.open_graph_window)
        graph_button.grid(row=0, column=3, padx=5)

        self.saldo_label = tk.Label(self, text="Saldo: R$0.00", font=("Arial", 14))
        self.saldo_label.pack(pady=10)

        self.update_saldo()
        self.update_table()


    def open_create_window(self):
        create_window = CreateWindow(self, self.dao)
        create_window.mainloop()

    def edit_selected(self):
        selection = self.treeview.selection()
        if len(selection) == 1:
            item_id = selection[0]
            item_values = self.treeview.item(item_id, 'values')
            item_id = item_values[0]
            titulo = item_values[1]
            valor = item_values[2]
            data = item_values[3]
            tipo = item_values[4]

            edit_window = EditWindow(self.master, self.dao, item_id, titulo, valor, data, tipo)
            edit_window.transient(self.master)
            edit_window.grab_set()
            self.master.wait_window(edit_window)
            
            self.update_table()
            self.update_saldo()

    def update_saldo(self):
        saldo = self.dao.get_saldo()
        self.saldo_label.config(text=f"Saldo: R$ {saldo:.2f}")

    def update_table(self):
        self.treeview.delete(*self.treeview.get_children())

        transacoes = self.dao.get_all_transacoes()

        filtro = self.filter_var.get()
        if filtro != "Todas":
            if filtro == "Entrada":
                transacoes = self.dao.get_all_entradas()
            if filtro == "Saída":
                transacoes = self.dao.get_all_saidas()

        for transacao in transacoes:
            tipo = "Saída" if transacao.is_saida else "Entrada"
            self.treeview.insert("", "end", values=(transacao.id, transacao.titulo, transacao.valor, transacao.data.split()[0], tipo))

    def filter_transacoes(self):
        self.update_table()

    def delete_selected(self):
        selection = self.treeview.selection()
        if len(selection) == 1:
            item_id = selection[0]
            values = self.treeview.item(item_id, 'values')
            item_id = values[0]
            titulo = values[1]

            result = messagebox.askyesno("Confirmação", f"Deseja excluir a transação: {titulo}?")
            if result:
                self.dao.delete_transacao(item_id)
                self.update_table()
    
    def open_graph_window(self):
        graph_window = GraphWindow(self.master, self.dao)
        graph_window.transient(self.master)
        graph_window.grab_set()
        self.master.wait_window(graph_window)