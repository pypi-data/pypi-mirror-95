import os, sys

if not __package__:
    sys.path[0] = sys.path[0][:sys.path[0].rfind("/")]

import wandbox

def main():
    try:
        wandbox.main()
    except Exception as e:
        print(f"Error:\n{e}")

