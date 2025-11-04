# 🐚 ShellGen

**ShellGen** is an AI-powered command-line assistant that converts natural language into valid shell commands — powered by a **local LLM** (no API keys, no cloud).  
It helps you write shell commands faster, safer, and more intuitively.

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
git clone https://github.com/yourusername/ShellGen.git
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

Add the `--no-confirm` flag to skip the confirmation prompt:

```bash
shellgen "show current directory" --no-confirm
```

---

## 🐟 Fish Shell Integration

You can bind ShellGen to a keyboard shortcut (e.g., `Ctrl+G`) to generate commands inline.

Example function (`~/.config/fish/functions/ai_command.fish`):

```fish
function ai_command
    set input (commandline)
    set tmpfile (mktemp)
    echo "[AI] Generating command..." >&2

    bash -c "echo "$input" | shellgen --no-confirm > '$tmpfile'" &
    set pid $last_pid

    # Spinner animation
    set spin_chars "/ - \\ |"
    while kill -0 $pid 2>/dev/null
        for c in $spin_chars
            printf "\r[AI] Generating command... %s" $c >&2
            sleep 0.1
        end
    end

    set output (cat $tmpfile)
    rm $tmpfile
    printf "\r\033[K" >&2
    commandline -r $output
    commandline -f repaint
end

bind \cg ai_command
```

Now just type your natural language request and press **Ctrl+G** to turn it into a shell command ✨

---

## 🧩 Model Configuration

By default, ShellGen looks for your model at:

```
~/.aimodels/Llama-3.2-3B-Instruct-IQ3_M.gguf
```

You can change this in your config or environment variable (coming soon).

You can download models from:
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

MIT License © 2025 [Your Name]  
Feel free to fork, contribute, and enhance!

---

## 💡 Example Ideas

| Input | Output |
|-------|---------|
| "find all .py files in this folder" | `find . -name '*.py'` |
| "check disk usage in human readable format" | `du -h --max-depth=1` |
| "start a simple HTTP server" | `python3 -m http.server` |

---

## 🧠 Future Roadmap

- [ ] Bash/Zsh keybinding helpers  
- [ ] Custom model path configuration  
- [ ] Inline suggestions  
- [ ] Risk scoring (for destructive commands)  
- [ ] Streamed LLM responses  

---

> 💬 *ShellGen helps you command your terminal the way you think — not the way the shell does.*
