import os
import argparse

from src.script import traverse_directory_tree
from src.tools import load_last_state, save_state, check_if_src_dir_contains_state_file, check_and_set_src_dir, check_and_set_backup_dir

# No cmd args
def sync():
    whole_dict = load_last_state(os.getcwd())

    dict_files = whole_dict['dict_files']
    dict_dirs = whole_dict['dict_dirs']
    src_dir = whole_dict['root_src_dir']
    backup_dir = whole_dict['backup_dir']

    r_dict_dirs, r_dict_files = traverse_directory_tree(src_dir, backup_dir, dict_dirs, dict_files)
    save_state(src_dir, backup_dir, r_dict_dirs, r_dict_files)

    print('State file was updated')
    print(f"Directory '{src_dir}' was successfully a backuped(just new changes, sync) to directory '{backup_dir}'")

def new_backup(args):
    src_dir = check_and_set_src_dir(args.new_backup[0])
    backup_dir = check_and_set_backup_dir(args.new_backup[1])

    if check_if_src_dir_contains_state_file(src_dir):
        raise argparse.ArgumentTypeError(f"This directory is already containing state file. Can not perform new backup. Read help.")

    print(f"Performing backup of new directory\n SRC DIR '{src_dir}' \n BACKUP DIR '{backup_dir}'")
    r_dict_dirs, r_dict_files = traverse_directory_tree(src_dir, backup_dir)
    save_state(src_dir, backup_dir, r_dict_dirs, r_dict_files)
    print('State file was created')
    print(f"Directory '{src_dir}' was successfully backuped to directory '{backup_dir}'")

def main_wrapped():
    parser = argparse.ArgumentParser(
        description="CLI app to backup directories and files",
        epilog='If want to perform backup(just synchronization) of directory which already has state file, call app withou any arguments.'
    )

    parser.add_argument("-v", action="store_true", help="Enable verbose output")
    parser.add_argument(
        '--new-backup',
        help="Specify directory to backup and directory where should it be backuped. " \
        "If you want to use current working directory as source, just type '.' as path. " \
        "Both paths must be absolute and valid if specified. " \
        "Backup directory must be empty.",
        nargs=2,
        metavar=("SRC_DIR", "BACKUP_DIR")
    )

    args = parser.parse_args()

    if args.new_backup is not None:  
        new_backup(args)
    else:
        sync()

if __name__ == "__main__":
    main_wrapped()
    

