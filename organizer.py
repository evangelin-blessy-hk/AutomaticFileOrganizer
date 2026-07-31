import  os
import  shutil as su

# Define file categories based on their extensions
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

# Track file statistics
stats = {
    "scanned": 0,
    "moved": 0,
    "skipped": 0,  # hidden files, temp files, unrecognized extensions, duplicates
    "errors": 0    # permission denied, disk removed, unexpeccted exceptions
}

# Folder to organize
# SOURCE_FOLDER = input("Enter the path of the folder to organize: ")
# SOURCE_FOLDER = app.selected_folder

# Check if the source folder exists
def check_source_folder(SOURCE_FOLDER, stats):
    if SOURCE_FOLDER == "":
        print("No folder path provided. Exiting.")
        exit()
    elif not os.path.exists(SOURCE_FOLDER):
        print(f"The folder '{SOURCE_FOLDER}' does not exist. Exiting.")
        exit()
    else:
        # Get a list of all files in the source folder
        files = os.listdir(SOURCE_FOLDER)
        organize_files(SOURCE_FOLDER, files, stats)

# Create a folder if it doesn't exist
def create_folder(folder_path, folder_name):
    try:
        os.mkdir(folder_path)
        print(f"Created folder: {folder_name}")
        return True
    except PermissionError:
        print(f"Permission denied while creating folder {folder_name}. Skipping.")
        return False
    except Exception as error:
        print(f"Error creating folder: {error}")
        return False

# Move a file to the specified folder
def move_file(source_folder, filename, folder_path,  stats):
    try:
        su.move(
            src=os.path.join(source_folder, filename), 
            dst=os.path.join(folder_path, filename)
            )
        print(f"Moved {filename} to {folder_path}.")
        stats["moved"] += 1
        
    except PermissionError:
        print(f"Permission denied while moving file {filename}. Skipping.")
        stats["errors"] += 1
    except Exception as error:
        print(f"Error moving file {filename}: {error}") 
        stats["errors"] += 1


# Organize files in the source folder based on their extensions
def organize_files(SOURCE_FOLDER,files, stats=stats):
   
    # Iterate through each file in the source folder
    for filename in files:

        # Skip hidden files and temporary files (starting with '.' or '~')
        if filename.startswith('.') or filename.startswith('~'):
            continue

        # Check if the item is a directory or a file
        if os.path.isdir(os.path.join(SOURCE_FOLDER, filename)):
            continue    
        else:   
            stats["scanned"] += 1

        # splitext() returns (filename, extension); [1] gets the extension
        file_extension = os.path.splitext(filename)[1]  

        # Check if the file extension is in the defined categories
        if file_extension in FILE_CATEGORIES:
            folder_name = FILE_CATEGORIES[file_extension]
            folder_path = os.path.join(SOURCE_FOLDER, folder_name)

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                if not create_folder(folder_path, folder_name):
                    stats["skipped"] += 1
                    print(f"Error creating folder {folder_name}. Skipping {filename}.")
                    continue  # Skip moving the file if folder creation failed

            # Handling duplicate files by checking if the file already exists in the destination folder
            if os.path.exists(os.path.join(folder_path, filename)):
                print(f"File {filename} already exists in {folder_path}. Skipping.")
                stats["skipped"] += 1
            else:
                # Move the file to the appropriate folder
                move_file(SOURCE_FOLDER, filename, folder_path, stats)

        # If the file extension is not recognized, skip the file
        else:
            stats["skipped"] += 1
            print(f"File {filename} has an unrecognized extension. Skipping.")

    summarize_statistics(stats)

def summarize_statistics(stats):
    print("\n----------- Summary -----------")
    print(f"Scanned Files: {stats['scanned']}")
    print(f"Moved: {stats['moved']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Errors: {stats['errors']}")

    print("---------File organization complete.---------\n")