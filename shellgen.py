#!/usr/bin/env python3
import sys
import os
from llama_cpp import Llama

# Get input either from argument or stdin
if not sys.stdin.isatty():
    # Input is piped
    user_input = sys.stdin.read().strip()
elif len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    print(f"Usage: {sys.argv[0]} <text to convert>")
    print("   or: echo '<text>' | python3 cmdgen.py")
    sys.exit(1)

# Path to your GGUF model
model_path = os.path.expanduser(
    "./models"
)

# Load model
llm = Llama(
    model_path=model_path,
    n_ctx=4096,
    n_threads=4
)

# System instruction
system_prompt = (
    "You are an AI that converts natural language into valid Linux shell commands. "
    "Respond ONLY with the command, no explanations, no extra text."
)

# Run the model
output = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ],
    max_tokens=128,
    temperature=0.0,  # deterministic output
)

# Extract AI response
command = output["choices"][0]["message"]["content"].strip().splitlines()[0]

# Print only the command, safe for piping into bash
print(command)

