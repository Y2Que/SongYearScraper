
from pathlib import Path

songPath = Path('E:\Music')

def delete_trash_files(strInputPath):
    for file in strInputPath.iterdir():    # loop thru files in directory
        if not file.is_dir():              # do not act on folders
            if file.name.startswith("._"): # detect trash files
                file.unlink()              # DELETE
        else:
            delete_trash_files(file)       # recusive call for folders

delete_trash_files(songPath)