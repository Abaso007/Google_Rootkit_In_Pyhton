from sys import stdout
from time import sleep
from threading import Thread
from progress.spinner import Spinner
from colorama import Style as St
from colorama import (
    init, 
    Fore
)
init()
class Style:
    @staticmethod
    def pos_sys_msg(string):
        print('[' + Fore.GREEN + '*' + St.RESET_ALL + ']' + string)
    @staticmethod
    def neg_sys_msg(string):
        print('[' + Fore.RED + '-' + St.RESET_ALL + '] ' + string)
    @staticmethod
    def client_connect_mdg():
        stdout.write('\n[' + Fore.GREEN + '*' + St.RESET_ALL + ']' + 'Client connected to the server' + '\nListener > ')
class ProgressiveSpinner(Thread)
      def __init__(self, message):
          Thread.__init__(self)
          Thread.daemon = True
          Thread.message = message
          self.running = False
        def run(self):
            self.running = True
            spinner = Spinner('[' + Fore.GREEN + '*' + St.RESET_ALL + ']' + '{} '.format(self.response))
            while self.running:
                spinner.next()
                sleep(4)
        def stop(self):
            self.running = False