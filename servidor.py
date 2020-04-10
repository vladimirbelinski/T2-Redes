#!/usr/bin/python3
import sys
import socket
import threading
import tkinter as tk
from _thread import *
from tkinter import ttk

# Name: servidor.py
# Author: Vladimir Belinski
# Execution (without GUI): ./servidor.py (for default values) OR ./servidor.py <serverAddress> <port>
# Description: this file contains the implementation of the server side of an application using TCP
#              In the application the user specifies an address and a port for a server and the server address, the
#              port and an order file for the client. After initializing both, server and client, the client sends
#              the content of the order file to the server, that returns to the client the number of different itens
#              and the total amount for the order submitted.

def clientThread(connection, clientAddress, stop_event):
        # RECEIVING THE REQUEST:
        # set() is an unordered collection of unique elements used to count how many different itens the clientMsg has
        itensSet = set()
        # value is used to store the total value of the order; i is an iterator used just for some prints
        value = 0; i = 0
        # amtExp and amtRcv are the data amount expected and data amount received, respectively, from a client message
        amtExp = amtRcv = 0
        # clientMsg is used to receive and store the client message
        clientMsg = bytes("", 'utf-8')

        # The function of this first while is get the lenght of the message that will be received from the client
        while True:
            # clientMsg receives 32 bytes
            clientMsg += connection.recv(32)
            # It is necessary to have a try here because decode() can handle special symbols, so if the last symbol is
            # a special symbol more 32 bytes are read, until we have a non special symbol at the end of the token
            try:
                # The request is decoded to utf-8 to be possible to split on '|'. After, its converted to bytes again
                # because the request will continue to be received in bytes
                clientMsg = clientMsg.decode('utf-8').split('|')
                clientMsg[1] = bytes(clientMsg[1], 'utf-8')
                # The first part consists in the value of data amount expected
                amtExp = int(clientMsg[0])
                # The second is already part of the order, so it is necessary to add its lenght to amtRcv
                amtRcv = len(clientMsg[1])
                clientMsg = clientMsg[1]
                if (controller):
                    print("...Recebendo de {}: ({}/{})".format(clientAddress, amtRcv, amtExp))
                break;
            except:
                continue;

        try:
            # While there is data to receive from the client...
            while amtRcv < amtExp:
                # Receive 32 bytes, concatenate the current part with the part already received and update amtRcv
                # It was chosen to receive 32 bytes just for educational purposes (to break the message into packets)
                partMsg = connection.recv(32)
                clientMsg += partMsg
                amtRcv += len(partMsg)
                # Printing the status just for the user know the message is being received
                if (controller):
                    if (i == 999):
                        print("...Recebendo de {}: ({}/{})".format(clientAddress, amtRcv, amtExp))
                    i = (i + 1) % 1000
                # If stop_event is set the server is not running, so an exception is raised
                if (stop_event.is_set()):
                    raise OSError()

            if (controller):
                print("...Recebendo de {}: ({}/{})".format(clientAddress, amtRcv, amtExp))
                print ("...Não há mais dados de {}".format(clientAddress))

            # PREPARING AND SENDING THE ANSWER:
            # Now the answer can be calculated. So, clientMsg is splitted at the end of each product line
            clientMsg = clientMsg.decode('utf-8').split('\n')
            # The last entry is "" because of the split above, so it is necessary to pop it
            clientMsg.pop(-1)
            # '(' and ')' are not considered; the infos are splitted at commas
            for token in clientMsg:
                token = token.replace("(", ""); token = token.replace(")", "");
                token = token.split(",");
                try:
                    # "" or an item that starts with " " are unconsidered
                    if ((token[0] != "") and (token[0][0] != " ")):
                        # The first value is the item name, added to the set of unique elements
                        itensSet.add(token[0]);
                        # The total value of the order is calculated
                        value += int(token[1]) * float(token[2]);
                except:
                    answer = "Arquivo fora do formato padrão!"
                    connection.sendall(bytes(str(len(bytes(answer, 'utf-8'))) + "|" + answer, 'utf-8'))
                    raise OSError()
                # If stop_event is set the server is not running, so an exception is raised
                if (stop_event.is_set()):
                    raise OSError()
            # The server answer is created and send to the client
            answer = "O pedido contém {} itens e resulta em um valor total de R$ {:.2f}.".format(len(itensSet), value);
            connection.sendall(bytes(str(len(bytes(answer, 'utf-8'))) + "|" + answer, 'utf-8'))

            # The client connection is closed
            connection.close()

        except OSError:
            # If the server was stopped or closed the client connection is closed too
            connection.close()


