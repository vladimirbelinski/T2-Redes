#!/usr/bin/python3
import sys
import socket
import clientegui

# Name: cliente.py
# Author: Vladimir Belinski
# Execution (without GUI): ./cliente.py <serverAddress> <port> <file>
# Description: this file contains the implementation of the client side of an application using TCP
#              In the application the user specifies an address and a port for a server and the server address, the
#              port and an order file for the client. After initializing both, server and client, the client sends
#              the content of the order file to the server, that returns to the client the number of different itens
#              and the total amount for the order submitted.

# In reqResult the content of the order file specified by the user is sent to the server and its answer is received
# and passed to main()
def reqResult(ip, port, fpath):
    # Create a TCP/IP socket using the given address family, socket type and protocol number
    # AF_INET is an address family that is used to designate the type of addresses that the socket can communicate
    # with (in this case IPv4 addresses). SOCK_STREAM is the default value for the socket type. The protocol number
    # is usually zero and may be omitted in that case (this is done here). 's' is the name given to the socket.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # serverAnsw is used to receive and store the server answer
    serverAnsw = bytes("", 'utf-8')

    try:
        # Connect the socket to the port where the server is listening
        serverAddress = (ip, port)
        s.connect(serverAddress)
        if (fpath != '' and controller):
            print("\n>>>Iniciando conexão com servidor {} na porta {}".format(ip, port))

        # SENDING THE REQUEST:
        # The order file is open and read; its content is converted to bytes and send to the server with its lenght
        # concatenated at the beggining and separated by a '|'.
        # It is necessary to send the lenght for the server know when the message is finished
        # sendall() is the function used to send the content of the file to the server
        orderFile = open(fpath, 'r')
        content = orderFile.read()
        s.sendall(bytes(str(len(bytes(content, 'utf-8'))) + "|" + content, 'utf-8'))

        # RECEIVING THE ANSWER:
        # amtExp and amtRcv are the data amount expected and data amount received, respectively, from a server answer
        amtExp = amtRcv = 0
        # The function of this first while is get the lenght of the message that will be received from the server
        while True:
            # serverAnsw receives 32 bytes
            serverAnsw += s.recv(32)
            # It is necessary to have a try here because decode() can handle special symbols, so if the last symbol is
            # a special symbol more 32 bytes are read, until we have a non special symbol at the end of the token
            try:
                # The answer is decoded to utf-8 to be possible to split on '|'. After, its converted to bytes again
                # because the answer will continue to be received in bytes
                serverAnsw = serverAnsw.decode('utf-8').split('|')
                serverAnsw[1] = bytes(serverAnsw[1], 'utf-8')
                # The first part consists in the value of data amount expected
                amtExp = int(serverAnsw[0])
                # The second is already part of the response, so it is necessary to add its lenght to amtRcv
                amtRcv = len(serverAnsw[1])
                serverAnsw = serverAnsw[1]
                break
            except:
                continue

        # While there is data to receive from the server...
        while amtRcv < amtExp:
            # Receive 32 bytes, concatenate the current part with the part already received and update amtRcv
            # It was chosen to receive 32 bytes just for educational purposes (to break the message into packets)
            partMsg = s.recv(32)
            serverAnsw += partMsg
            amtRcv += len(partMsg)

    except KeyboardInterrupt:
        print("\b\b>>>Fechando cliente")
    except:
        serverAnsw = bytes(">>>Erro inesperado!", 'utf-8')
    finally:
        # close() is the function to close the socket
        s.close()
        # Return the server answer or an error to main()
        return serverAnsw.decode('utf-8');

def main(argv):
    # Check if the user passed the correct number of arguments
    if (len(sys.argv) != 4):
        print("\n>>>Erro: número errado de argumentos!\n")
        sys.exit()

    # Put the arguments in variables and check if the value of 'Port' is an integer
    ipserver = argv[1]; filepath = argv[3];
    try:
        port = int(argv[2])
    except ValueError:
        print("\n>>>Erro: o valor da porta deve ser um inteiro!\n")
        sys.exit()
    except:
        print("\n>>>Erro: erro inesperado!\n")
        sys.exit()

    # Print the result returned by reqResult: the server answer or an error
    print(reqResult(ipserver, port, filepath) + "\n");

# controller is True when is a non GUI execution; it is used to controll the prints
controller = False
if __name__ == "__main__":
    # If the user passed arguments his entry is treated as an execution without GUI
    if len(sys.argv) > 1:
        controller = True
        main(sys.argv)
    # Else, his entry is treated as an execution with GUI
    else:
        clientegui.clientGUI().run()
