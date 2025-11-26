import os

from config import MAX_FILE_CHARACTERS

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