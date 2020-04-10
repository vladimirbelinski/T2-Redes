#!/usr/bin/python3
import cliente
import _thread
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Name: clientegui.py
# Author: Vladimir Belinski
# Execution (with GUI): ./cliente.py or ./clientegui.py
# Description: this file contains the GUI implementation of the client side of an application using TCP
#              In the application the user specifies an address and a port for a server and the server address, the
#              port and an order file for the client. After initializing both, server and client, the client sends
#              the content of the order file to the server, that returns to the client the number of different itens
#              and the total amount for the order submitted.


class clientGUI():
    def __init__(self):
        self.gui = tk.Tk()
        self.pathEntry = tk.StringVar()
        self.portEntry = tk.StringVar()
        self.saddrEntry = tk.StringVar()
        self.statusMsg = tk.StringVar()
        self.widgets()
        self.gui.wm_title("Cliente")
        self.gui.configure(bg="gray70")
        self.gui.protocol("WM_DELETE_WINDOW", self.close)

    def widgets(self):
        # Defining some values for fonts and background
        ft1=('Helvetica', '10')
        bg0=('gray70'); bg1=('gray92'); bg2=('gray77')

        # Instructions frame
        self.instrFrame = tk.Frame(self.gui, bg=bg0, bd=5)
        self.lbInstr = tk.Label(self.instrFrame, text="INSTRUÇÕES:\nPara usar a aplicação cliente por favor preencha todos os campos abaixo e clique em 'Enviar'\nObs.: o valor de 'Porta' deve ser um número inteiro", bg=bg1, font=ft1).pack(fill='x')
        self.instrFrame.pack(fill='x')

        # Forms frame
        self.formsFrame = tk.Frame(self.gui, bg=bg0, bd=6)
        # Label and entry for server address
        self.lbSaddr = tk.Label(self.formsFrame, text="Endereço IP do servidor", pady=5, bg=bg2)
        self.saddr = tk.Entry(self.formsFrame, exportselection=0, textvariable=self.saddrEntry, bg=bg1)
        self.saddr.focus_force()
        self.lbSaddr.pack(fill='x'); self.saddr.pack(fill='x')
        # Label and entry for port
        self.lbPort = tk.Label(self.formsFrame, text="Porta", pady=5, bg=bg2)
        self.port = tk.Entry(self.formsFrame, exportselection=0, textvariable=self.portEntry, bg=bg1)
        self.lbPort.pack(fill='x'); self.port.pack(fill='x')
        # Label and entry for file path
        self.pathFrame = tk.Frame(self.formsFrame, bg=bg2)
        self.lbPath = tk.Label(self.pathFrame, text="Caminho do arquivo", pady=5, bg=bg2)
        self.path = tk.Entry(self.pathFrame, exportselection=0, state='readonly', textvariable=self.pathEntry)
        self.lbPath.pack(fill='x'); self.path.pack(fill='x', side='left', expand=1)
        # Button for search
        self.search = tk.Button(self.pathFrame, text="Procurar")
        self.search["command"] = self.searchFunc
        self.search.pack(side='left');
        self.pathFrame.pack(fill='x'); self.formsFrame.pack(fill='x')

        # Submit frame
        self.submitFrame = tk.Frame(self.gui, bg='gray70', pady=8)
        # Button for submit
        self.submit = tk.Button(self.submitFrame, text="Enviar")
        self.submit["command"] = self.submitFunc
        self.submit.pack(); self.submitFrame.pack(fill='x')

        # Status frame
        self.statusFrame = tk.Frame(self.gui, bg='gray70', bd=5)
        self.statusMsg.set("Status: Aguardando entrada...")
        self.lbStatus = tk.Label(self.statusFrame, textvariable=self.statusMsg, bg=bg1).pack()
        self.statusFrame.pack(fill='x')

    def searchFunc(self):
        path = filedialog.askopenfilename()
        # Setting pathEntry if the entry is not empty
        if (path != ""):
            self.pathEntry.set(path)

    def submitFunc(self):
        self.statusMsg.set("Status: Processando...")
        # When the user click on 'Submit' the entries are disabled and a new thread is started
        self.entry('disabled');
        _thread.start_new_thread(self.sendFunc, ())

    def sendFunc(self):
        try:
            # Treating an empty entries
            if ((self.saddrEntry.get() == "") or (self.portEntry.get() == "") or (self.pathEntry.get() == "")):
                raise ValueError()
            # Treating nonstandard file
            resultado = cliente.reqResult(self.saddrEntry.get(), int(self.portEntry.get()), self.pathEntry.get())
            if (resultado == "Arquivo fora do formato padrão!"):
                raise ValueError("1")
            elif (resultado == ">>>Erro inesperado!"):
                raise ValueError("2")
            tk.messagebox.showinfo('Resultado', resultado)

        except ValueError as flag:
            if ("{}".format(flag) == "1"):
                tk.messagebox.showerror('Erro', 'Arquivo fora do formato padrão!')
            elif ("{}".format(flag) == "2"):
                tk.messagebox.showerror('Erro', 'Erro inesperado!')
            else:
                tk.messagebox.showerror('Erro', 'Por favor confira as instruções!')

        finally:
            self.entry('normal')
            self.statusMsg.set("Status: Aguardando entrada...")

    def entry(self, status):
        # Configuring the text entries
        self.search.config(state = status)
        self.submit.config(state = status)
        self.saddr.config(state = status)
        self.port.config(state = status)
        # Path entry is set readonly to avoid wrong paths. This way the user must use the search option
        if (status == 'normal'):
            status = 'readonly'
        self.path.config(state = status)

    def close(self):
        self.gui.destroy()

    def run(self):
        self.gui.mainloop()

def main():
    clientGUI().run()

if __name__ == "__main__":
    main()
