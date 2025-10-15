import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    work_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(work_path)
    abs_work = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_work):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(work_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(work_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(abs_path) > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error getting file contents: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will be read, relative to the working directory. This is required by the function.",
            ),
        },
    ),
)