"""
Automatic File Organizer

This program scans a selected directory, creates folders based on
file types (PDFs, Images, Videos, Audio, etc.), and moves each file
into its appropriate folder.
"""

import  os
import  shutil as su

# Folder to organize
SOURCE_FOLDER = input("Enter the path of the folder to organize: ")

# Get a list of all files in the source folder
files = os.listdir(SOURCE_FOLDER)

# Track file statistics
scanned_folders = 0  # Number of folders found
scanned_files = 0  # Number of files found
moved_files = 0    # Files successfully organized
skipped_files = 0  # Files that were not organized due to unrecognized extensions

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

# Iterate through each file in the source folder
for filename in files:

    # Skip hidden files and temporary files (starting with '.' or '~')
    if filename.startswith('.') or filename.startswith('~'):
        continue

    # Check if the item is a directory or a file
    if os.path.isdir(os.path.join(SOURCE_FOLDER, filename)):
        scanned_folders += 1
        # Skip directories, we only want to organize files
        continue    
    else:   
        scanned_files += 1

    # splitext() returns (filename, extension); [1] gets the extension
    file_extension = os.path.splitext(filename)[1]  

    # Check if the file extension is in the defined categories
    if file_extension in FILE_CATEGORIES:
        folder_name = FILE_CATEGORIES[file_extension]
        folder_path = os.path.join(SOURCE_FOLDER, folder_name)

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"Created folder: {folder_name}")

        # Handling duplicate files by checking if the file already exists in the destination folder
        if os.path.exists(os.path.join(folder_path, filename)):
            print(f"File {filename} already exists in {folder_path}. Skipping.")
            skipped_files += 1
        else:
            # Move the file to the appropriate folder
            move_file(SOURCE_FOLDER, filename, folder_path)
            moved_files += 1

    # If the file extension is not recognized, skip the file
    else:
        skipped_files += 1

print("\n----------- Summary -----------")
print(f"Scanned Files: {scanned_files}")
print(f"Scanned Folders: {scanned_folders}")
print(f"Moved: {moved_files}")
print(f"Skipped: {skipped_files}")

print("---------File organization complete.---------\n")