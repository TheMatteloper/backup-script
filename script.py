import os
import json
import shutil
from pathlib import Path

STATE_FILE = "file_state.json"

# Directories to backup
DIRECTORIES = ["E:/", "I:/foto/"]

BACKUP_DIR = Path("R:/backup/")

def get_file_state(path):
    stat = os.stat(path)
    return {'mtime': stat.st_mtime, 'size': stat.st_size}

def traverse_directory(sdir, last_state = None):
    sdir = Path(dir).resolve()
    
    for root, dirs, files in os.walk(sdir):
        # Create directories
        for dir in dirs:
            # Strip top directories and replace them with BACKUP_DIR
            new_dir = BACKUP_DIR.joinpath(*Path(os.path.join(root, dir)).parts[len(sdir.parts) - 1:])
            new_dir.mkdir(parents=True, exist_ok=True)

        # Copy files
        for file in files:
            # Copies files to BACKUP_DIR while preserving directory tree(preserved tree starts from the deepest specified folder)
            shutil.copy2(os.path.join(root, file), BACKUP_DIR.joinpath(*Path(os.path.join(root, file)).parts[len(sdir.parts) - 1:]))
        
        

def load_old_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def detect_changes(base_dir):
    old_state = load_old_state()
    new_state = scan_directory(base_dir)
    changed = []

    for path, meta in new_state.items():
        if path not in old_state or old_state[path] != meta:
            changed.append(path)

    deleted = [p for p in old_state if p not in new_state]
    save_state(new_state)

    return changed, deleted

# TODO on first backup save info about files and directories(last_state)
# TODO when last_state is available, backup only new changes
# (files new/modified, dirs new, modified dir structure, relocate files, delete relocated files in backup)

if __name__ == "__main__":
    traverse_directory("E:/Ostatní/KAJ/")
    print("done")
