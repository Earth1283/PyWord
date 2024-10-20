# Now running PyWord 1.3 Beta 3
# Earth1283 2024

import tkinter as tk
from tkinter import filedialog, simpledialog, font as tkFont
import os

class TextProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("PyWord")
        self.root.geometry("800x600")
        
        # Initialize current filename as None
        self.current_filename = None

        # Load default font from settings
        self.default_font = self.load_font_settings()
        
        # Create Ribbon Bar
        self.create_ribbon()

        # Create a Text widget for editing
        self.text_area = tk.Text(self.root, wrap='word', undo=True, font=self.default_font)
        self.text_area.pack(expand=1, fill='both')

        # Add scrollbar to the Text widget
        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

        # Create an unsaved changes indicator
        self.unsaved_indicator = tk.Label(self.root, text="Unsaved Changes", fg="red")
        self.unsaved_indicator.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)
        self.unsaved_indicator.pack_forget()  # Initially hidden

        # Bind the modified event to update the indicator
        self.text_area.bind("<<Modified>>", self.on_modified)
        
        # Bind the indicator to save the document when clicked
        self.unsaved_indicator.bind("<Button-1>", self.save_document)

        # Create a Menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Add File menu
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Document", command=self.new_document)
        self.file_menu.add_command(label="Open Document", command=self.open_document)
        self.file_menu.add_command(label="Save Document", command=self.save_document)
        self.file_menu.add_command(label="Save As...", command=self.save_as_document)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def create_ribbon(self):
        ribbon_frame = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        ribbon_frame.pack(side=tk.TOP, fill=tk.X)

        # Add buttons to the ribbon
        new_button = tk.Button(ribbon_frame, text="New", command=self.new_document)
        new_button.pack(side=tk.LEFT, padx=2, pady=2)

        open_button = tk.Button(ribbon_frame, text="Open", command=self.open_document)
        open_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_button = tk.Button(ribbon_frame, text="Save", command=self.save_document)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_as_button = tk.Button(ribbon_frame, text="Save As", command=self.save_as_document)
        save_as_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Add Save and Exit button
        save_exit_button = tk.Button(ribbon_frame, text="Save and Exit", command=self.save_and_exit)
        save_exit_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Add Settings button
        settings_button = tk.Button(ribbon_frame, text="Settings", command=self.open_settings)
        settings_button.pack(side=tk.LEFT, padx=2, pady=2)

    def new_document(self):
        self.text_area.delete(1.0, tk.END)  # Clear the text area
        self.current_filename = None  # Reset current filename
        self.hide_unsaved_indicator()

    def open_document(self):
        filename = filedialog.askopenfilename(defaultextension=".txt",
                                              filetypes=[("Text Files", "*.txt"),
                                                         ("All Files", "*.*")])
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)  # Clear the text area
                self.text_area.insert(tk.END, content)  # Insert file content
                self.current_filename = filename  # Update current filename
                self.hide_unsaved_indicator()

    def save_document(self, event=None):  # Accept an event parameter for the label click
        if self.current_filename:
            with open(self.current_filename, 'w') as file:
                content = self.text_area.get(1.0, tk.END)  # Get content from text area
                file.write(content.strip())  # Write content to file, stripping trailing newlines
            self.hide_unsaved_indicator()
        else:
            self.save_as_document()

    def save_as_document(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"),
                                                           ("All Files", "*.*")])
        if filename:
            self.current_filename = filename  # Save current filename
            self.save_document()

    def save_and_exit(self):
        self.save_document()  # Save the current document
        self.root.quit()      # Close the application

    def open_settings(self):
        # Create a new window for font settings
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Font Settings")
        
        # Available fonts
        available_fonts = list(tkFont.families())
        
        # Create a dropdown menu for font selection
        self.selected_font = tk.StringVar(value=self.default_font[0])
        font_dropdown = tk.OptionMenu(settings_window, self.selected_font, *available_fonts)
        font_dropdown.pack(padx=20, pady=10)

        # Create a size entry
        font_size_label = tk.Label(settings_window, text="Font Size:")
        font_size_label.pack(padx=20, pady=5)
        self.font_size_entry = tk.Entry(settings_window)
        self.font_size_entry.pack(padx=20, pady=5)
        self.font_size_entry.insert(0, self.default_font[1])

        # Save button
        save_button = tk.Button(settings_window, text="Save", command=self.apply_font_settings)
        save_button.pack(pady=10)

    def apply_font_settings(self):
        font_family = self.selected_font.get()
        font_size = int(self.font_size_entry.get())
        
        if font_family and font_size:
            self.default_font = (font_family, font_size)
            self.text_area.config(font=self.default_font)  # Apply new font to the text area
            self.save_font_settings()  # Save the new font settings

    def on_modified(self, event):
        self.text_area.edit_modified(False)  # Reset the modified flag
        self.show_unsaved_indicator()  # Show the unsaved changes indicator

    def show_unsaved_indicator(self):
        self.unsaved_indicator.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

    def hide_unsaved_indicator(self):
        self.unsaved_indicator.pack_forget()  # Hide the indicator

    def save_font_settings(self):
        with open("pyword_settings.txt", "w") as file:  # Specific file for font settings
            file.write(f"{self.default_font[0]},{self.default_font[1]}")  # Save font family and size

    def load_font_settings(self):
        if os.path.exists("pyword_settings.txt"):
            with open("pyword_settings.txt", "r") as file:
                line = file.readline().strip()
                font_family, font_size = line.split(",")
                return (font_family, int(font_size))  # Return as a tuple
        return ("Arial", 12)  # Default if file doesn't exist

if __name__ == "__main__":
    root = tk.Tk()
    app = TextProcessor(root)
    root.mainloop()
