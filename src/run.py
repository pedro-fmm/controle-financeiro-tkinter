from models import Transacao, TransacaoDAO
from main_window import MainWindow

import tkinter as tk
from datetime import date

if __name__ == '__main__':
    db_name = 'transacoes.sqlite'
    dao = TransacaoDAO(db_name)
    window = tk.Tk()
    window.title("Minhas Transações")
    window.geometry("1200x450")
    main_screen = MainWindow(window, dao)
    main_screen.pack()
    window.mainloop()
    dao.close()