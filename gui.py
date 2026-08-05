import tkinter as tk
from tkinter import filedialog, messagebox
import organizer

class FileOrganizerGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Automatic File Organizer")
        self.window.geometry("600x600")

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

        self.select_organize_button = tk.Button(
                    self.window,
                    text="Start Organizing",
                    command=self.organize_and_summarize,
                    state="disabled"
                )
        self.select_organize_button.pack(pady=20)


    # Function to select a folder on the user's computer
    def select_folder(self):
        folder = filedialog.askdirectory()
        # Check if user selected a folder or canceled the dialog
        if folder:
            self.selected_folder = folder
            self.selected_folder_label.config(
                text=f"Selected folder: {folder}"
                )
            organizer.check_source_folder(self.selected_folder)
            self.start_organizing()
        else:
            self.selected_folder_label.config(
                text="No folder selected. Exiting."
                )
            self.window.destroy()

    def reset_stats(self):
        organizer.stats = {
            "scanned": 0,
            "moved": 0,
            "skipped": 0,
            "errors": 0
        }
            
    def start_organizing(self):
        self.selected_folder_label.config(
            text=f"Organizing files in: {self.selected_folder}"
        )
        self.select_organize_button.config(state="normal")

    def disable_organize_button(self):
        self.select_organize_button.config(state="disabled")
        

    def display_summary(self):
        summary = (
            f"Organization Summary in {self.selected_folder}:\n"
            f"Files scanned: {organizer.stats['scanned']}\n"
            f"Files moved: {organizer.stats['moved']}\n"
            f"Files skipped: {organizer.stats['skipped']}\n"
            f"Errors encountered: {organizer.stats['errors']}"
        )
        self.summary_label = tk.Label(
            self.window, 
            text=summary
        )
        self.summary_label.pack(pady=10)
        messagebox.showinfo(
            "Completed",
            "Files organized successfully!"
        )

    def organize_and_summarize(self):
        self.reset_stats()
        organizer.organize_files(self.selected_folder, organizer.stats)
        self.disable_organize_button()
        self.display_summary()
    

    def run(self):
        self.window.mainloop()

