import sys
import os
from pathlib import Path
import json
import argparse

STATE_FILE_NAME = ".state_file.json"

def check_if_src_dir_contains_state_file(src_dir):
    if os.path.exists(Path(src_dir).joinpath(STATE_FILE_NAME)):
        return True
    return False

def load_last_state(src_dir):
    if os.path.exists(Path(src_dir).joinpath(STATE_FILE_NAME)):
        with open(Path(src_dir).joinpath(STATE_FILE_NAME), 'r') as f:
            return json.load(f)
    raise argparse.ArgumentTypeError(f"This directory is not containing state file. You have to use --new-backup switch to backup this dir.")

def save_state(root_src_dir, backup_dir, dict_dirs, dict_files):
    root_dict = {
        'root_src_dir': root_src_dir,
        'backup_dir': backup_dir,
        'dict_dirs' : dict_dirs,
        'dict_files' : dict_files
    }
    with open(Path(root_src_dir).joinpath(STATE_FILE_NAME), 'w') as f:
        json.dump(root_dict, f, indent=2)

def check_last_state(root_src_dir, backup_dir, arg_src_dir, arg_backup_dir):
    if (Path(root_src_dir).resolve() != Path(arg_src_dir).resolve()):
        raise argparse.ArgumentTypeError(f"Src directory'{arg_src_dir}' is not matched with scr directory specified in state file")
    
    if (Path(backup_dir).resolve() != Path(arg_backup_dir).resolve()):
        raise argparse.ArgumentTypeError(f"Backip directory'{arg_backup_dir}' is not matched with backup directory specified in state file")


def check_and_set_src_dir(arg_src_dir):
    if arg_src_dir == '.': 
        return os.getcwd()
    
    if not os.path.exists(arg_src_dir):
        raise argparse.ArgumentTypeError(f"'{arg_src_dir}' is not a valid src directory: directory must exist")

    return arg_src_dir  

def check_and_set_backup_dir(arg_backup_dir):
    if os.path.exists(arg_backup_dir):
        return arg_backup_dir
    else:
        raise argparse.ArgumentTypeError(f"'{arg_backup_dir}' is not a valid backup directory: directory must exists and must be empty")