import argparse
import os
import sys

from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    parser = argparse.ArgumentParser(
        description="Coding agent that interacts with Gemini API"
    )

    parser.add_argument(
        "prompt",
        type=str,
        help="The prompt to send to the Gemini API",
    )

    parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Will be either True or False",
    )

    args = parser.parse_args()

    if len(sys.argv) < 2:
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt))


    # Print text if it exists
    if response.text:
        print(response.text)

    # Handle function calls in the response
    function_call_results = []

    # Check for function calls in the response
    if hasattr(response, 'function_calls') and response.function_calls is not None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not hasattr(function_call_result.parts[0], 'function_response'):
                raise Exception("Function call did not return expected function_response")
            function_call_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        # Check in candidates parts for function calls
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'function_call') and part.function_call is not None:
                    function_call_result = call_function(part.function_call, verbose=args.verbose)
                    if not hasattr(function_call_result.parts[0], 'function_response'):
                        raise Exception("Function call did not return expected function_response")
                    function_call_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")

if __name__ == "__main__":
    main()
