from utils import *
import tkinter as tk
from tkinter import filedialog

class Panel:
    def __init__(self, width:int=1200, height:int=720):
        self.width = width
        self.height = height
        self.window = tk.Tk()
        self.window.title("Json Generator")
        self.window.geometry(f"{self.width}x{self.height}")
        self.generator = JSONGenerator() 
        self.widgets = {
            "path": {
                "Excel Data Path": None,
                "Json Template Path": None,
                "Export Path": None
                },
            "interval": {
                "start": None,
                "end": None,
                }, 
            "options": {
                "Remove Spaces": None,
                "Remove Extention": None,
                "String to Number": None,
                "Number to String": None},
            "columns": None,
            "preview": None,
        }

        # self.window.minsize(1200, 720)
        self.create_widgets()

    def create_widgets(self):
        """
        Create various GUI widgets for the Panel.
        """
        # Window Layout: LEFT & RIGHT
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        # UI Initialization
        ## MIDDLE
        self.create_title()
        self.create_write_to_file_button()

        # LEFT
        self.create_scroll_frame()
        # self.create_transform_button()

        # RIGHT
        self.create_path_frame()
        self.create_interval_frame()
        self.create_options_frame()

    def create_title(self):
        """
        Create the title label for the Panel.
        """
        label_title = tk.Label(self.window, text="Json Generator", font=("Arial", 16, "bold italic"), fg="blue")
        label_title.grid(row=0, column=0, columnspan=2, pady=10)

    def create_scroll_frame(self):
        """
        Create the scroll frame containing preview text and buttons.
        """
        # Frame Layout Settings
        scroll_frame = tk.Frame(self.window)
        scroll_frame.grid(row=1, column=0, rowspan=3, padx=10, sticky="nsew")

        scrollbar_title = tk.Label(scroll_frame, text="Preview")
        scrollbar_title.pack(side="top", fill="x")

        transform_button = tk.Button(scroll_frame, text="Transform", command=self.transform_data)
        transform_button.pack(side="bottom")

        # Vertical Scrollbar
        scrollbar_y = tk.Scrollbar(scroll_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        # Horizontal Scrollbar
        scrollbar_x = tk.Scrollbar(scroll_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        preview_text = tk.Text(scroll_frame, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        preview_text.pack(side="left", fill="both", expand=True)
        preview_text.configure(state="disabled")

        self.widgets["preview"] = preview_text
        scrollbar_y.config(command=preview_text.yview)
        scrollbar_x.config(command=preview_text.xview)


    def create_path_frame(self):
        """
        Create the frame for displaying and browsing file paths.
        """    
        # Window Layout Settings
        self.window.rowconfigure(1, weight=1)

        # Frame Layout Settings     
        path_frame = tk.Frame(self.window)
        path_frame.grid(row=1, column=1, pady=10, sticky="nsew")
        path_frame.grid_columnconfigure(1, weight=1)

        # Paths
        for row, label_text in enumerate(self.widgets["path"].keys()):
            label_path = tk.Label(path_frame, text=f"{label_text}:")
            label_path.grid(row=row, column=0, pady=5, padx=5, sticky="e")

            entry_path = tk.Entry(path_frame)
            entry_path.grid(row=row, column=1, pady=5, padx=5, sticky="ew")

            button_browse = tk.Button(path_frame, text="Browse", command=lambda: self.browse(entry_path, label_text))
            button_browse.grid(row=row, column=2, pady=5, padx=5)
            
            self.widgets["path"][label_text] = entry_path

    def create_interval_frame(self):
        """
        Create the frame for specifying row intervals and selecting columns.
        """
        # Window Layout Settings
        self.window.rowconfigure(2, weight=1)

        # Frame Layout Settings
        interval_frame = tk.Frame(self.window)
        interval_frame.grid(row=2, column=1, pady=10, sticky="nsew")
        interval_frame.grid_columnconfigure(1, weight=1)

        # Start Row
        label_start_row = tk.Label(interval_frame, text="Start Row:")
        label_start_row.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        entry_start_row = tk.Entry(interval_frame)
        entry_start_row.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        self.widgets["interval"]["start"] = entry_start_row

        # End Row
        label_end_row = tk.Label(interval_frame, text="End Row:")
        label_end_row.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        entry_end_row = tk.Entry(interval_frame)
        entry_end_row.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        self.widgets["interval"]["end"] = entry_end_row
        
        # Column Selection
        label_result = tk.Label(interval_frame, text="Select Column:")
        label_result.grid(row=2, column=0, pady=5, padx=5, sticky="e")
        
        result_frame = tk.Frame(interval_frame)
        result_frame.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        
        scrollbar_y = tk.Scrollbar(result_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        result_listbox = tk.Listbox(result_frame, yscrollcommand=scrollbar_y.set, selectmode=tk.SINGLE)
        result_listbox.pack(side="left", fill="both", expand=True)
        result_listbox.bind("<<ListboxSelect>>", self.show_options)

        self.widgets["columns"] = result_listbox
        scrollbar_y.config(command=result_listbox.yview)

    def create_options_frame(self):
        """
        Create the frame for displaying and interacting with column options.
        """
        # Window Layout Settings
        self.window.rowconfigure(3, weight=1)

        # Frame Layout Settings
        options_frame = tk.Frame(self.window)
        options_frame.grid(row=3, column=1, pady=10, sticky="nsew")
        options_frame.grid_columnconfigure(1, weight=1)

        # Column Options
        options_label = tk.Label(options_frame, text="Column Options:")
        options_label.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        container_frame = tk.Frame(options_frame)
        container_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

        opt_names = list(self.widgets["options"].keys())
        pairs = {(0,0): opt_names[0],
                (0,1): opt_names[1],
                (1,0): opt_names[2],
                (1,1): opt_names[3]}

        for i in range(2):
            for j in range(2):
                option_button = tk.Button(container_frame, text=pairs[(i,j)], command=lambda pair=pairs[(i, j)]: self.option_event(pair))
                option_button.grid(row=i, column=j, pady=5, padx=5, sticky="nsew")

                container_frame.grid_rowconfigure(i, weight=1)
                container_frame.grid_columnconfigure(j, weight=1)
                
                self.widgets["options"][pairs[(i,j)]] = option_button

    def create_transform_button(self):
        """
        Create the Transform button.
        """
        transform_button_frame = tk.Frame(self.window)
        transform_button_frame.grid(row=4, column=0, pady=10)

        transform_button = tk.Button(transform_button_frame, text="Transform", command=self.transform_data)
        transform_button.pack(side="left")

    def create_write_to_file_button(self):
        """
        Create the Write to File button.
        """
        # Window Layout Settings
        self.window.grid_rowconfigure(4, weight=1)
        
        # Frame Layout Settings
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        write_button = tk.Button(button_frame, text="Write to File", command=self.write_to_file)
        write_button.pack(side="right")

    def write_to_file(self):
        """
        Write generated JSON data to a file.
        """
        target_dir = self.widgets["path"]["Export Path"].get()
        row_range = None
        
        if(self.generator.previews == [] or target_dir == ''):
            return  
        
        try:
            lower = int(self.widgets["interval"]["start"].get()) - 2
            lower = max(lower, 0)
        except:
            lower = 0
        
        try:
            upper = int(self.widgets["interval"]["end"].get()) - 1
            upper = min(upper, self.generator.data_size)
        except:
            upper = self.generator.data_size
        
        row_range = (lower, upper)
        
        self.generator.export_json(target_dir, g_range=row_range)
        self.widgets["preview"].configure(state="normal")
        self.widgets["preview"].delete("1.0", tk.END)
        self.widgets["preview"].configure(state="disabled")

    def transform_data(self):
        """
        Transform data to JSON and display it in the preview area.
        """
        # get row range
        row_range = None
        try:
            lower = int(self.widgets["interval"]["start"].get()) - 2
            lower = max(lower, 0)
        except:
            lower = 0
        
        try:
            upper = int(self.widgets["interval"]["end"].get()) - 1
            upper = min(upper, self.generator.data_size)
        except:
            upper = self.generator.data_size
            
        row_range = (lower, upper)

        # transform to json
        self.generator.generate_json(g_range=row_range)
        
        self.widgets["preview"].configure(state="normal")
        self.widgets["preview"].delete("1.0", tk.END)
        self.widgets["preview"].configure(state="disabled")
        if(row_range == None):
            row_range = (0, self.generator.data_size)
            
        for i in range(*row_range):
            self.widgets["preview"].configure(state="normal")
            self.widgets["preview"].insert(tk.END, f"[Row: {i + 2}]:\n" + self.generator.pick_preview(i) + "\n\n")
            self.widgets["preview"].configure(state="disabled")

    def option_event(self, name: str):
        """
        Handle events related to column options.

        Parameters:
        - name (str): Name of the column option.
        """
        try:
            options_state = self.generator.option_list[self.widgets["columns"].get(self.widgets["columns"].curselection())]
        except:
            return
        
        if name == "Remove Spaces":
            options_state.remove_spaces = not options_state.remove_spaces
        elif name == "Remove Extention":
            options_state.remove_ext_name = not options_state.remove_ext_name
        elif name == "String to Number":
            options_state.string_to_number = not options_state.string_to_number
            options_state.number_to_string = False
        elif name == "Number to String":
            options_state.number_to_string = not options_state.number_to_string
            options_state.string_to_number = False
        
        self.show_options()  
       
    def show_options(self, event=None):
        """
        Show the current state of column options.
        """
        try:
            options_state = self.generator.option_list[self.widgets["columns"].get(self.widgets["columns"].curselection())]
        except:
            return
        
        if options_state.remove_spaces:
            self.widgets["options"]["Remove Spaces"].config(fg="red")
        else:
            self.widgets["options"]["Remove Spaces"].config(fg="black")
            
        if options_state.remove_ext_name:
            self.widgets["options"]["Remove Extention"].config(fg="red")
        else:
            self.widgets["options"]["Remove Extention"].config(fg="black")
            
        if options_state.string_to_number:
            self.widgets["options"]["String to Number"].config(fg="red")
        else:
            self.widgets["options"]["String to Number"].config(fg="black")
            
        if options_state.number_to_string:
            self.widgets["options"]["Number to String"].config(fg="red")
        else:
            self.widgets["options"]["Number to String"].config(fg="black")


    def browse(self, entry_widget:tk.Entry, kind: str = ""):
        """
        Open a file dialog for browsing and selecting a file path. Then import it.

        Parameters:
        - entry_widget: The entry widget to display the selected file path.
        - kind: The kind (str) of the path to import.
        """  
        if kind == "Excel Data Path":
            # Excel path
            path = filedialog.askopenfilename(
                title="Select An Excel Dataset",
                filetypes=[("Excel File", "*.xlsx")])
            
            if path == "":
                return
            
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)
            
            self.generator.import_dataset(self.widgets["path"]["Excel Data Path"].get())
            self.widgets["columns"].delete(0, tk.END)

            for col in self.generator.data_columns:
                self.widgets["columns"].insert(tk.END, col)
                
        elif kind == "Json Template Path":
            # Json Template path
            path = filedialog.askopenfilename(
                title="Select A Json Template",
                filetypes=[("Json File", "*.json")])
            
            if path == "":
                return
            
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)
            
            self.generator.import_template(self.widgets["path"]["Json Template Path"].get())
            
        elif kind == "Export Path":
            # export path
            path = filedialog.askdirectory()
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)
            
    def run(self):
        """
        Run the main loop of the tkinter window.
        """
        self.window.mainloop()