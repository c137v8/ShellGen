#!/usr/bin/env python3
import sys
import os
import subprocess
import contextlib
import configparser
from llama_cpp import Llama
from colorama import Fore, Style, init
from gpt4all import GPT4All
from . import setup

init(autoreset=True)

CONFIG_DIR = os.path.expanduser("~/.config/shellgen/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")


# -----------------------
#  CONFIG / MODEL HANDLING
# -----------------------
def load_model_name():
    """Load model name from config.ini. If missing or malformed, trigger setup.py."""

    # If config file doesn't exist -> run setup
    if not os.path.exists(CONFIG_FILE):
        print(f"{Fore.RED}ShellGen not configured. Launching setup...{Style.RESET_ALL}")
        setup.run_setup()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # If section OR key is missing -> run setup again
    if "shellgen" not in config or "model" not in config["shellgen"]:
        print(f"{Fore.RED}Invalid or corrupt config file. Relaunching setup...{Style.RESET_ALL}")
        os.system(f"{sys.executable} setup.py")
        config.read(CONFIG_FILE)

    return config["shellgen"]["model"]


MODEL_NAME = load_model_name()  # <-- ✅ assign the global model name


# -----------------------
#  UTILS
# -----------------------

@contextlib.contextmanager
def suppress_output():
    """Temporarily hide noisy llama-cpp logs."""
    with open(os.devnull, 'w') as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = devnull, devnull
            yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr


def clean_command(cmd):
    """Remove quotes or backticks from model output."""
    cmd = cmd.strip()
    if cmd.startswith(("`", '"', "'")) and cmd.endswith(("`", '"', "'")):
        cmd = cmd[1:-1].strip()
    return cmd


def download_model(model_path):
    """Download selected model from GPT4All."""
    print(f"{Fore.YELLOW}Downloading model {MODEL_NAME} ...{Style.RESET_ALL}")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # GPT4All downloads into directory path, not full file path
    GPT4All(MODEL_NAME, model_path=os.path.dirname(model_path))

    print(f"{Fore.GREEN}✅ Model downloaded:{Style.RESET_ALL} {model_path}")


# -----------------------
#  MAIN SHELLGEN LOGIC
# -----------------------

def main():
    # Get user input (supports pipe and arguments)
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        user_input = " ".join([a for a in sys.argv[1:] if a != "--no-confirm"])
    else:
        print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL} {sys.argv[0]} <text>")
        print(f"   or: echo 'text' | {sys.argv[0]}")
        sys.exit(1)

    model_path = os.path.expanduser(f"{CONFIG_DIR}/models/{MODEL_NAME}")

    if not os.path.exists(model_path):
        print(f"{Fore.RED}Model not found:{Style.RESET_ALL} {model_path}")
        download_model(model_path)

    # Load LLaMA model silently
    with suppress_output():
        llm = Llama(model_path=model_path, n_ctx=4096, n_threads=4)

    system_prompt = (
        "You convert natural language into valid Linux shell commands. "
        "Respond ONLY with the command, nothing else."
    )

    # Ask the model
    with suppress_output():
        output = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=128,
            temperature=0.0,
        )

    command = clean_command(output["choices"][0]["message"]["content"].strip().splitlines()[0])

    print(f"\n{Fore.CYAN}Input:{Style.RESET_ALL} {user_input}")
    print(f"{Fore.GREEN}Command:{Style.RESET_ALL} {command}\n")

    # Safety prompt for destructive commands
    risky = any(x in command.split() for x in ("rm", "mv", "chmod", "chown", "rmdir", "dd", "mkfs"))
    if risky:
        print(f"{Fore.RED}⚠️  WARNING: command modifies system files.{Style.RESET_ALL}\n")

    confirm = input(f"{Fore.YELLOW}Run this command? [Y/n]{Style.RESET_ALL} ").strip().lower()

    if confirm in ("", "y", "yes"):
        print(f"{Fore.GREEN}Executing...{Style.RESET_ALL}\n")
        subprocess.run(command, shell=True)
    else:
        print(f"{Fore.BLUE}Cancelled.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
