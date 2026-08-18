import  os
import  shutil as su

# Define file categories based on their extensions
FILE_CATEGORIES = {
    "PDFs_AFO": [".pdf"],
    "Images_AFO": [".jpeg", ".png", ".jpg"],
    "Audio_AFO": [".mp3", ".wav"],
    "Videos_AFO": [".mp4", ".mkv"],
    "Documents_AFO": [".docx", ".txt"],
    "Compressed_AFO": [".zip", ".rar"],
    "Executables_AFO": [".exe"],
    "Excel_AFO": [".xlsx", ".csv"]
}

# Track file statistics
stats = {
    "scanned_files": 0,
    "scanned_folders": 0,
    "moved": 0,
    "skipped": 0,  # hidden files, temp files, unrecognized extensions, duplicates
    "errors": 0    # permission denied, disk removed, unexpeccted exceptions
}

moved_files = []  # List to track moved files

created_folders = []  # List to track created folders

deleted_folders = []

# Check if the source folder exists
def check_source_folder(SOURCE_FOLDER, log_callback):

    # Check if the source folder exists
    if not os.path.exists(SOURCE_FOLDER):
        log_callback(f"The folder '{SOURCE_FOLDER}' does not exist. Exiting.")
        # print(f"The folder '{SOURCE_FOLDER}' does not exist. Exiting.")
        exit()
    
# Create a folder if it doesn't exist
def create_folder(folder_path, folder_name,log_callback):
    try:
        os.mkdir(folder_path)
        log_callback(f"Created folder: {folder_name}")
        # print(f"Created folder: {folder_name}")
        created_folders.append({"path": folder_path, "name": folder_name})
        return True
    except PermissionError:
        log_callback(f"Permission denied while creating folder {folder_name}. Skipping.")
        # print(f"Permission denied while creating folder {folder_name}. Skipping.")
        return False
    except Exception as error:
        log_callback(f"Error creating folder {folder_name}: {error}")
        # print(f"Error creating folder: {error}")
        return False

# Move a file to the specified folder
def move_file(source_folder, filename, folder_path,  stats, log_callback):
    try:
        su.move(
            src=os.path.join(source_folder, filename), 
            dst=os.path.join(folder_path, filename)
            )
        log_callback(f"Moved {filename} to {folder_path}.")
        # print(f"Moved {filename} to {folder_path}.")
        stats["moved"] += 1
        moved_files.append({
            "source": os.path.join(source_folder, filename), 
            "destination": os.path.join(folder_path, filename)
            })
        
    except PermissionError:
        log_callback(
            f"Permission denied while moving file {filename}. "
            "The file was copied to the destination, "
            "but the original could not be removed "
            "because it is currently open in another application."
            )
        stats["errors"] += 1

    except Exception as error:
        log_callback(f"Error moving file {filename}: {error}")
        # print(f"Error moving file {filename}: {error}") 
        stats["errors"] += 1

# Scan the source folder to count the total number of files (excluding hidden and temporary files)
def scan_folder(SOURCE_FOLDER):
    total_files = 0
   
    for root, dirs, files in os.walk(SOURCE_FOLDER):
        dirs[:] = [folder for folder in dirs if not folder.endswith("_AFO")]
        for filename in files:
            if filename.startswith('.') or filename.startswith('~'):
                continue
            total_files += 1
    return total_files  # Return total files 

# Get the category for a given file extension
def get_category_for_extension(file_extension):
    for folder_name, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return folder_name
    return None  # Return None if the extension is not recognized

def delete_empty_folders(SOURCE_FOLDER):
        for root, folders, files in os.walk(SOURCE_FOLDER, topdown=False):
            if root == SOURCE_FOLDER:
                continue

            if os.path.basename(root).endswith("_AFO"):
                continue

            if not os.listdir(root):
                try:
                    os.rmdir(root)
                    print(f"Removed folder empty folder: {root}.")
                    deleted_folders.append({"path": root})
                except OSError as error:
                    print(f"Error removing folder {root}: {error}")
                

