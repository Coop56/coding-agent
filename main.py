import argparse
import os
import sys

from dotenv import load_dotenv

from google import genai
from google.genai import types

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

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    print(response.text)

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")

if __name__ == "__main__":
    main()
