from openai import OpenAI

import os
import tiktoken
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
import readline

def start():
    # Enable arrow key editing in input()
    readline.parse_and_bind("bind ^[[A ed-prev-line")  # Up arrow
    readline.parse_and_bind("bind ^[[B ed-next-line")  # Down arrow
    readline.parse_and_bind("bind ^[[C ed-next-char")  # Right arrow
    readline.parse_and_bind("bind ^[[D ed-prev-char")  # Left arrow
    print("Loading...")
    
    code_theme = os.getenv("BCLIGPT_CODE_THEME", "monokai")
    model = os.getenv("BCLIGPT_MODEL", "gpt-3.5-turbo")
    messages  = [
            {"role": "system", "content": "Your are an helpful coding assistant. You write responses in markdown. In code blocks, always add the language of the code to enable syntax highlighting. For code blocks containing commands, always add bash as a language near the ``` mark, like this: ```bash"},
        ]

    message_database = []
    encoding = tiktoken.encoding_for_model(model)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.chat.completions.create(
        model=model,
        messages=messages
        )

    tokens = 0
    console = Console()
    cost = 0.00
    while True:
        message = input(f"(Spent: ${'{:.2f}'.format(cost)}) (Tokens: {tokens}) - You: ")
        message_token_count = len(encoding.encode(message))
        tokens += message_token_count
        while tokens > 3500:
            popped_message = messages.pop(1)
            tokens -= len(encoding.encode(popped_message["content"]))
        messages.append({"role": "user", "content": message})

        try:
            result = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
                )
            full_content = ''
            new_lines = 0
            with Live(console=console, refresh_per_second=10) as live:
                for chunk in result:
                    # get "finish_reason" from delta, otherwise return None
                    if chunk.choices[0].finish_reason == "stop":
                        break
                    content = chunk.choices[0].delta.content
                    full_content += content
                    md = Markdown(full_content, code_theme=code_theme)
                    live.update(md)
            message_token_count = len(encoding.encode(full_content))
            tokens += message_token_count
            messages.append({"role": "assistant", "content": full_content})
            cost += tokens * 0.002 / 1000
        except Exception as e:
            print("Error: ", e)
            while tokens > 3500:
                popped_message = messages.pop(1)
                tokens -= len(encoding.encode(popped_message["content"]))
