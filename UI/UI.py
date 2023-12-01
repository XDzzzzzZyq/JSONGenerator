from utils import *
from tkinter import scrolledtext
from tkinter import filedialog
import tkinter as tk


def select_file_path(file_name: str, file_type: str, entry: tk.Entry):
    path = filedialog.askopenfilename(filetypes=[(file_name, file_type)])
    entry.insert(0, path)
    entry.pack()


class Panel:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.window = tk.Tk()
        self.excel_path = None
        self.json_template_path = None
        self.preview_area = None

    def set_generator_instance(self, generator: JSONGenerator):
        self.generator = generator

    def run(self):
        self.create_panel()
        self.window.mainloop()
        
    def create_panel(self):
        # Create Main Panel
        self.window.title("Json Generator")
        self.window.geometry(f"{self.width}x{self.height}")

        # Title Text
        title = tk.Label(self.window, text="Json Generator", font=("Arial", 16, "bold italic"), fg="blue")
        title.pack()

        # Excel Input
        excel_label = tk.Label(self.window, text="\nExcel Path:")
        excel_label.pack()
        self.excel_path = tk.Entry(self.window, width=int(self.width/20))
        self.excel_path.pack()
        button = tk.Button(self.window, text="Select File", command=self.select_excel_path)
        button.pack()

        # Json Template Input
        json_template_label = tk.Label(self.window, text="\nJson Template Path:")
        json_template_label.pack()
        self.json_template_path = tk.Entry(self.window, width=int(self.width/20))
        self.json_template_path.pack()
        button = tk.Button(self.window, text="Select File", command=self.select_template_path)
        button.pack()
        
        # Empty Line1
        empty_line1 = tk.Label(self.window, text="\n")
        empty_line1.pack()

        # Transform Button
        transform = tk.Button(self.window, text="Transform", command=self.transform_to_json)
        transform.pack()

        # Scrolled Preview
        preview_label = tk.Label(self.window, text="\nPreview:")
        preview_label.pack()
        self.preview_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=int(self.width/12), height=int(self.height/30))
        self.preview_area.pack()

        # Empty Line2
        empty_line3 = tk.Label(self.window, text="\n")
        empty_line3.pack()

        # Write In Json File
        write_json = tk.Button(self.window, text="Write Into File", command=self.write_in_json)
        write_json.pack()

    def select_excel_path(self):
        select_file_path("Excel File: ", "*.xlsx", self.excel_path)
        self.generator.import_dataset(self.excel_path.get())

    def select_template_path(self):
        select_file_path("Json Template File: ", "*.json", self.json_template_path)
        self.generator.import_template(self.json_template_path.get())
    
    def transform_to_json(self):
        self.generator.generate_json("example/result/")
                          
    def write_in_json(self):
        pass