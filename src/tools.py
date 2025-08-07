import sys
import os
from pathlib import Path
import json
import argparse

STATE_FILE_NAME = ".state_file.json"

def load_last_state(src_dir):
    if os.path.exists(Path(src_dir).joinpath(STATE_FILE_NAME)):
        with open(Path(src_dir).joinpath(STATE_FILE_NAME), 'r') as f:
            return json.load(f)
    return None

def save_state(root_src_dir, backup_dir, dict_dirs, dict_files):
    root_dict = {
        'root_src_dir': root_src_dir,
        'backup_dir': backup_dir,
        'dict_dirs' : dict_dirs,
        'dict_files' : dict_files
    }
    with open(Path(root_src_dir).joinpath(STATE_FILE_NAME), 'w') as f:
        json.dump(root_dict, f, indent=2)

def check_last_state(root_src_dir, backup_dir, arg_backup_dir):
    if (Path(root_src_dir).resolve() == Path(os.getcwd()).resolve()):
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory")
    
    if (Path(backup_dir).resolve() == Path(arg_backup_dir).resolve()):
        return True
    
    return False

