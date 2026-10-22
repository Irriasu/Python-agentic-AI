import os 

from config import MAX_CHARS
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory) 
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path)) 
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: File not found or is not a regurlr file: "{target_file}"'
        with open(target_file,"r") as f :
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content        
    except Exception as e:
        return f'Error: reading file "{target_file}": {e}'

