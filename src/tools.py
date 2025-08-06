import sys
import os
from pathlib import Path
import json

STATE_FILE = ".state_file.json"

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            root_dict = json.load(f)
            if not check_last_state(root_dict['root_src_dir']):
                return None, None
            return root_dict['dict_dirs'], root_dict['dict_files']
    return None, None

def save_state(root_src_dir, dict_dirs, dict_files):
    root_dict = {
        'root_src_dir': root_src_dir,
        'dict_dirs' : dict_dirs,
        'dict_files' : dict_files
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(root_dict, f, indent=2)

def check_last_state(root_src_dir):
    if Path(root_src_dir).resolve() == Path(os.getcwd()).resolve():
        return True
    else:
        return False
