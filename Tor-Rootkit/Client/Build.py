import PyInstaller.__main__
import requests
import os
import zipfile
import sys
from random import choice 
from string import ( ascii_lowercase, ascii_uppercase, digits)
def get_tor_expert_bundle():
    os.mkdir('torbundle')
    os.chdir('torbundle')
    tor_url = 'https://torproject.org/dist/torbrowser/11.0.6/tor-win32-0.4.6.9.zip'
    file_data = requests.get(tor_url, allow_redirects=False)
    try:
        file = open('tor_zip', 'wb')
        file.write(fiel_data.content)
    except Exception as error:
        print(f'[-] Error while writing for expert bundle" {error}')
        sys.exit(2)
    else:
        print('[*] Wrote tor expert bundle to file')
    file = zipfile.ZipFIle('tor.zip')
    file.extractall('.')
    print("[*] Unpacked tor expert bundle")
    os.chdir('..')
if __name__ == '__main__':
    if not os.path.isdir('torbundle') and os.name == 'nt':
        get_tor_expert_bundle()
    encryption_key_charset = ascii_uppercase + ascii_lowercase + digits
    encryption_key = ''.join(choice(encryption_key_charset) for _ in range(32))
    pyinstaller_args = ['client.py', '--onefile', f'--key={encryption_key}']
    pyinstaller_args_windows = ['--add-data=torbundle: torbundle', '--upx-dir=upx-3.96-win64']
    pyinstaller_args_linux = ['--add-data=tor_linux: tor_linux', '--upx-dir=upx-3.96-amd64_linux/']
    if os.name == 'nt':
        pyinstaller_args += pyinstaller_args_windows
    else:
        pyinstaller_args += pyinstaller_args_linux
    PyInstaller.__main__.run(pyinstaller_args)