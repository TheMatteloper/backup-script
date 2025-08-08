# Backup App

## What is this?

This is a simple command-line tool to help you back up your files and folders from one place (the source) to another (the backup directory). It’s perfect if you want to keep a copy of your important stuff on another drive or location, and you want the backup to always match your source—new and changed files are copied over, and deleted files are removed from the backup.

**Note:**  
This app only syncs changes one way—from your source directory to your backup directory. It does not support restoring from backup or syncing changes back to the source.

---

## Use Cases

- Back up your documents, photos, or code to another drive or folder.
- Keep a mirror copy of a folder for safety.
- Quickly update your backup with only the files that changed.

---

## Why incremental backup?

After the initial backup, updating your backup is much faster because the app only propagates changes—new or modified files are copied, and deleted files are removed from the backup. This saves time and bandwidth compared to copying everything every time.

---

## How to Use

### 1. Initial Setup

Make sure you have Python 3.8+ installed.

Clone or copy this project to your computer.

### 2. Creating a New Backup

To back up a folder for the first time, use the `--new-backup` option:

```sh
python backup_app.py --new-backup SRC_DIR BACKUP_DIR
```

- `SRC_DIR`: The folder you want to back up. Use `.` for the current directory.
- `BACKUP_DIR`: The (empty) folder where your backup will go.

**Example:**

```sh
python backup_app.py --new-backup "E:/my_documents" "R:/backup/my_documents"
```

> The backup folder must be empty, and the source folder must not already have a `.state_file.json` file.

---

### 3. Updating Your Backup (Sync)

After the initial backup, just run the app from your source directory with no arguments:

```sh
python backup_app.py
```

This will:
- Copy new or changed files to the backup.
- Remove files from the backup if they were deleted from the source.
- Update the `.state_file.json` file to keep track of everything.

---

### 4. Extra Options

- `-v`: Enable verbose output (for more details).
- `--help`: Show help and usage info.

---

## Notes

- The `.state_file.json` file in your source folder tracks the backup state—don’t delete or edit it.
- The app only syncs from source to backup, not the other way around.
- Make sure your backup folder is accessible and has enough space.

---

**That’s it! Simple, fast, and keeps your backup up to date.**