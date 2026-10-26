import os
import argparse
import json 
import sys
from config import MAX_ITERS
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

def generate_content(client: OpenAI , messages: list , verbose: bool) -> str| None:
    response = client.chat.completions.create(
            model="openrouter/free",
            messages= messages,
            tools=available_functions)

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print("Prompt tokens: ",response.usage.prompt_tokens)
        print("Response tokens: ",response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call,verbose)
        print(result_message)
        if not result_message.get("content"): 
            raise RuntimeError(f"Empty function response for: {tool_call.function.name}")
        if verbose :
            print(f"-> {result_message['content']}")
        messages.append(result_message)
    return None


def main() -> None:
        
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt",type=str ,help="User prompt")
    parser.add_argument("--verbose",action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("API-KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")
    
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
            ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client,messages,args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
        except Exception as e:
            print(f"Error in generating content: {e}")
    print(f"Maximum iterations {MAX_ITERS} reached")
    sys.exit(1)

if __name__ == "__main__":
    main()

