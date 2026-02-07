<div align = center>


<img src="https://raw.githubusercontent.com/c137v8/ShellGen/refs/heads/main/Shellgen.png">

**ShellGen** is an AI-powered command-line assistant that converts natural language into valid shell commands. Powered by a **local LLM**

</div>

##  Features

- Type what you want to do, and ShellGen generates the right command.
- Runs entirely on your machine using [llama.cpp](https://github.com/ggerganov/llama.cpp).
- Works best with key binding(See Scripts).

---

##  Installation

### From PyPI (recommended)
Once published, you’ll be able to install ShellGen via pip:

```bash
pip install shellgen
```

### From source (local development)
If you’re developing or testing locally:

```bash
git clone https://github.com/c137v8/ShellGen.git
cd ShellGen
pip install -e .
```

This installs `shellgen` as a terminal command in your environment.

---

##  Usage

###  Basic usage

You can run ShellGen directly from the terminal:

```bash
shellgen "list all files in current directory"
```

Output:
```
Input: list all files in current directory
Command: ls -la
Run this command? [Y/n]
```

---

## Shell Integration

You can bind ShellGen to a keyboard shortcut (e.g., `Ctrl+G`) to generate commands inline.

To bind keys run the following command:

For bash/zsh:
```bash
source ./scripts/ai_command.sh
```

For fish:
```fish
source ./script/ai_command.fish
```

Now just type your natural language request and press **Ctrl+G** to turn it into a shell command 

---

##  Model setup

When run for the first time, ShellGen creates a configuration file at ~/.config/shellgen
Downloaded models are stored at:
```
~/.config/shellgen/models/
```

##  Development

### Setup environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Run tests
```bash
pytest
```

### Build package
```bash
python -m build
```

---

##  Autur 
Ibrahim Umran Parray 

---

##  Example Ideas

| Input | Output |
|-------|---------|
| "find all .py files in this folder" | `find . -name '*.py'` |
| "check disk usage in human readable format" | `du -h --max-depth=1` |
| "start a simple HTTP server" | `python3 -m http.server` |

---
