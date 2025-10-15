import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    work_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(work_path)
    abs_work = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_work):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(work_path):
        return f'Error: "{directory}" is not a directory'
    try:
        contents = os.listdir(work_path)
        output = []
        for content in contents:
            content_path = os.path.join(work_path, content)
            bytes = os.path.getsize(content_path)
            isdir = os.path.isdir(content_path)
            output.append(f' - {content}: file_size={bytes}, is_dir={isdir}')
        return "\n".join(output)
    except Exception as e:
        return f"Error listing files: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)