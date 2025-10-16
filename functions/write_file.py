import os
from google.genai import types

def write_file(working_directory, file_path, content):
    work_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(work_path)
    abs_work = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_work):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        try:
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(abs_path) and os.path.isdir(abs_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(work_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file contents: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to a file at the specified path, constrained to the working directory. Returns a message confirming success when there are no errors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the target file that the contents will be written to. Requried by the function.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content as a string that will be written to the file. Requried by the function.",
            ),
        },
    ),
)