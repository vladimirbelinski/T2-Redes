import socket
import _thread
import cliente

# Name: thread.py
# Author: Vladimir Belinski
# Description: this file contains the class thread, used in the implementation of an application using TCP
#              In the application the user specifies an address and a port for a server and the server address, the
#              port and an order file for the client. After initializing both, server and client, the client sends
#              the content of the order file to the server, that returns to the client the number of different itens
#              and the total amount for the order submitted.

class thread():
    def __init__(self):
        self._error = False
        self.reset()

    def stop(self):
        self._stop = True
        # It is sent a request because the server is waiting for a connection (necessary to stop the client thread and the server)
        cliente.reqResult(self.addr, int(self.port), '')

    def stopped(self):
        return self._stop

    def reset(self):
        self._stop = False
        self._done = False
        self.addr = self.port = 0

    def finished(self):
        return self._done

    def run(self, trg, addr, port):
        self.addr = addr
        self.port = port
        _thread.start_new_thread(trg, (addr, port, self))

    def error(self):
        return self._error
