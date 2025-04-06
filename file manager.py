import os
import stat
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Manager")
        self.current_path = os.path.expanduser("~")
        self.history = [self.current_path]  # Initialize history with the starting directory
        self.history_index = 0  # Start at the first item in history
        self.dark_mode = False
        self.style = ttk.Style()

        # Top Frame: Path Label and Search
        path_frame = ttk.Frame(root)
        path_frame.pack(fill='x', padx=5, pady=5)
        
        self.path_label = ttk.Label(path_frame, text=self.current_path, font=("Arial", 12))
        self.path_label.pack(side='left', padx=5)

        self.search_entry = ttk.Entry(path_frame)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind("<Return>", self.search_files)

        # Dropdown for File Type Filter
        self.file_filter_var = tk.StringVar(value="All Files")
        file_types = ["All Files", ".py", ".txt", ".exe", ".jpg", ".png", ".pdf"]
        self.file_filter_menu = ttk.OptionMenu(path_frame, self.file_filter_var, *file_types)
        self.file_filter_menu.pack(side='left', padx=5)

        # Buttons with different colors for clarity
        button_frame = ttk.Frame(root)
        button_frame.pack(fill='x', padx=5, pady=5)

        self.search_button = ttk.Button(button_frame, text="Search", command=self.search_files)
        self.search_button.pack(side='left', padx=5)

        self.back_button = ttk.Button(button_frame, text="Back", command=self.go_back)
        self.back_button.pack(side='left', padx=5)

        self.forward_button = ttk.Button(button_frame, text="Next", command=self.go_forward)
        self.forward_button.pack(side='left', padx=5)

        self.theme_button = ttk.Button(button_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side='right', padx=5)

        self.help_button = ttk.Button(button_frame, text="Help", command=self.show_help)
        self.help_button.pack(side='right', padx=5)

        # File Explorer (Treeview)
        self.tree = ttk.Treeview(root, columns=("Name", "Size", "Modified"), show='headings', selectmode='extended')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Modified", text="Modified")
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.open_item)

        self.update_theme()
        self.style_buttons()
        self.load_directory()

    def style_buttons(self):
        """Apply different colors to buttons for a professional look."""
        self.search_button.configure(style="Search.TButton")
        self.back_button.configure(style="Back.TButton")
        self.forward_button.configure(style="Next.TButton")
        self.theme_button.configure(style="Theme.TButton")
        self.help_button.configure(style="Help.TButton")

        self.style.configure("Search.TButton", foreground="black", background="lightblue", padding=5)
        self.style.configure("Back.TButton", foreground="black", background="lightgreen", padding=5)
        self.style.configure("Next.TButton", foreground="black", background="orange", padding=5)
        self.style.configure("Theme.TButton", foreground="white", background="darkgray", padding=5)
        self.style.configure("Help.TButton", foreground="black", background="yellow", padding=5)

    def show_help(self):
        """Show help options: File colors or Directory hierarchy"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")

        tk.Label(help_window, text="Choose an option:", font=("Arial", 12, "bold")).pack(pady=5)

        ttk.Button(help_window, text="File Type Colors", command=self.show_colors).pack(pady=5)
        ttk.Button(help_window, text="Directory Hierarchy", command=self.show_hierarchy).pack(pady=5)

    def show_colors(self):
        """Display file type color meanings"""
        color_info = """
        File Type Colors:
        - Folders: Blue 🔵
        - Python Files (.py): Green🟢  
        - Executables (.exe): Red 🔴 
        - Text Files (.txt): Orange🟠
        - Images (.jpg, .png): Purple🟣
        - PDFs (.pdf): Brown🟤
        - Other Files: White⚪
        """
        messagebox.showinfo("File Type Colors", color_info)

    def is_hidden_or_system(self, filepath):
        """Check if a file is hidden/system (Windows) or starts with '.' (Unix)."""
        try:
            attrs = os.stat(filepath).st_file_attributes
            return bool(attrs & (stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_SYSTEM))
        except AttributeError:
            return os.path.basename(filepath).startswith('.')

    def is_pyi_file_or_directory(self, filepath):
        """Check if a file has .pyi extension or is a directory ending with .pyi."""
        return filepath.endswith('.pyi') or (os.path.isdir(filepath) and os.path.basename(filepath).endswith('.pyi'))

    def generate_tree(self, root_dir, prefix=''):
        """Generate filtered directory hierarchy string."""
        hierarchy = "\n"
        if not os.path.isdir(root_dir):
            return f"Error: '{root_dir}' is not a directory or cannot be accessed."
        
        try:
            entries = os.listdir(root_dir)
            # Filter out hidden/system files and .pyi files/directories
            entries = [
                e for e in entries
                if not self.is_hidden_or_system(os.path.join(root_dir, e)) and
                not self.is_pyi_file_or_directory(os.path.join(root_dir, e))
            ]
            entries.sort()  # Sort alphabetically after filtering

            for index, entry in enumerate(entries):
                path = os.path.join(root_dir, entry)
                connector = '├── ' if index < len(entries) - 1 else '└── '
                hierarchy += prefix + connector + entry + "\n"
                
                if os.path.isdir(path):
                    extension = '│   ' if index < len(entries) - 1 else '    '
                    hierarchy += self.generate_tree(path, prefix + extension)
        
        except PermissionError:
            hierarchy += prefix + '└── [Access Denied]\n'
        except FileNotFoundError:
            hierarchy += prefix + '└── [Path Not Found]\n'
        
        return hierarchy

    def show_hierarchy(self):
        """Display directory structure with filtering."""
        hierarchy = self.generate_tree(self.current_path)
        messagebox.showinfo("Directory Hierarchy", hierarchy)

    def search_files(self, event=None):
        """Search files by name or filter by type"""
        query = self.search_entry.get().lower()
        selected_filter = self.file_filter_var.get()  
        self.tree.delete(*self.tree.get_children())

        try:
            for item in os.listdir(self.current_path):
                item_path = os.path.join(self.current_path, item)
                if selected_filter != "All Files" and not item.endswith(selected_filter):
                    continue  # Skip if file does not match the filter

                if query in item.lower() or selected_filter == "All Files":
                    size = os.path.getsize(item_path) if os.path.isfile(item_path) else "-"
                    modified = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%Y-%m-%d %H:%M')
                    color = self.get_file_color(item)
                    self.tree.insert("", "end", values=(item, size, modified), tags=(color,))
                    self.tree.tag_configure(color, foreground=color)
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied")

    def update_theme(self):
        """Apply Theme Based on Mode."""
        if self.dark_mode:
            self.style.theme_use("clam")
            self.root.configure(bg="black")
            self.style.configure("Treeview", background="black", foreground="white", fieldbackground="black")
        else:
            self.style.theme_use("default")
            self.root.configure(bg="#F0F0F0")
            self.style.configure("Treeview", background="white", foreground="black", fieldbackground="white")

        self.style.configure("Back.TButton", foreground="white", background="blue")
        self.style.configure("Next.TButton", foreground="white", background="green")
        self.style.configure("Dark.TButton", foreground="white", background="black")
        self.style.configure("Help.TButton", foreground="white", background="orange")

        self.load_directory()

    
    def toggle_theme(self):
        """Toggle Dark/Light Mode."""
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def load_directory(self, *_):
        self.tree.delete(*self.tree.get_children())
        items = []
        try:
            for item in os.listdir(self.current_path):
                item_path = os.path.join(self.current_path, item)
                size = os.path.getsize(item_path) if os.path.isfile(item_path) else "-"
                modified = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%Y-%m-%d %H:%M')
                items.append((item, size, modified))
            self.sort_items(items)
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied")

    def sort_items(self, items):
        for item in items:
            name, size, modified = item
            color = self.get_file_color(name)
            self.tree.insert("", "end", values=(name, size, modified), tags=(color,))
            self.tree.tag_configure(color, foreground=color)

    def get_file_color(self, filename):
        if os.path.isdir(os.path.join(self.current_path, filename)):
            return "blue"
        elif filename.endswith(".py"):
            return "green"
        elif filename.endswith(".exe"):
            return "red"
        elif filename.endswith(".txt"):
            return "orange"
        elif filename.endswith(".jpg") or filename.endswith(".png"):
            return "purple"
        elif filename.endswith(".pdf"):
            return "brown"
        else:
            return "white"

    def go_back(self):
        """Navigate to the previous directory in history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            self.path_label.config(text=self.current_path)
            self.load_directory()

    def go_forward(self):
        """Navigate to the next directory in history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            self.path_label.config(text=self.current_path)
            self.load_directory()

    def open_item(self, event=None):
        """Open a directory or file."""
        selected = self.tree.item(self.tree.selection())['values'][0]
        path = os.path.join(self.current_path, selected)
        if os.path.isdir(path):
            # Add the new directory to history and update the index
            if self.history_index < len(self.history) - 1:
                # If we're not at the end of history, truncate the forward history
                self.history = self.history[:self.history_index + 1]
            self.history.append(path)
            self.history_index += 1
            self.current_path = path
            self.path_label.config(text=self.current_path)
            self.load_directory()
        else:
            os.startfile(path)

# Run the application
root = tk.Tk()
root.title("File Manager")
root.geometry("600x500")
app = FileManager(root)
root.mainloop()