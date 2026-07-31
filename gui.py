import tkinter as tk
from tkinter import filedialog
import organizer

class FileOrganizerGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Automatic File Organizer")
        self.window.geometry("600x400")

        # Create a label for the title
        self.title_label = tk.Label(
            self.window, 
            text="Automatic File Organizer"
            )
        self.title_label.config(font=("Arial", 24))
        self.title_label.pack() 

        self.select_folder_label = tk.Label(
            self.window, 
            text="Select a folder to organize:"
            )
        self.select_folder_label.pack(pady=10)

        self.select_folder_button = tk.Button(
            self.window, 
            text="Select Folder", 
            command=self.select_folder
            )
        self.select_folder_button.pack(pady=20)

        self.selected_folder_label = tk.Label(
            self.window, 
            text=""
            )
        self.selected_folder_label.pack(pady=10)


    # Function to select a folder on the user's computer
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.selected_folder_label.config(
                text=f"Selected folder: {folder}"
                )
            organizer.check_source_folder(folder, organizer.stats)
        

    def run(self):
        self.window.mainloop()

