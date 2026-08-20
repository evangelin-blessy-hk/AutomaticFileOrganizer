import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import organizer, os

class FileOrganizerGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Automatic File Organizer")
        self.window.geometry("1000x700")

        # Create canvas
        self.canvas = tk.Canvas(self.window)

        # Create scrollbar for the canvas
        self.main_scrollbar = tk.Scrollbar(
            self.window,
            orient="vertical",
            command=self.canvas.yview
        )
        self.main_scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # Connect canvas to scrollbar
        self.canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        # Frame that will contain all your widgets
        self.main_frame = tk.Frame(
            self.canvas,
            bd=2,
            relief=tk.GROOVE
        )

        # Put main_frame inside canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_main_frame
        )

        # Update scrollable region when frame changes size
        self.main_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Create a label for the title
        self.title_label = tk.Label(
            self.main_frame, 
            text="Automatic File Organizer"
            )
        self.title_label.config(font=("Arial", 15))
        self.title_label.pack(pady=15) 

        self.select_folder_label = tk.Label(
            self.main_frame, 
            text="Select a folder to organize:"
            )
        self.select_folder_label.pack(pady=(15, 5))

        self.select_folder_button = tk.Button(
            self.main_frame, 
            text="Select Folder", 
            command=self.select_folder
            )
        self.select_folder_button.pack(pady=5)

        self.selected_folder_label = tk.Label(
            self.main_frame, 
            text=""
            )
        self.selected_folder_label.pack(pady=5)

        self.folder_tree = ttk.Treeview(self.main_frame, height=12)
        self.folder_tree.pack(pady=10)

        self.select_organize_button = tk.Button(
                    self.main_frame,
                    text="Start Organizing",
                    command=self.organize_and_summarize,
                    state="disabled"
                )
        self.select_organize_button.pack(pady=(25,5))

        self.status_label = tk.Label(self.main_frame, text="")
        self.status_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(
                    self.main_frame,
                    orient="horizontal",
                    length=400,
                    mode="determinate"
                )
        self.progress_bar.pack(pady=5)

        self.progress_label = tk.Label(self.main_frame, text="0%")
        self.progress_label.pack(pady=1)

        # Create a frame to hold the log box and scrollbar
        self.log_frame = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.log_frame.pack(pady=10)

        # Create the log box
        self.log_box = tk.Text(self.log_frame, height=8, width=80)
        self.log_box.pack(side=tk.LEFT)

        # Create the scrollbar
        self.log_scrollbar = tk.Scrollbar(
            self.log_frame,
            command=self.log_box.yview
        )
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Connect the log box to the scrollbar
        self.log_box.config(yscrollcommand=self.log_scrollbar.set)

         # Create a frame to hold the summary box and scrollbar
        self.summary_frame = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.summary_frame.pack(pady=10)

         # Create the summary box
        self.summary_box = tk.Text(self.summary_frame, height=10, width=40)
        self.summary_box.pack(side=tk.LEFT)

        # Create the scrollbar
        self.summary_scrollbar = tk.Scrollbar(
            self.summary_frame,
            command=self.summary_box.yview
        )
        self.summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Connect the summary box to the scrollbar
        self.summary_box.config(yscrollcommand=self.summary_scrollbar.set)

        self.undo_button = tk.Button(
            self.main_frame,
            text="Undo Last Organization",
            command=self.undo_last_organization,
            state="disabled"
        )
        self.undo_button.pack(pady=5)

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def resize_main_frame(self, event):
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def display_folder_tree(self, source_folder):

        # Clear existing tree
        for item in self.folder_tree.get_children():
            self.folder_tree.delete(item)

        # Add source folder
        root_id = self.folder_tree.insert(
            "",
            "end",
            text=f"📁 {os.path.basename(source_folder)}"
        )

        # Keep track of Treeview IDs
        tree_items = {
            source_folder: root_id
        }

        # Walk through the folder structure
        for root, folders, files in os.walk(source_folder):

            parent_id = tree_items[root]

            for folder in folders:

                folder_path = os.path.join(root, folder)

                folder_id = self.folder_tree.insert(
                    parent_id,
                    "end",
                    text=f"☐ 📁 {folder}"
                )

                tree_items[folder_path] = folder_id


    def disable_organize_button(self):
        self.select_organize_button.config(state="disabled")

    def reset_progress_bar(self):
        self.progress_bar['value'] = 0
        self.progress_label.config(text="0%")
        self.main_frame.update_idletasks() # Update the GUI to reflect the progress bar change

    # Function to select a folder on the user's computer
    def select_folder(self):
        folder = filedialog.askdirectory() # Open a dialog to select a folder

        # Check if user selected a folder or canceled the dialog
        if folder:
            # If a folder is selected, update the label and enable the organize button
            self.selected_folder = folder
            self.selected_folder_label.config(
                text=f"Selected folder: {folder}"
                )
            self.disable_organize_button()
            self.reset_progress_bar()
            organizer.check_source_folder(self.selected_folder, self.log_message)
            self.start_organizing()

        else:
            # If the user cancels the folder selection, reset the label and progress bar
            self.selected_folder_label.config(
                text="No folder selected. Please select a folder."
                )
            self.status_label.config(text="Status: Not Ready")
            self.reset_progress_bar()

    # Function to reset the statistics and progress bar
    def reset_stats(self):
        organizer.stats = {
            "scanned_files": 0,
            "scanned_folders": 0,
            "moved": 0,
            "skipped": 0,
            "errors": 0
        }
        self.reset_progress_bar()
        self.log_box.insert(tk.END, "\n-------------------------------------------------------------------------\n")
        self.log_box.see(tk.END)  # Scroll to the end

    # Function to start organizing files in the selected folder
    def start_organizing(self):
        self.selected_folder_label.config(
            text=f"Organizing files in: {self.selected_folder}"
        )
        self.display_folder_tree(self.selected_folder)
        self.select_organize_button.config(state="normal")
        self.status_label.config(text="Status: Ready")

    def display_summary(self):
        summary = (
            f"Organization Summary in {self.selected_folder}:\n"
            f"Files scanned: {organizer.stats['scanned_files']}\n"
            f"Folders scanned: {organizer.stats['scanned_folders']}\n"
            f"Files moved: {organizer.stats['moved']}\n"
            f"Files skipped: {organizer.stats['skipped']}\n"
            f"Errors encountered: {organizer.stats['errors']} \n"
        )
       
        self.summary_box.insert(tk.END, "\n------------------------------------\n" + summary)  # Insert new summary
        self.summary_box.see(tk.END)  # Scroll to the end

        messagebox.showinfo(
            "Completed",
            "Files organized successfully!"
        )

    def log_message(self, message):
        # Create a label for the log message
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)  # Scroll to the end

    # Function to update the progress bar for each file and percentage label
    def update_progress(self):
        self.progress_bar['value'] += 1
        current = self.progress_bar["value"]
        maximum = self.progress_bar["maximum"]
    
        percentage = (current / maximum) * 100

        self.progress_label.config(
            text=f"{percentage:.0f}%"
        )
        self.main_frame.update_idletasks() # Update the GUI to reflect the progress bar change

    def set_progress_maximum(self, total_files):
        self.progress_bar['maximum'] = total_files
        self.main_frame.update_idletasks() # Update the GUI to reflect the progress bar change

    def organize_and_summarize(self):
        self.status_label.config(text="Status: Organizing...")
        self.reset_stats()
        organizer.organize_files(self.selected_folder, organizer.stats, self.log_message, self.update_progress, self.set_progress_maximum)
        self.status_label.config(text="Status: Organization Completed")
        self.disable_organize_button()
        self.display_summary()
        self.undo_button.config(state="normal")  # Enable the undo button after organizing files

    def undo_last_organization(self):

        # Check if there are any moved files to undo
        if not organizer.moved_files and not organizer.deleted_folders:
            messagebox.showinfo(
                "Undo Not Possible",
                "No files have been moved yet. Cannot undo."
            )
            self.status_label.config(text="Status: Undo Not Possible")
            self.undo_button.config(state="disabled")  # Disable the undo button if no files to undo
            self.reset_progress_bar()  # Reset the progress bar since no files were moved
            return

        self.status_label.config(text="Status: Undoing last organization...")
        organizer.undo_organize_files(organizer.moved_files, organizer.stats, self.log_message)
        self.status_label.config(text="Status: Undo Completed")
        self.undo_button.config(state="disabled")  # Disable the undo button after undoing
        
        # Clear the moved files list after undoing
        organizer.moved_files.clear()
        organizer.created_folders.clear()  # Clear the created folders list after undoing

    def run(self):
        self.window.mainloop()
