# Development Journey

## Version 0 - Initial Implementation

### Goal
Build a Python script that automatically organizes files into folders based on file type.

### Approach
- Used multiple if-elif statements.
- Checked each extension individually.
- Created folders if they didn't exist.
- Moved files using shutil.move().

### What I Learned
- os.listdir()
- os.mkdir()
- shutil.move()
- os.path.join()

### Problems
- Lots of repeated code.
- Difficult to add new file types.
- Hard to maintain.

---

## Version 1.0 - Refactoring
### Improvements
- Added move_file() function.
- Replaced repeated if-elif blocks with a dictionary.
- Used os.path.splitext().
- Used SOURCE_FOLDER constant.
- Added documentation and comments.
- Cleaner folder creation.
### Result
The code became much shorter, easier to read, and easier to extend.

---

## Future Versions

### Version 1.1
[x] Ignore temporary Office files.
[x] Ignore directories.
[x] Handle duplicate filenames.
[x] Users can input folder to organize

### Version 1.2 – Error Handling
### Planned improvements
[x] Handle invalid source folder (FileNotFoundError)
[x] Handle permission denied while moving files (PermissionError)
[x] Handle duplicate filenames in destination folder
[x] Handle files currently open by another application
[x] Handle files being used by another process
[x] Handle invalid destination folder
[x] Handle unexpected errors gracefully (Exception)
[x] Display meaningful error messages instead of crashing

### Version 2.0 - GUI using Tkinter.
[] 2.0.1 Create a window
[] 2.0.2 Add labels
[] 2.0.3 Add browse button: User to choose source folder 
[] 2.0.4 Connect browse button to textbox
[] 2.0.5 Add organize files vutton
[] 2.0.6 When clicked call organize_files()
[] 2.0.7 Display files status while moving,etc
[] 2.0.8 Show popup with summary

### Version 3.0
Package into an executable using PyInstaller.

### Version 4.0
- Drag and drop
- Progress bar
- Undo
- Custom categories