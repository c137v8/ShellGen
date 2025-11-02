#!/usr/bin/env python3
import sys
import os
import subprocess
import contextlib
import shlex
from llama_cpp import Llama
from colorama import Fore, Style, init

init(autoreset=True)

@contextlib.contextmanager
def suppress_output():
    """Temporarily suppress stdout and stderr."""
    with open(os.devnull, 'w') as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = devnull, devnull
            yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr


def clean_command(cmd):
    """Remove wrapping quotes or backticks, trim whitespace."""
    cmd = cmd.strip()
    if cmd.startswith(("`", '"', "'")) and cmd.endswith(("`", '"', "'")):
        cmd = cmd[1:-1].strip()
    return cmd


def main():
    # Input handling
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL} {sys.argv[0]} <text to convert>")
        print(f"   or: echo '<text>' | python3 {os.path.basename(sys.argv[0])}")
        sys.exit(1)

    # Model path
    model_path = os.path.expanduser("./models/Llama-3.2-3B-Instruct-IQ3_M.gguf")

    if not os.path.exists(model_path):
        print(f"{Fore.RED}Model not found at:{Style.RESET_ALL} {model_path}")
        print(f"{Fore.CYAN}Please download and place the model in ./models before continuing.{Style.RESET_ALL}")
        sys.exit(1)

    # Load model quietly
    with suppress_output():
        llm = Llama(model_path=model_path, n_ctx=4096, n_threads=4)

    # Prompt definition
    system_prompt = (
        "You are an AI that converts natural language into valid Linux shell commands. "
        "Respond ONLY with the command, no explanations, no extra text."
    )

    # Query model
    with suppress_output():
        output = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=128,
            temperature=0.0,
        )

    # Clean the AI output
    raw_command = output["choices"][0]["message"]["content"].strip().splitlines()[0]
    command = clean_command(raw_command)

    print(f"\n{Fore.CYAN}Input:{Style.RESET_ALL} {user_input}")
    print(f"{Fore.GREEN}Command:{Style.RESET_ALL} {command}\n")

    # Basic safety detection
    risky = any(x in command.split() for x in ("rm", "mv", "chmod", "chown", "rmdir", "dd", "mkfs"))
    if risky:
        print(f"{Fore.RED}⚠️  Warning:{Style.RESET_ALL} This command may alter or delete files.\n")

    confirm = input(f"{Fore.YELLOW}Run this command? [Y/n] {Style.RESET_ALL}").strip().lower()

    if confirm in ("", "y", "yes"):
        print(f"\n{Fore.GREEN}Executing...{Style.RESET_ALL}\n")
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Command failed with exit code {e.returncode}{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}Cancelled.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
