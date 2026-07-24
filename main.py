"""
Automatic File Organizer

This program scans a selected directory, creates folders based on
file types (PDFs, Images, Videos, Audio, etc.), and moves each file
into its appropriate folder.
"""

import  os
import  shutil as su

# Folder to organize
SOURCE_FOLDER = r"F:\testing"

# Get a list of all files in the source folder
files = os.listdir(SOURCE_FOLDER)

# Move a file to the specified folder
def move_file(source_folder, filename, folder_path):
    su.move(
        src=os.path.join(source_folder, filename), 
        dst=os.path.join(folder_path, filename)
        )
    print(f"Moved {filename} to {folder_path}.")

FILE_CATEGORIES = {
    ".pdf": "PDFs",
    ".jpeg": "Images",
    ".png": "Images",
    ".jpg": "Images",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".docx": "Documents",
    ".txt": "Documents",
    ".zip": "Compressed",
    ".rar": "Compressed",
    ".exe": "Executables",
    ".xlsx": "Excel",
    ".csv": "Excel" 
}

for filename in files:
    file_extension = os.path.splitext(filename)[1]  # Get the file extension (name, extension) as a tuple and take the second element
    if file_extension in FILE_CATEGORIES:
        folder_name = FILE_CATEGORIES[file_extension]
        folder_path = os.path.join(SOURCE_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"Created folder: {folder_name}")
        move_file(SOURCE_FOLDER, filename, folder_path)

print("-----------File organization complete.-----------")