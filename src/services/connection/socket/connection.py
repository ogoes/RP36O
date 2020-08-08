import json, socket

class Connection:
    encode = 'utf-8'

    def __init__(self, **attrs):
        self.attrs = attrs

        self.__connection = attrs.get('connection')
        pass

    def __send_dict__(self, request):

        as_bytes = bytes('DefautMessage'.encode(Connection.encode))
        try:
            as_bytes = json.dumps(request).encode(Connection.encode)
        except json.decoder.JSONDecodeError:
            as_bytes = bytes('ERROR: not a dict request'.encode(Connection.encode))

        return self.__connection.sendall(as_bytes)


    def send(self, request):
        if not self.__connection:
            return

        if isinstance(request, dict):
            return self.__send_dict__(request)

        return self.__connection.sendall(request)


    def receive(self, size=1024, dict=False):
        if not self.__connection:
            return {}

        received = self.__connection.recv(size)

        if dict:
            try:
                received = json.loads(received.decode(Connection.encode))
            except json.decoder.JSONDecodeError:
                pass

        return received
    
    def close(self):
        self.__connection.close()