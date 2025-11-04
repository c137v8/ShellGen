#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

def install():
    home = Path.home()
    shell = os.path.basename(os.environ.get("SHELL", "bash"))
    src_dir = Path(__file__).parent / "assets"
    user_bin = Path.home() / ".shellgen"

    user_bin.mkdir(exist_ok=True)

    if shell == "fish":
        dest = Path.home() / ".config/fish/functions/ai_command.fish"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src_dir / "ai_command.fish", dest)
        print("✅ Installed for Fish shell (Ctrl+X Ctrl+T to activate).")
    elif shell in {"bash", "zsh"}:
        dest = user_bin / "ai_command.sh"
        shutil.copy(src_dir / "ai_command.sh", dest)
        for rc in [".bashrc", ".zshrc"]:
            rc_path = home / rc
            if rc_path.exists():
                with open(rc_path, "a") as f:
                    f.write(f"\n# Added by ShellGen\nsource {dest}\n")
        print(f"✅ Installed for {shell} (Ctrl+X Ctrl+T to activate).")
    else:
        print(f"⚠️ Unsupported shell: {shell}")

    print("🎉 ShellGen is ready! Type something and press Ctrl+X Ctrl+T.")

def uninstall():
    """Removes ShellGen bindings."""
    home = Path.home()
    files = [
        home / ".shellgen/ai_command.sh",
        home / ".config/fish/functions/ai_command.fish",
    ]
    for f in files:
        if f.exists():
            f.unlink()
    print("🧹 ShellGen uninstalled.")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["setup", "uninstall"], help="Install or remove ShellGen integration.")
    args = parser.parse_args()
    if args.action == "setup":
        install()
    else:
        uninstall()

if __name__ == "__main__":
    main()
