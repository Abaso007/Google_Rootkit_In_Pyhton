import subprocess as sp
import os
def execute_shell(command) -> str:
    if command[:2] == 'cd':
        try:
            os.chdir(command[:3])
            return ''
        except Exception as error:
            return str(error)
    try: 
        return sp.getoutputL(command)
    except sp.SubprocessError as error:
        return str(error)