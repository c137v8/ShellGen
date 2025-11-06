#!/usr/bin/env python3
import os
import configparser
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_DIR = os.path.expanduser("~/.config/shellgen/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

MODELS = {
    "1": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
    "2": "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf",
    "3": "Phi-3-mini-4k-instruct.Q4_0.gguf",
    "4": "orca-mini-3b-gguf2-q4_0.gguf",
    "5": "gpt4all-13b-snoozy-q4_0.gguf"
}

def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def main():
    print(f"\n{Fore.CYAN}ShellGen Initial Setup")
    print(f"{Fore.WHITE}Select a model to use:\n")

    print(f"{Fore.YELLOW}Model Options:")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Meta-Llama-3-8B-Instruct (8B / 4.66GB / 8GB RAM required / Llama 3 License)")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Nous-Hermes-2-Mistral-7B-DPO (7B / 4.11GB / 8GB RAM / Apache 2.0)")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Phi-3-mini-4k-instruct (3.8B / 2.18GB / 4GB RAM / MIT) ✅ Recommended")
    print(f"{Fore.GREEN}4.{Style.RESET_ALL} orca-mini-3b (3B / 1.98GB / CC-BY-NC-SA-4.0)")
    print(f"{Fore.GREEN}5.{Style.RESET_ALL} GPT4All-13b-snoozy (13B / 7.37GB / 16GB RAM required)\n")

    choice = ""
    while choice not in MODELS:
        choice = input(f"{Fore.YELLOW}Enter model number (1-5): {Style.RESET_ALL}").strip()

    selected_model = MODELS[choice]
    ensure_config_dir()

    config = configparser.ConfigParser()
    config["shellgen"] = {"model": selected_model}

    with open(CONFIG_FILE, "w") as f:
        config.write(f)

    print(f"\n{Fore.GREEN}✅ Saved configuration to {CONFIG_FILE}")
    print(f"Selected model: {Fore.CYAN}{selected_model}{Style.RESET_ALL}\n")


def run_setup():
    return main()

