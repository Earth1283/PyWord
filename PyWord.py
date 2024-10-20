# Now running PyWord V1.2
# Earth1283 2024

import tkinter as tk
from tkinter import filedialog

class TextProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("PyWord")
        self.root.geometry("800x600")
        
        # Initialize current filename as None
        self.current_filename = None

        # Create Ribbon Bar
        self.create_ribbon()

        # Create a Text widget for editing
        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(expand=1, fill='both')

        # Add scrollbar to the Text widget
        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

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

    def new_document(self):
        self.text_area.delete(1.0, tk.END)  # Clear the text area
        self.current_filename = None  # Reset current filename

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

    def save_document(self):
        if self.current_filename:
            with open(self.current_filename, 'w') as file:
                content = self.text_area.get(1.0, tk.END)  # Get content from text area
                file.write(content)  # Write content to file
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

if __name__ == "__main__":
    root = tk.Tk()
    app = TextProcessor(root)
    root.mainloop()