# Organize files in the source folder based on their extensions
def organize_files(SOURCE_FOLDER, stats=stats, log_callback=None, progress_callback=None, 
                   total_files_callback=None):

    total_files = scan_folder(SOURCE_FOLDER)
   
    total_files_callback(total_files)  # Update the total number of files to process

    for root, dirs, files in os.walk(SOURCE_FOLDER):
        dirs[:] = [folder for folder in dirs if not folder.endswith("_AFO")]

        # Iterate through each file in the source folder
        for filename in files:
            # Skip hidden files and temporary files (starting with '.' or '~')
            if filename.startswith('.') or filename.startswith('~'):
                progress_callback()
                continue
            else:   
                stats["scanned_files"] += 1

            # splitext() returns (filename, extension); [1] gets the extension
            file_extension = os.path.splitext(filename)[1].lower()

            folder_name = get_category_for_extension(file_extension)

            if folder_name != None:
                folder_path = os.path.join(SOURCE_FOLDER, folder_name)

                # Create the folder if it doesn't exist
                if not os.path.exists(folder_path):
                    if not create_folder(folder_path, folder_name, log_callback):
                        stats["skipped"] += 1
                        log_callback(f"Error creating folder {folder_name}. Skipping {filename}.")
                        # print(f"Error creating folder {folder_name}. Skipping {filename}.")
                        continue  # Skip moving the file if folder creation failed

                # Handling duplicate files by checking if the file already exists in the destination folder
                if os.path.exists(os.path.join(folder_path, filename)):
                    log_callback(f"File {filename} already exists in {folder_path}. Skipping.")
                    # print(f"File {filename} already exists in {folder_path}. Skipping.")
                    stats["skipped"] += 1
                else:
                    # Move the file to the appropriate folder
                    move_file(root, filename, folder_path, stats, log_callback)

            # If the file extension is not recognized, skip the file
            else:
                stats["skipped"] += 1
                log_callback(f"File {filename} has an unrecognized extension. Skipping.")
                # print(f"File {filename} has an unrecognized extension. Skipping.")
        
            progress_callback()  # Update progress after each file is processed

    # If no files were scanned, log a message indicating that no files were found
    if stats["scanned_files"] == 0:
        log_callback(f"No files found in {SOURCE_FOLDER} to organize.")
        print(f"No files found in {SOURCE_FOLDER} to organize.")

    delete_empty_folders(SOURCE_FOLDER)

def undo_organize_files(moved_files, stats, log_callback):
    log_callback("\n Undoing file organization...\n")
    print(f"Moved Files: {moved_files}\n")
    print(f"Created Folders: {created_folders}")

    for file_info in moved_files:
        source = file_info["source"]
        destination = file_info["destination"]

        try:
            # Recreate the original folder structure
            os.makedirs(os.path.dirname(source), exist_ok=True)
            su.move(destination, source)
            log_callback(f"Moved {os.path.basename(destination)} back to {source}.")
        except Exception as error:
            print(f"Error undoing {source} folder: {error}")
            log_callback(f"Error moving {os.path.basename(destination)} back to {source}: {error}")

    for folder_info in created_folders:
        folder_path = folder_info["path"]
        folder_name = folder_info["name"]
        try:
            os.rmdir(folder_path)
            log_callback(f"Removed folder: {folder_name}.")
        except OSError as error:
            log_callback(f"Error removing folder {folder_name}: {error}")

    # Creating the deleted empty folder
    for deleted_folder in deleted_folders:
        # print(deleted_folder)
        folder_info = deleted_folder["path"]
        if not os.path.exists(folder_info):
            try:
                os.makedirs(folder_info, exist_ok=True)
                log_callback(f"Created folder {folder_info}")
            except Exception as error:
                log_callback(f"Error creating {folder_info}: {error}")

    log_callback("\n Undoing file organization completed.\n")      
    print("\nUndo operation completed.")
    print(f"Files moved back: {stats['moved']}, Errors: {stats['errors']}")