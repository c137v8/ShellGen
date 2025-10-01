# ShellGen

ShellGen is an offline, privacy-friendly Python utility that converts natural language instructions into valid Linux shell commands.

**Offline:** Once the model is downloaded, no internet connection is required.

**Privacy-friendly:** All inputs and commands stay on your machine; nothing is sent to external servers.

**Command-only output:** The AI responds only with the shell command, no explanations or extra text.

## Features

- Converts plain English instructions into Linux commands.
- Accepts input via command-line arguments or piped stdin.
- Automatically handles local models in a dedicated folder (`~/shellgen_models`).
- Prompts to download the default model if none exists.
- Deterministic outputs for consistent command generation.

## Requirements

- Python 3.11+
- `llama_cpp` Python package
