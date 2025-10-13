import os

def write_file(working_directory, file_path, content):
    work_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(work_path)
    abs_work = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_work):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(work_path):
            os.makedirs(work_path)
        with open(work_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file contents: {e}"