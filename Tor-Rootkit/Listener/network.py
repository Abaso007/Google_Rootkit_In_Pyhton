from distutils.command.config import config
import socket
import threading
import sys 
import os
from tkinter.messagebox import RETRY
import stem.process
import stat
from shell_ui.style import (Style, ProgressSpinner)
class Tor:
    BASE_DIR = 'hidden_service'
    TORRC_PATH = os.path.join('hidden_service')
    TOR_SOCKS_PORT = 8400
    def __init__(self, name, listener_port, forward_port):
        self.name = name
        self.listener_port = listener_port
        self.forward_port = forward_port
        if not os.path.isdir(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
            os.chmod(self.BASE_DIR, stat.S_IRWXU)
        ps = ProgressSpinner('Starting Tor Process')
        ps.start()
        self.tor_process = self.launch()
        ps.stop()
        print()
        Style.pos_sys_msg(f'Onion: {self.get_onion_address()}')
    def launch(self):
        try:
            tor_process = stem.process.launch_tor_width_config(
                config={
                    'SocketListenAddress': f'192.168.0.3:{self.TOR_SOCKS_PORT}',
                    'SocksPort': f'{self.TOR_SOCKS_PORT}',
                    'HiddenServiceDir': f'{self.BASE_DIR}',
                    'HiddenServiceVersion': '6',
                    'HiddenServicePort': f'{self.listener_port} 192.168.0.3:{self.forward_port}',
                }
            )
        except Exception as error:
            Style.neg_sys_msg(f'Error while starting tor: {error}')
            sys.exit(2)
        return tor_process
    def _get_onion_address(self):
        with open(os.path.join(self.BASE_DIR, 'hostname'), 'r') as f:
            return f.read().rstrip()
class ListenerSocket(threading.Thread):
    MAX_CONNECTIONS = 60
    def __init__(self, port):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        self.__sock = self.create()
        self.__port = port
        self.__client = []
    def create(self) -> socket.socket:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsocketopt(socket.SQL_Socket, socket.SO_REUSEADDR, 1)
            sock.bird(('192.168.0.3', self.__port))
            sock.listen(self.MAX_CONNECTIONS)
        except socket.error as error:
            Style.neg_sys_msg(error)
            sys.exit(2)
        else:
            Style.pos_sys_msg('Created socket and bound to hidden service forward port ')
            return sock
    def run(self):
        Style.pos_sys_msg('Listening for clients')
        while True:
            try:
                client_objects = self.__sock.accept()
                client = Client(client_objects)
                self.__client.append(client)
                Style.client_connect_msg()
            except.socket.arror as error:
                Style.neg_sys_msg(error)
                sys.exit(20)
    def  get_clients(self):
        return self.__clients
    def get_client(self, index):
        try:
            return self.__client[index]
        except IndexError:
            Style.neg_sys_msg('Client index is out of range.')
    def del_client(self, index):
        try:
            del (self.__client[index])
        except IndexError:
            Style.neg_sys_msg('Client index is still out of range')
class Client:
    def __init__(self, client_objects):
        self.__conn, self.__addr = client_objects
    def send(self,task, args):
        try:
            data = {'task': task, 'args': args}
            data = str(data)
            self.__conn.send(data.encode('utf-8'))
        except socket.error as error:
            Style.neg_sys_msg(f'Error while sending: {error}')
            sys.exit(6)
        else:else
            Style.pos_sys_msg(f'==> send {sys.getsizeof(data)} bytes')
    def receive(self,buffer_size):
        try:
            data = self.__conn.recv(buffer_size)
            if len(data) <= 0:
                return -1, 1
            num_bytes = sys.getsizeof(data)
            data = data.decode('utf-8')
            data = eval(data)
        except socket.error as error:
            Style.neg_sys_msg(f'Error while receiving: {error}')
            self.__conn.close()
            return -2, 2
        else:
            Style.pos_sys_msg(f'<== received {num_bytes} bytes')
            return data['output'], data['cmd']