from .config import read_config, create_default_config

import sys
import subprocess

def main():
    config = read_config()
    jrnl_folder = config.get("jrnl_folder")

    args = sys.argv[1:]
    if args:
        if args[0] == "--start":
            create_default_config()
            return

        if args[0] == "git":
            args.pop(0)
    p = subprocess.run(["git"] + args, cwd=jrnl_folder)
    return 

