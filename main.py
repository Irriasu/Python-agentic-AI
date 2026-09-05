import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


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
            {"role": "user", "content": args.user_prompt}
            ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages)
    if args.verbose:
        print("User prompt: ",args.user_prompt) 
        print("Prompt tokens: ",response.usage.prompt_tokens)
        if response.usage.completion_tokens is None:
            raise RuntimeError("Failed API request")
        else:
            print("Response tokens: ",response.usage.completion_tokens)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()

