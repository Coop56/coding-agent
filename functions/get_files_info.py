import os

from google.genai import types

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

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    if (directory == "."):
        files_string = "Result for current directory:\n"
    else:
        files_string = f"Result for directory '{directory}':\n"

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        files_string = files_string + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return files_string

    if not os.path.isdir(full_path):
        files_string = files_string + f'    Error: The directory "{directory}" does not exist.'
        return files_string

    for item in os.listdir(full_path):
        file_name = os.path.join(full_path, item)
        file_size = os.path.getsize(file_name)
        is_dir = os.path.isdir(file_name)
        files_string = files_string + (f'  - {item}: file_size={file_size} bytes, is_dir={is_dir}\n')

    return files_string