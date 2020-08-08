import socket

from .connection import Connection

class Server:
    socket_s = None
    socket_host = ''
    socket_port = 7337

    @staticmethod
    def __create_socket__(HOST='', PORT=7337):
        try:
            Server.socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            Server.socket_s = None
            pass

        try:
            if Server.socket_s:
                Server.socket_s.bind((HOST, PORT))
        except socket.error:
            Server.socket_s.close()
            Server.socket_s = None
            pass
        pass

    def __init__(self, PORT=socket_port):

        if not Server.socket_s:
            Server.__create_socket__(PORT=PORT)
            pass

        self.is_listening = False
        pass

    def listen(self, broadcast=1):
        if not Server.socket_s:
            Server.__create_socket__()
            pass

        Server.socket_s.listen(broadcast)
        self.is_listening = True
        pass

    def wait_connection(self, auth=None):
        if not Server.socket_s:
            Server.__create_socket__()
            self.listen()
            pass

        if not self.is_listening:
            self.listen()

        (conn, addr) = Server.socket_s.accept()

        cred = None
        if auth: # authentication
            pass        

        return Connection(
            connection=conn,
            address=addr,
            auth=auth,
            credentials=cred,
        )
