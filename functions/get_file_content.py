import os

from google.genai import types

from config import MAX_FILE_CHARACTERS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        }
    )
)

def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(full_path, 'r') as file:
        content = file.read(MAX_FILE_CHARACTERS)

    if len(content) >= MAX_FILE_CHARACTERS:
        content += f"[...File '{file_path}' truncated at 10000 characters]"

    return content