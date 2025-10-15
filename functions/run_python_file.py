import subprocess
import os
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    work_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(work_path)
    abs_work = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_work):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(work_path):
        return f'Error: File "{file_path}" not found.'
    if not work_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        cmd = ["python3", str(abs_path)]
        if args:
            cmd.extend(args)
        output = subprocess.run(cmd, cwd=abs_work, timeout=30, capture_output=True, text=True)
        if output.stdout != "" or output.stderr != "":
            output_str = f'STDOUT: {output.stdout}\n' + f'STDERR: {output.stderr}'
        else:
            output_str = "No output produced"
        if output.returncode != 0:
            output_str += f'Process exited with code {output.returncode}\n'
        return output_str
    except Exception as e:
        return f"Error executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file at the specificed path with optional arguments, constrained to the working directory. Returns the STDOUT and STDERR if available, otherwise confirms no output was produced.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file, relative to the working directory. Required by the function.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of optional arguments passed to the python file. If excluded, an empty list is provided instead.",
            ),
        },
    ),
)