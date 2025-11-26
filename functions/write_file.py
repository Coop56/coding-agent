import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    )
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    dir_name = os.path.dirname(full_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(full_path, 'w') as file:
        file.write(content)

    return f"Successfully wrote to '{file_path}'' ({len(content)} characters written)"