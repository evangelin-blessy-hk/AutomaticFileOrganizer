import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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

        self.progress_bar = ttk.Progressbar(
                    self.window,
                    orient="horizontal",
                    length=400,
                    mode="determinate"
                )

        self.progress_bar.pack(pady=10)

        self.progress_label = tk.Label(self.window, text="0%")
        self.progress_label.pack()

        self.log_box = tk.Text(self.window, height=10, width=60)
        self.log_box.pack(pady=10)


    # Function to select a folder on the user's computer
    def select_folder(self):
        folder = filedialog.askdirectory()
        # Check if user selected a folder or canceled the dialog
        if folder:
            self.selected_folder = folder
            self.selected_folder_label.config(
                text=f"Selected folder: {folder}"
                )
            organizer.check_source_folder(self.selected_folder, self.log_message)
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

    def log_message(self, message):
        # Create a label for the log message
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)  # Scroll to the end

    def update_progress(self):
        self.progress_bar['value'] += 1
        current = self.progress_bar["value"]
        maximum = self.progress_bar["maximum"]
        percentage = (current / maximum) * 100

        self.progress_label.config(
            text=f"{percentage:.0f}%"
        )
        self.window.update_idletasks() # Update the GUI to reflect the progress bar change

    def set_progress_maximum(self, total_files):
        self.progress_bar['maximum'] = total_files
        self.window.update_idletasks() # Update the GUI to reflect the progress bar change

    def organize_and_summarize(self):
        self.reset_stats()
        organizer.organize_files(self.selected_folder, organizer.stats, self.log_message, self.update_progress, self.set_progress_maximum)
        self.disable_organize_button()
        self.display_summary()

    def run(self):
        self.window.mainloop()
