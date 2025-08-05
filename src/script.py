import os
import json
import shutil
from pathlib import Path

STATE_FILE = "file_state"

# Directories to backup
DIRECTORIES = ["E:/", "I:/foto/"]

BACKUP_DIR = Path("R:/backup/")

def get_file_state(path):
    stat = os.stat(path)
    return {'mtime': stat.st_mtime, 'size': stat.st_size, 'matched': False}

def compare_mtime(new, old):
    if new == old:
        return True
    else:
        return False

def synchronize_dirs_on_level(root, dirs, sdir, last_state, dict_dirs):
    # Traverse all directories at this level
    for dir in dirs:
        # Make new record
        relative_path = str(Path(*Path(os.path.join(root, dir)).parts[len(sdir.parts) - 1:]).as_posix())
        dict_dirs[relative_path] = False

        # Strip top directories and replace them with BACKUP_DIR
        new_dir = BACKUP_DIR.joinpath(*Path(os.path.join(root, dir)).parts[len(sdir.parts) - 1:])
        if last_state is None:
            new_dir.mkdir(parents=True, exist_ok=True)
        else:
            if relative_path not in last_state:
                new_dir.mkdir(parents=True, exist_ok=True)
            else:
                last_state[relative_path] = True

def synchronize_files_on_level(root, files, sdir, last_state, dict_files):
    # Traverse all files at this level
    for file in files:
        path = Path(os.path.join(root, file))
        # Make new record
        relative_path = str(Path(*path.parts[len(sdir.parts) - 1:]).as_posix())
        dict_files[relative_path] = get_file_state(path)

        # Strip top directories and replace them with BACKUP_DIR
        copy_dst = BACKUP_DIR.joinpath(*path.parts[len(sdir.parts) - 1:])
        if last_state is None:
            shutil.copy2(path, copy_dst)
        else:
            if relative_path not in last_state:
                shutil.copy2(path, copy_dst)
            else:
                last_state[relative_path]['matched'] = True
                if not compare_mtime(dict_files[relative_path]['mtime'], last_state[relative_path]['mtime']):
                    shutil.copy2(path, copy_dst)

def traverse_directory_tree(sdir, last_state_dirs = None, last_state_files = None):
    sdir = Path(sdir).resolve()
    dict_dirs = {}
    dict_files = {}
    for root, dirs, files in os.walk(sdir):
        synchronize_dirs_on_level(root, dirs, sdir, last_state_dirs, dict_dirs)
        synchronize_files_on_level(root, files, sdir, last_state_files, dict_files)

    delete_old_files(last_state_files)
    delete_old_directories(last_state_dirs)

    return dict_dirs, dict_files

def delete_old_files(last_state_files):
    # Delete old files in backup
    if last_state_files is not None:
        for key in last_state_files:
            if last_state_files[key]['matched'] is False:
                print(str(BACKUP_DIR.joinpath(Path(key))) + ' removed')
                os.remove(BACKUP_DIR.joinpath(Path(key)))

def delete_old_directories(last_state_dirs):
    # Delete old directories in backup
    if last_state_dirs is not None:
        for key in last_state_dirs:
            if last_state_dirs[key] is False:
                print(str(BACKUP_DIR.joinpath(Path(key))) + ' removed')
                shutil.rmtree(BACKUP_DIR.joinpath(Path(key)), ignore_errors=True)
        

def load_last_state(name):
    if os.path.exists(STATE_FILE + name + '.json'):
        with open(STATE_FILE + name + '.json', 'r') as f:
            return json.load(f)
    return None

def save_state(state, name):
    with open(STATE_FILE + name + '.json', 'w') as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    dict_dirs, dict_files = traverse_directory_tree("E:/Ostatní/KAJ/", load_last_state('_dirs'), load_last_state('_files'))
    save_state(dict_dirs, '_dirs')
    save_state(dict_files, '_files')
