<div align = center>


<img src="https://raw.githubusercontent.com/c137v8/ShellGen/refs/heads/main/Shellgen.png">

**ShellGen** is an AI-powered command-line assistant that converts natural language into valid shell commands — powered by a **local LLM** (no API keys, no cloud).  
It helps you write shell commands faster, safer, and more intuitively.
</div>
---

## ✨ Features

- 🧠 **Natural Language → Command**  
  Type what you want to do, and ShellGen generates the right command.

- 🔒 **Private and Offline**  
  Runs entirely on your machine using [llama.cpp](https://github.com/ggerganov/llama.cpp).

- ⚙️ **Shell Integration**  
  Works directly in Fish, Bash, or Zsh (customizable key bindings).

- 🧩 **Command Preview and Confirmation**  
  Lets you see what will run — and warns you about risky commands.

- 🚀 **Local Model Support**  
  Supports quantized `.gguf` Llama models for fast, low-RAM inference.

---

## 🧰 Installation

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

## ⚙️ Usage

### 🔹 Basic usage

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

### 🔹 Using stdin

```bash
echo "show disk usage" | shellgen
```

---

### 🔹 Auto-confirm execution

Add the `--no-confirm` flag to skip the confirmation prompt(For use with terminal key bindings):

```bash
shellgen "show current directory" --no-confirm
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

Now just type your natural language request and press **Ctrl+G** to turn it into a shell command ✨

---

## 🧩 Model setup

When run for the first time, ShellGen creates a configuration file at ~/.config/shellgen

Downloaded models are stored at:
```
~/.config/shellgen/models/
```


Alternatively, you can download models from:
- [TheBloke’s Hugging Face models](https://huggingface.co/TheBloke)
- [llama.cpp model zoo](https://huggingface.co/models?library=llama.cpp)

---

## 🛠️ Development

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

## 📜 License

MIT License © 2025 Ibrahim  
Feel free to contribute and enhance!

---

## 💡 Example Ideas

| Input | Output |
|-------|---------|
| "find all .py files in this folder" | `find . -name '*.py'` |
| "check disk usage in human readable format" | `du -h --max-depth=1` |
| "start a simple HTTP server" | `python3 -m http.server` |

---

## 🧠 Future Roadmap

- [ ] Fine tune custom models so its faster and better ;)

---

> 💬 *ShellGen*
