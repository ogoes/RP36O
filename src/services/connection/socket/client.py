import socket

from .connection import Connection


class Client:
    def __init__(self, **attrs):
        self.attrs = attrs

        self.__socket = None
        self.__connection = None

    def __authenticate__(self, key=None):
        return key

    def connect(self, HOST, PORT, key=None):

        infos = {}

        for addrinfo in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            if self.__socket: # authentication
                infos['auth'] = self.__authenticate__(key)
                break

            AF_FAMILY, SOCK_TYPE, SOCK_PROTOCOL, canonname, INFOS = addrinfo
            try:
                self.__socket = socket.socket(AF_FAMILY, SOCK_TYPE, SOCK_PROTOCOL)
            except socket.error:
                self.__socket = None
                continue

            try:
                self.__socket.connect(INFOS)
            except socket.error:
                self.__socket.close()
                self.__socket = None
                continue

            infos['socket_infos'] = {
                'family': AF_FAMILY,
                'type': SOCK_TYPE,
                'protocol': SOCK_PROTOCOL,
            }

            infos['server_infos'] = {
                'name': canonname,
                'host': INFOS[0],
                'port': INFOS[1],
            }

            break

        if not self.__socket:
            return False

        self.__connection = Connection(
            connection=self.__socket,
            socket=infos.get('socket_infos'),
            auth=infos['auth'],
            server=infos['server_infos'],
        )

        return True

    def send(self, data):
        if self.__connection:
            return self.__connection.send(data)

    def receive(self, size):
        if self.__connection:
            return self.__connection.receive(size)

    pass