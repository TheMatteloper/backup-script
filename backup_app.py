import os
import argparse

from src.script import traverse_directory_tree
from src.tools import load_last_state, save_state

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Backup CLI app")

    parser.add_argument("-v", action="store_true", help="Enable verbose output")
    parser.add_argument("src_dir", nargs=1, help="Directory which to backup if not used current working directory will be backuped, path must be absolute")
    parser.add_argument("backup_dir", nargs=1, help="Directory where should be source dir backuped, path must be absolute")

    args = parser.parse_args()

    path = os.getcwd() if args.src_dir == None else args.src_dir

    dict_dirs, dict_files = load_last_state()
    if dict_dirs == None:
        r_dict_dirs, r_dict_files = traverse_directory_tree(path, argparse.backup_dir)
        save_state(os.getcwd(), r_dict_dirs, r_dict_files)
    else:
        r_dict_dirs, r_dict_files = traverse_directory_tree(os.getcwd(), argparse.backup_dir, dict_dirs, dict_files)
        save_state(os.getcwd(), r_dict_dirs, r_dict_files)