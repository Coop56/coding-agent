import os

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