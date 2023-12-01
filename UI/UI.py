from utils import *
from tkinter import scrolledtext
from tkinter import filedialog
import tkinter as tk


def select_file_path(entry: tk.Entry, file_name: str = None, file_type: str = None):
    if(file_name == None or file_type == None):
        path = filedialog.askdirectory()
    else:
        path = filedialog.askopenfilename(filetypes=[(file_name, file_type)])
    entry.delete(0, tk.END)
    entry.insert(0, path)
    entry.pack()


class Panel:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.window = tk.Tk()
        self.preview_area = None
        self.excel_path = None
        self.json_template_path = None
        self.export_path = None
        self.start_entry = None
        self.end_entry = None
        self.generator = JSONGenerator()

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
        button1 = tk.Button(self.window, text="Select File", command=lambda: select_file_path(self.excel_path, "Excel File: ", "*.xlsx"))
        button1.pack()

        # Json Template Input
        json_template_label = tk.Label(self.window, text="\nJson Template Path:")
        json_template_label.pack()
        self.json_template_path = tk.Entry(self.window, width=int(self.width/20))
        self.json_template_path.pack()
        button2 = tk.Button(self.window, text="Select File", command=lambda: select_file_path(self.json_template_path, "Json Template File: ", "*.json"))
        button2.pack()
        
        # Row Range Input
        range_label = tk.Label(self.window, text="\nRow Range (both included, no input means read all rows):")
        range_label.pack()
        start_label = tk.Label(self.window, text="Start Row Num:")
        start_label.pack()
        self.start_entry = tk.Entry(self.window, justify="center")
        self.start_entry.pack()
        end_label = tk.Label(self.window, text="End Row Num:")
        end_label.pack()
        self.end_entry = tk.Entry(self.window, justify="center")
        self.end_entry.pack()       
                
        # Empty Line1
        empty_line1 = tk.Label(self.window, text="\n")
        empty_line1.pack()

        # Transform Button
        transform = tk.Button(self.window, text="Transform", command=lambda: self.transform_to_json())
        transform.pack()

        # Scrolled Preview
        preview_label = tk.Label(self.window, text="\nPreview:")
        preview_label.pack()
        self.preview_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=int(self.width/12), height=int(self.height/50))
        self.preview_area.pack()
        
        # Json File Output
        export_label = tk.Label(self.window, text="\nJson Output Path:")
        export_label.pack()
        self.export_path = tk.Entry(self.window, width=int(self.width/20))
        self.export_path.pack()
        button3 = tk.Button(self.window, text="Select File", command=lambda: select_file_path(self.export_path))
        button3.pack()

        # Empty Line2
        empty_line3 = tk.Label(self.window, text="\n")
        empty_line3.pack()

        # Write In Json File
        write_json = tk.Button(self.window, text="Write Into File", command=self.write_in_json)
        write_json.pack()
    
    def transform_to_json(self):
        row_range = None
        try:
            row_range = (int(self.start_entry.get()) - 2, int(self.end_entry.get()) - 1)
        except:
            print("Enter correct range!")
          
        self.generator.import_dataset(self.excel_path.get())
        self.generator.import_template(self.json_template_path.get())
        self.generator.generate_json(g_range=row_range)
        
        self.preview_area.delete("1.0", tk.END)
        if(row_range == None):
            row_range = (0, self.generator.data_size)
            
        for i in range(*row_range):
            self.preview_area.insert(tk.END, f"[Row: {i + 2}]:\n" + self.generator.pick_preview(i) + "\n\n")
                          
    def write_in_json(self):
        target_dir = self.export_path.get()
        
        if(self.generator.buffer == [] or target_dir == ''):
            return
        
        self.generator.export_json(target_dir)
        self.preview_area.delete("1.0", tk.END)
        

        