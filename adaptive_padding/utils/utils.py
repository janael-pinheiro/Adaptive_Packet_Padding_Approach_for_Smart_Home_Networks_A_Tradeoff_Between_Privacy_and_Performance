from os import makedirs
from os.path import exists, join
from datetime import datetime


def create_folder(folder_path: str) -> str:
    if exists(folder_path):
        raise FileExistsError(f"Folder {folder_path} exists.")
    makedirs(folder_path)
    return folder_path
