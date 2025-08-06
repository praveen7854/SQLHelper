from tkinter import filedialog

class FileHandler:
    def validate_file(self, file_path):
        """Validate the selected SQL file."""
        return file_path.endswith('.sql')

    def select_file(self):
        """Open file dialog to select the SQL file."""
        return filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
