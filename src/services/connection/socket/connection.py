import socket, pickle

class Connection:
    encode = 'utf-8'

    def __init__(self, **attrs):
        self.attrs = attrs

        self.__connection = attrs.get('connection')
        pass

    def __send_dict__(self, request):

        sent = None

        try:
            sent = self.__connection.sendall(pickle.dumps(request))
        except:
            print("excecao")
            pass

        return sent


    def send(self, request):
        if not self.__connection:
            return

        if isinstance(request, dict):
            return self.__send_dict__(request)
        else:
            return self.__send_dict__({
                'not_dict': True,
                'body': request, 
            })

        pass


    def receive(self, size=1024):
        if not self.__connection:
            return {}

        received = self.__connection.recv(size)
        response = pickle.loads(received)

        if response.get('not_dict'):
            return response.get('body')

        
        return response
    
    def close(self):
        self.__connection.close()