def startserver(addr, port, thread):
    # Create a TCP/IP socket using the given address family, socket type and protocol number
    # AF_INET is an address family that is used to designate the type of addresses that the socket can communicate
    # with (in this case IPv4 addresses). SOCK_STREAM is the default value for the socket type. The protocol number
    # is usually zero and may be omitted in that case (this is done here). 's' is the name given to the socket.
    if thread != None:
        thread._error = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress = (addr, port)
    # SO_REUSEADDR is used to avoid the TIME_WAIT, so a process do not need to wait to listen in the specified port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # There is a try here because it is necessary to handle exceptions when bind is not ok (e.g.: if the port is
    # already in use)
    try:
        # bind() is used to associate the socket with the server address
        s.bind(serverAddress)
    except:
        if (controller):
            print('\n>>>A porta informada já está sendo utilizada! Por favor tente usar outra porta.\n')
        if thread != None:
            thread._error = True
            thread._done = True
        return
    if (controller):
        print ("\n>>>Servidor iniciando em (endereço, porta): {}".format(serverAddress))
    # The argument to listen() tells the socket library that we want it to queue up as many as 5 connect resquests
    # (the normal max) before refusing outside connections. Calling listen() puts the socket into server mode
    s.listen(5)

    try:
        # To stop the client thread in execution it is necessary set and event, here named t_stop
        t_stop = threading.Event()
        while thread == None or not thread.stopped():
            if (controller):
                print (">>>Aguardando por conexões")
            # With accept() the socket waits for an incoming connection
            connection, clientAddress = s.accept()
            # If there is a client thread in execution and the server is stopped it is necessary to set t_stop to
            # close the client thread and raise and exception
            if (thread != None and thread.stopped()):
                t_stop.set()
                raise OSError('>>>Servidor parado')
            # Starting a new client thread
            if (controller):
                print (">>>Iniciando conexão para {}".format(clientAddress))
            # start_new_thread(target, (args- socket and clientAdress caught on accept() and the stop flag))
            start_new_thread(clientThread, (connection, clientAddress, t_stop))
    # Exception when closing the server in a non GUI execution
    except KeyboardInterrupt:
        if (controller):
            print("\b\b>>>Fechando o servidor\n")
    except OSError as msg:
        if (controller):
            print("{}".format(msg))
    finally:
        s.close()
        if thread != None:
            thread._done = True

def main(argv):
    ipserver = argv[1]
    try:
        port = int(argv[2])
        startserver(ipserver, port, None)
    except ValueError:
        if (controller):
            print("Erro: o valor da porta deve ser um inteiro!")
        sys.exit()
    except:
        if (controller):
            print("Erro: erro inesperado!")
        sys.exit()

# If the user is not using the GUI for the server, then the values are fixed in '' for the server address
# ('' specifies that the soket is reachable by any address the machine happens to have) and 10000 for the port.
# During the inialization there is not a client thread yet, this is what means the 3rd argument
# If the user passes more than 1 arg then the default values are not considered
# controller is True when is a non GUI execution; it is used to controll the prints
controller = False
if __name__ == "__main__":
    controller = True
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        startserver('', 10000, None)
