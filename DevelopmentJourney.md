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
[x] 2.0.1 Create a window
[x] 2.0.2 Add labels
[x] 2.0.3 Add browse button: User to choose source folder 
[x] 2.0.4 Connect browse button to textbox
[x] 2.0.5 Add organize files button
[x] 2.0.6 When clicked call organize_files()
[x] 2.0.7 Display files status while moving,etc
[x] 2.0.8 Show popup with summary

### Problems Faced

1. Summary displayed too early
Problem: Statistics were shown before file organization completed.
Solution: Created an organize_and_summarize() function to display the summary only after organizing.

2. Statistics accumulated across runs
Problem: Counters continued from the previous run.
Solution: Added a reset_stats() function before each organization.

3. Understanding exception handling
Problem: While debugging, it appeared that both the try and except blocks were executing.
Learning: Realized that the debugger's Step Into can be misleading when entering library functions. The except block only executes if an exception is actually raised.

4. Handling open files
Problem: An open PDF in Adobe Acrobat produced a PermissionError, yet a copy appeared in the destination folder.
Cause: shutil.move() copied the file but couldn't delete the original because it was in use.
Solution: Improved the error message to clearly explain this behavior.

5. Project structure
Problem: Managing everything in a single file became difficult.
Solution: Refactored the project into main.py, gui.py, and organizer.py.

### Version 2.1 - Improve the GUI.

[] Progress bar
[] Status label ("Organizing...")
[] Scrollable log window
[] Better colors
[] Better spacing

### Version 3.0 - Package it
Package into an executable using PyInstaller.

[] Convert to .exe
[] Custom icon
[] Installer
[] Ready for anyone to download

### Version 4.0 - Real-world improvements

[] Drag & Drop folder
[] Recursive folder organization
[] Undo last operation
[] User-defined categories
[] Settings saved automatically
[] Dark mode