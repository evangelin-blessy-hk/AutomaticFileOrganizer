"""
Automatic File Organizer

This program scans a selected directory, creates folders based on
file types (PDFs, Images, Videos, Audio, etc.), and moves each file
into its appropriate folder.
"""

from  gui import FileOrganizerGUI 

# Create an object of FileOrganizerGUI
app = FileOrganizerGUI()
app.run()