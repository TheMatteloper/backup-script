import os
import shutil
from pathlib import Path

from src.tools import STATE_FILE_NAME

def get_file_state(path):
    stat = os.stat(path)
    return {'mtime': stat.st_mtime, 'size': stat.st_size, 'matched': False}

def compare_mtime(new, old):
    if new == old:
        return True
    else:
        return False

def synchronize_dirs_on_level(root, bdir, dirs, sdir, last_state, dict_dirs):
    # Traverse all directories at this level
    for dir in dirs:
        # Make new record
        relative_path = str(Path(*Path(os.path.join(root, dir)).parts[len(sdir.parts) - 1:]).as_posix())
        dict_dirs[relative_path] = False

        # Strip top directories and replace them with BACKUP_DIR
        new_dir = bdir.joinpath(*Path(os.path.join(root, dir)).parts[len(sdir.parts) - 1:])
        if last_state is None:
            new_dir.mkdir(parents=True, exist_ok=True)
        else:
            if relative_path not in last_state:
                new_dir.mkdir(parents=True, exist_ok=True)
            else:
                last_state[relative_path] = True

def synchronize_files_on_level(root, bdir, files, sdir, last_state, dict_files):
    # Traverse all files at this level
    for file in files:
        if file == STATE_FILE_NAME:
            continue
        path = Path(os.path.join(root, file))
        # Make new record
        relative_path = str(Path(*path.parts[len(sdir.parts) - 1:]).as_posix())
        dict_files[relative_path] = get_file_state(path)

        # Strip top directories and replace them with BACKUP_DIR
        copy_dst = bdir.joinpath(*path.parts[len(sdir.parts) - 1:])
        if last_state is None:
            shutil.copy2(path, copy_dst)
        else:
            if relative_path not in last_state:
                shutil.copy2(path, copy_dst)
            else:
                last_state[relative_path]['matched'] = True
                if not compare_mtime(dict_files[relative_path]['mtime'], last_state[relative_path]['mtime']):
                    shutil.copy2(path, copy_dst)

def traverse_directory_tree(sdir, bdir, last_state_dirs = None, last_state_files = None):
    sdir = Path(sdir).resolve()
    bdir = Path(bdir)
    dict_dirs = {}
    dict_files = {}
    for root, dirs, files in os.walk(sdir):
        synchronize_dirs_on_level(root, bdir, dirs, sdir, last_state_dirs, dict_dirs)
        synchronize_files_on_level(root, bdir, files, sdir, last_state_files, dict_files)

    delete_old_files(last_state_files, bdir)
    delete_old_directories(last_state_dirs, bdir)

    return dict_dirs, dict_files

def delete_old_files(last_state_files, bdir):
    # Delete old files in backup
    if last_state_files is not None:
        for key in last_state_files:
            if last_state_files[key]['matched'] is False:
                try:
                    os.remove(bdir.joinpath(Path(key)))
                except FileNotFoundError:
                    pass

def delete_old_directories(last_state_dirs, bdir):
    # Delete old directories in backup
    if last_state_dirs is not None:
        for key in last_state_dirs:
            if last_state_dirs[key] is False:
                shutil.rmtree(bdir.joinpath(Path(key)), ignore_errors=True)