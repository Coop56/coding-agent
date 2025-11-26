import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", file_path] + args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory,
        )

        output_string = f"STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}"

        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}.\n{output_string}"

        if completed_process.stdout == '':
            return f"No output produced."

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
