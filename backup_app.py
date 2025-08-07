import os
import argparse

from src.script import traverse_directory_tree
from src.tools import load_last_state, save_state, check_last_state

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Backup CLI app")

    parser.add_argument("-v", action="store_true", help="Enable verbose output")
    parser.add_argument(
        '--src_dir',
        default=os.getcwd(),  # default to current working directory
        help='Path to a directory (optional). Defaults to current working directory.'
    )
    parser.add_argument("backup_dir", help="Directory where should be source dir backuped, path must be absolute")

    args = parser.parse_args()

    whole_dict = load_last_state(args.src_dir)
    
    # New dir to backup
    if whole_dict == None:
        r_dict_dirs, r_dict_files = traverse_directory_tree(args.src_dir, args.backup_dir)
        save_state(args.src_dir, args.backup_dir, r_dict_dirs, r_dict_files)
    else:
        # Just sync
        check_last_state(whole_dict['root_src_dir'], whole_dict['backup_dir'], args.backup_dir)
        dict_files = whole_dict['dict_files']
        dict_dirs = whole_dict['dict_dirs']
        r_dict_dirs, r_dict_files = traverse_directory_tree(args.src_dir, args.backup_dir, dict_dirs, dict_files)
        save_state(args.src_dir, args.backup_dir, r_dict_dirs, r_dict_files)