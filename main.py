import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from call_function import available_functions, call_function

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("Leah's AI Agent for BootDev")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)    

    user_prompt = " ".join(args)

    if verbose: #--verbose command line argument
        print(f"User prompt: {user_prompt}\n")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],
            system_instruction=SYSTEM_PROMPT),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response: ")
    if not response.function_calls:
        return response.text

    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if not result.parts[0].function_response.response:
            raise Exception("Error: fatal exception in response to function call - no response.")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        return result


if __name__ == "__main__":
    main()





