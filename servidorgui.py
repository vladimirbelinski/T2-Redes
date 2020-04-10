#!/usr/bin/python3
import time
import tkinter as tk
import thread as thread
from tkinter import ttk
from tkinter import messagebox
from servidor import clientThread, startserver

# Name: servidorgui.py
# Author: Vladimir Belinski
# Execution: ./servidorgui.py
# Description: this file contains the GUI implementation of the server side of an application using TCP
#              In the application the user specifies an address and a port for a server and the server address, the
#              port and an order file for the client. After initializing both, server and client, the client sends
#              the content of the order file to the server, that returns to the client the number of different itens
#              and the total amount for the order submitted.


class serverGUI():
    def __init__(self):
        self.gui = tk.Tk()
        self.saddrEntry = tk.StringVar()
        self.portEntry = tk.StringVar()
        self.servidor = thread.thread()
        self.statusMsg = tk.StringVar()
        self.widgets()
        self.gui.wm_title("Servidor")
        self.gui.configure(bg="gray70")
        self.gui.protocol("WM_DELETE_WINDOW", self.close)

    def widgets(self):
        # Defining some values for fonts and background
        ft1=('Helvetica', '10')
        bg0=('gray70'); bg1=('gray92'); bg2=('gray77')

        # Instructions frame
        self.instrFrame = tk.Frame(self.gui, bg=bg0, bd=5)
        self.lbInstr = tk.Label(self.instrFrame, text="INSTRUÇÕES:\nPara usar a aplicação servidor por favor preencha todos os campos abaixo e clique em 'Iniciar'\nObs.: o valor de 'Porta' deve ser um número inteiro", bg=bg1, font=ft1).pack(fill='x')
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
        self.lbPort.pack(fill='x'); self.port.pack(fill='x'); self.formsFrame.pack(fill='x')

        # Start and stop frame
        self.startFrame = tk.Frame(self.gui, bg=bg0, pady=8)
        self.startStop = tk.Button(self.startFrame, text="Iniciar")
        self.startStop["command"] = self.startFunc
        self.startStop.pack(); self.startFrame.pack(fill='x')

        # Status frame
        self.statusFrame = tk.Frame(self.gui, bg='gray70', bd=5)
        self.statusMsg.set("Status: Aguardando entrada...")
        self.lbStatus = tk.Label(self.statusFrame, textvariable=self.statusMsg, bg=bg1).pack()
        self.statusFrame.pack(fill='x')


    def startFunc(self):
        # Starting the server...
        if self.startStop["text"] == "Iniciar":
            try:
                self.servidor.run(startserver, self.saddrEntry.get(), int(self.portEntry.get()))
                # This time.sleep is used to give time to thread._entry be set on server.py before test it with error()
                time.sleep(0.1)
                if self.servidor.error():
                    tk.messagebox.showerror('Erro', 'Porta já em uso! Favor informar outra porta!')
                    return
            except ValueError:
                tk.messagebox.showerror('Erro', 'Por favor confira as instruções!')
                return
            self.statusMsg.set("Status: Servidor rodando...")
            self.startStop["text"] = "Parar"
        # Stopping the server
        else:
            self.servidor.stop()
            while not self.servidor.finished():
                continue
            self.servidor.reset()
            self.statusMsg.set("Status: Servidor parado...")
            self.startStop["text"] = "Iniciar"

    def close(self):
        self.servidor.stop()
        self.gui.destroy()

    def run(self):
        self.gui.mainloop()

def main():
    serverGUI().run()

if __name__ == "__main__":
    main()
