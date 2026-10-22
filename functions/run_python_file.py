import os 
import subprocess
from pathlib import Path
def run_python_file(working_directory: str, file_path: str, arg: list[str] | None= None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory) 
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path)) 
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{Path(target_file).name}" does not exist or is not a regular file'
        if target_file[-3:] != ".py":
            return f'Error: "{Path(target_file).name}" is not a Python file'
        command = ["python" , target_file]
        if arg is not None :
            command.extend(arg)
        process_result = subprocess.run(command,text=True,timeout=30,stdout=True,stderr=True)
        result =""
        result += f'Process exited with code {process_result.returncode}\n'
        result += f'STDOUT: {process_result.stdout}\n' if process_result.stdout  else "STDOUT: No output produced\n"
        result += f'STDERR: {process_result.stderr}'  if process_result.stderr else "STDERR: No output produced"
        return result
    except Exception as e:
        return f'Error: executing Python file {e}'

