import sys, os, shutil

# Path to desktop and documents
desktop_path = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
documents_path = os.path.join(os.path.join(os.path.expanduser("~")), "Documents")

# Storing all the files in desktop in a backup folder
backup_path = os.path.join(documents_path, "desktop_washer_backup")

"""Clears the specified folder in path

The function iterates through a folder and deletes the files or file 
(if specified) in it.

Keyword arguments:
path -- the path of the folder that contains the files to be deleted
arg -- to delete the specific file (default "*")
"""
def empty_folder(path, arg="*"):
    # Locally storing some important paths for optimization
    local_desktop_path = desktop_path
    local_backup_path = backup_path
    # Iterating through a list of items on desktop
    items = os.listdir(path)
    for item in items:
        item_path = os.path.join(path, item)
        # Permanently deleting file in backup
        if path == local_backup_path:
            # Delete file
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            # Delete folder
            elif os.path.isdir(item_path) and arg == "*":
                shutil.rmtree(item_path)
        # Delete only the non-hidden files
        elif not item.startswith("."):
            # arg = "*" deletes all files on desktop and stores them in backup folder
            if os.path.isfile(item_path) or os.path.islink(item_path):
                if arg == "*":
                    os.system(f"cp {local_desktop_path}/'{item}' {local_backup_path}")
                    os.unlink(item_path)
                # To delete a specific file
                elif arg != "*" and item == arg:
                    os.system(f"cp {local_desktop_path}/'{item}' {local_backup_path}")
                    os.unlink(item_path)
            # Delete folder
            elif os.path.isdir(item_path):
                # To delete all folders
                if arg == "*":
                    os.system(f"cp -R {local_desktop_path}/'{item}' {local_backup_path}")
                    shutil.rmtree(item_path)
                # To delete a specific folder
                elif arg != "*" and item == arg:
                    os.system(f"cp -R {local_desktop_path}/'{item}' {local_backup_path}")
                    shutil.rmtree(item_path)

# Creating the directory if it doesn't exist to avoid errors.
if not os.path.exists(backup_path):
    os.mkdir(backup_path)

# Counting the number of hidden files to avoid deleting them.
hidden_files_desktop = 0
for item in os.listdir(desktop_path):
    item_path = os.path.join(desktop_path, item)
    if item.startswith("."):
        hidden_files_desktop += 1

# Saving the files/ directories in desktop to the backup folder.
if (len(os.listdir(desktop_path)) > hidden_files_desktop):
    # Checking if a file to delete is specified
    if len(sys.argv) > 1:
        empty_folder(desktop_path, sys.argv[1])
    else:
        empty_folder(desktop_path)
    
# Deleting the files from the back up folder
sys.stdout.write("Enter Y/N to delete/keep files from backup folder: ")
sys.stdout.flush()
response = sys.stdin.readline().upper()
if response.rstrip() == "Y":
    empty_folder(backup_path)