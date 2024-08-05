import copy
import tkinter as tk

from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from utils import JSONGenerator as JSG
from utils import Task

class Panel:
    def __init__(self, width:int=1000, height:int=720):     
        self.task = Task()
        self.generator = JSG()    
        self.window = tk.Tk()
        
         # Window Layout: LEFT & RIGHT
        self.window.geometry(f"{width}x{height}")
        self.window.title("Json Generator")
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        
        # Window Events
        self.window.bind_all("<Control-s>", self.save_config)
        self.window.bind_all("<Command-s>", self.save_config)
        self.window.protocol("WM_SAVE_YOURSELF", self.save_config)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self.widgets = {
            "save": None,
            "path": {
                "excel_path": None,
                "templ_path": None,
                "export_path": None,
                },
            "interval": {
                "start": None,
                "end": None,
                }, 
            "options": {
                "remove_spaces": None,
                "remove_ext": None,
                "str_to_num": None,
                "num_to_str": None
                },
            "decoder": None,
            "one_file": None,
            "columns": None,
            "preview": None,
        }

        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        """
        Create various GUI widgets for the Panel.
        """
        # UI Initialization
        ## MIDDLE
        self.create_title_frame()
        self.create_write_to_file_button()

        ## LEFT
        self.create_scroll_frame()

        ## RIGHT
        self.create_path_frame()
        self.create_interval_frame()
        self.create_options_frame()

    def create_title_frame(self):
        """
        Create the title label for the Panel.
        """
        # Frame Layout Settings
        title_frame = tk.Frame(self.window)
        title_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=1)
        title_frame.columnconfigure(2, weight=1)

        # Save Icon Button
        save_icon = tk.Label(title_frame, text="💾", font=("Arial", 16), fg="#00CC00")
        save_icon.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        save_icon.bind("<Button-1>", self.save_config)
        
        self.widgets["save"] = save_icon
        
        # Title Label
        label_title = tk.Label(title_frame, text="Json Generator", font=("Arial", 16, "bold italic"), fg="blue")
        label_title.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

    def create_scroll_frame(self):
        """
        Create the scroll frame containing preview text and buttons.
        """
        # Frame Layout Settings
        scroll_frame = tk.Frame(self.window)
        scroll_frame.grid(row=1, column=0, rowspan=3, padx=10, sticky="nsew")

        # Transform Frame
        transform_frame = tk.Frame(scroll_frame)
        transform_frame.pack(side="bottom", fill="x")
        transform_frame.columnconfigure(0, weight=1)
        transform_frame.columnconfigure(1, weight=1)

        transform_button = tk.Button(transform_frame, text="Transform", command=self.transform_data)
        transform_button.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        decoder = tk.BooleanVar()
        decoder.set(True)
        decode_box = tk.Checkbutton(transform_frame, text="Decode", variable=decoder, command=lambda: self.set_config("enable_decoder", decoder))
        decode_box.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        self.widgets["decoder"] = decoder

        # Preview Text
        ## Title
        scrollbar_title = tk.Label(scroll_frame, text="Preview")
        scrollbar_title.pack(side="top", fill="x")

        ## Vertical Scrollbar
        scrollbar_y = tk.Scrollbar(scroll_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        ## Horizontal Scrollbar
        scrollbar_x = tk.Scrollbar(scroll_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        ## Text Area
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
        def create_path_entry(self: Panel, parent: tk.Frame, label_text:str, row: int)-> tk.Entry:
            label_path = tk.Label(parent, text=f"{label_text}:")
            label_path.grid(row=row, column=0, pady=5, padx=5, sticky="e")

            entry_path = tk.Entry(parent)
            entry_path.grid(row=row, column=1, pady=5, padx=5, sticky="ew")
            entry_path.bind("<KeyRelease>", lambda event: self.set_config(label_text, entry_path))

            button_browse = tk.Button(parent, text="Browse", command=lambda: self.browse(entry_path, label_text))
            button_browse.grid(row=row, column=2, pady=5, padx=5)
            
            self.widgets["path"][label_text] = entry_path


        # Window Layout Settings
        self.window.rowconfigure(1, weight=1)

        # Frame Layout Settings     
        path_frame = tk.Frame(self.window)
        path_frame.grid(row=1, column=1, pady=10, sticky="nsew")
        path_frame.grid_columnconfigure(1, weight=1)

        # Paths
        for row, label_text in enumerate(self.widgets["path"].keys()):
            create_path_entry(self, path_frame, label_text, row)

        # Import
        import_button = tk.Button(path_frame, text="Import", command=self.import_all)
        import_button.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky="ew")


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
        interval_frame.grid_columnconfigure(3, weight=1)
        interval_frame.grid_columnconfigure(5, weight=1)
        
        # Sheet Selection
        label_dropdown = tk.Label(interval_frame, text="Select Sheet:")
        label_dropdown.grid(row=0, column=0, pady=5, padx=5, sticky="e")
        
        select_sheet = ttk.Combobox(interval_frame, state='readonly')
        select_sheet['values'] = ["None"]
        select_sheet.set("None")
        select_sheet.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        select_sheet.bind("<<ComboboxSelected>>", self.select_sheet)
        
        self.widgets["interval"]["sheet"] = select_sheet

        # Start Row
        label_start_row = tk.Label(interval_frame, text="Start Row:")
        label_start_row.grid(row=0, column=2, pady=5, padx=5, sticky="e")

        entry_start_row = tk.Entry(interval_frame)
        entry_start_row.bind("<KeyRelease>", lambda event: self.set_config("start_row", entry_start_row))
        entry_start_row.grid(row=0, column=3, pady=5, padx=5, sticky="ew")
        
        self.widgets["interval"]["start"] = entry_start_row

        # End Row
        label_end_row = tk.Label(interval_frame, text="End Row:")
        label_end_row.grid(row=0, column=4, pady=5, padx=5, sticky="e")

        entry_end_row = tk.Entry(interval_frame)
        entry_end_row.bind("<KeyRelease>", lambda event: self.set_config("end_row", entry_end_row))
        entry_end_row.grid(row=0, column=5, pady=5, padx=5, sticky="ew")
        
        self.widgets["interval"]["end"] = entry_end_row
        
        # Column Selection
        label_result = tk.Label(interval_frame, text="Select Column:")
        label_result.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        
        result_frame = tk.Frame(interval_frame)
        result_frame.grid(row=1, column=1, columnspan=5, pady=5, padx=5, sticky="ew")
        
        scrollbar_y = tk.Scrollbar(result_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        result_listbox = tk.Listbox(result_frame, yscrollcommand=scrollbar_y.set, selectmode=tk.SINGLE)
        result_listbox.pack(side="left", fill="both", expand=True)
        result_listbox.bind("<<ListboxSelect>>", self.color_options)

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

        opt_names = ["Remove Spaces", "Remove Extension", "String to Number", "Number to String"]
        names = {(0,0): opt_names[0],
                 (0,1): opt_names[1],
                 (1,0): opt_names[2],
                 (1,1): opt_names[3]}
        
        opt_keys = list(self.widgets["options"].keys())     
        keys = {(0,0): opt_keys[0],
                (0,1): opt_keys[1],
                (1,0): opt_keys[2],
                (1,1): opt_keys[3]}

        for i in range(2):
            for j in range(2):
                option_button = tk.Button(container_frame, text=names[(i,j)], command=lambda key=keys[(i, j)]: self.toggle_option(key))
                option_button.grid(row=i, column=j, pady=5, padx=5, sticky="nsew")

                container_frame.grid_rowconfigure(i, weight=1)
                container_frame.grid_columnconfigure(j, weight=1)
                
                self.widgets["options"][keys[(i,j)]] = option_button

    def create_write_to_file_button(self):
        """
        Create the Write to File button.
        """
        # Window Layout Settings
        self.window.grid_rowconfigure(4, weight=1)
        
        # Frame Layout Settings
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        write_button = tk.Button(button_frame, text="Write to File", command=self.write_to_file)
        write_button.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        one_file = tk.BooleanVar()
        one_file.set(False)
        one_file_box = tk.Checkbutton(button_frame, text="Export One File", variable=one_file, command=lambda: self.set_config("export_one_file", one_file))
        one_file_box.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        self.widgets["one_file"] = one_file

    def write_to_file(self):
        """
        Write generated JSON data to a file.
        """
        target_dir = self.widgets["path"]["export_path"].get()
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
            upper = min(upper, self.generator.data[self.generator.current_sheet]["data_size"])
        except:
            upper = self.generator.data[self.generator.current_sheet]["data_size"]
        
        row_range = (lower, upper)
        
        self.generator.export_json(target_dir, generate_range=row_range, one_file=self.widgets["one_file"].get())
        self.widgets["preview"].configure(state="normal")
        self.widgets["preview"].delete("1.0", tk.END)
        self.widgets["preview"].configure(state="disabled")

    def transform_data(self):
        """
        Transform data to JSON and display it in the preview area.
        """
        
        # get the sheet name
        sheetname = self.widgets["interval"]["sheet"].get()
                
        # get row range
        row_range = None
        try:
            lower = int(self.widgets["interval"]["start"].get()) - 2
            lower = max(lower, 0)
        except:
            lower = 0
        
        try:
            upper = int(self.widgets["interval"]["end"].get()) - 1
            upper = min(upper, self.generator.data[sheetname]["data_size"])
        except:
            upper = self.generator.data[sheetname]["data_size"]
            
        row_range = (lower, upper)

        # transform to json 
        self.generator.generate_json(sheetname=sheetname, generate_range=row_range, decoder=self.widgets["decoder"].get())
        
        self.widgets["preview"].configure(state="normal")
        self.widgets["preview"].delete("1.0", tk.END)
        self.widgets["preview"].configure(state="disabled")
        if(row_range == None):
            row_range = (0, self.generator.data[sheetname]["data_size"])
        
        self.widgets["preview"].configure(state="normal")
        self.widgets["preview"].insert(tk.END, f"<Sheet: {sheetname}>\n\n")
        for i in range(*row_range):
            preview = self.generator.pick_preview(i)
            if preview != '{}':
                self.widgets["preview"].insert(tk.END, f"[Row: {i + 2}]:\n" + preview + "\n\n")
        self.widgets["preview"].configure(state="disabled")

    def toggle_option(self, widget_key: str):
        """
        Handle events related to column options.

        Parameters:
        - name (str): Name of the column option.
        """
        sheetname = self.widgets["interval"]["sheet"].get()
        selection = self.widgets["columns"].curselection()
        if selection:
            column = self.widgets["columns"].get(selection)
            options_state = self.generator.option_list[sheetname][column]
        else:
            return

        if widget_key == "remove_spaces":
            options_state.remove_spaces = not options_state.remove_spaces          
        elif widget_key == "remove_ext":
            options_state.remove_ext_name = not options_state.remove_ext_name
        elif widget_key == "str_to_num":
            options_state.string_to_number = not options_state.string_to_number
            options_state.number_to_string = False
        elif widget_key == "num_to_str":
            options_state.number_to_string = not options_state.number_to_string
            options_state.string_to_number = False
            
        options = {}
        for sheet in self.generator.option_list.keys():
            sheet_options = {}
            for col in self.generator.option_list[sheet].keys():
                opt = self.generator.option_list[sheet][col]
                col_options = {}
                
                if opt.remove_spaces:
                    col_options["remove_spaces"] = True
                if opt.remove_ext_name:
                    col_options["remove_ext"] = True
                if opt.string_to_number:
                    col_options["str_to_num"] = True
                if opt.number_to_string:
                    col_options["num_to_str"] = True
                
                if col_options:
                    sheet_options[col] = col_options
            
            if sheet_options:
                options[sheet] = sheet_options
        
        self.set_config("options", copy.deepcopy(options), is_widget=False)     
        self.color_options()  
       
    def color_options(self, event=None):
        """
        Show the current state of column options.
        """
        
        sheetname = self.widgets["interval"]["sheet"].get()
        selection = self.widgets["columns"].curselection()     
        if selection:
            selected_index = selection[0]
            options_state = self.generator.option_list[sheetname][self.widgets["columns"].get(selection)]
        else:
            return
        
        options_count = 0
        
        if options_state.remove_spaces:
            self.widgets["options"]["remove_spaces"].config(fg="red")
            options_count += 1
        else:
            self.widgets["options"]["remove_spaces"].config(fg="black")
            
        if options_state.remove_ext_name:
            self.widgets["options"]["remove_ext"].config(fg="red")
            options_count += 1
        else:
            self.widgets["options"]["remove_ext"].config(fg="black")
            
        if options_state.string_to_number:
            self.widgets["options"]["str_to_num"].config(fg="red")
            options_count += 1
        else:
            self.widgets["options"]["str_to_num"].config(fg="black")
            
        if options_state.number_to_string:
            self.widgets["options"]["num_to_str"].config(fg="red")
            options_count += 1
        else:
            self.widgets["options"]["num_to_str"].config(fg="black")

        if options_count > 0:
            self.widgets["columns"].itemconfig(selected_index, {'fg': 'red'})
        elif self.widgets["columns"].itemcget(selected_index, 'fg') == 'red':
            col_text = self.widgets["columns"].get(selected_index)
            self.widgets["columns"].delete(selected_index)
            self.widgets["columns"].insert(selected_index, col_text)
            self.widgets["columns"].selection_set(selected_index)
            self.widgets["columns"].activate(selected_index)

    def select_sheet(self, event=None):
        """
        The event happens when selecting the excel sheet.
        """
        
        # Clear Options Color
        for button in self.widgets["options"].values():
            button.config(fg="black")
        
        # Upload Project Task
        self.set_config("select_sheet", self.widgets["interval"]["sheet"])
        if (self.widgets["interval"]["sheet"].get() == "None"):
            self.set_config("options", {}, is_widget=False)
        
        # Update Columns
        sheetname = self.widgets["interval"]["sheet"].get()
        self.widgets["columns"].delete(0, tk.END)
        if sheetname != "None":
            for col in self.generator.data[sheetname]["data_columns"]:
                self.widgets["columns"].insert(tk.END, col)
                
                options_state = self.generator.option_list[sheetname][col]
                if options_state.remove_spaces or options_state.remove_ext_name or options_state.string_to_number or options_state.number_to_string:
                    selected_index = self.widgets["columns"].get(0, tk.END).index(col)
                    self.widgets["columns"].itemconfig(selected_index, {'fg': 'red'})               

    def browse(self, entry_widget:tk.Entry, kind: str = ""):
        """
        Open a file dialog for browsing and selecting a file path. Then import it.

        Parameters:
        - entry_widget: The entry widget to display the selected file path.
        - kind: The kind (str) of the path to import.
        """  
        if kind == "excel_path":
            # Excel path
            path = filedialog.askopenfilename(
                title="Select An Excel Dataset",
                filetypes=[("Excel File", "*.xlsx")])
            
            if path == "":
                return
            
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)
            
            self.set_config("excel_path", self.widgets["path"]["excel_path"])
                
        elif kind == "templ_path":
            # templ_path
            path = filedialog.askopenfilename(
                title="Select A Json Template",
                filetypes=[("Json File", "*.json")])
            
            if path == "":
                return
            
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)
            
            self.set_config("templ_path", self.widgets["path"]["templ_path"])
            
        elif kind == "export_path":
            # export path
            path = filedialog.askdirectory(
                title="Select Export File")
            
            if path == "":
                return
            
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)
            
            self.set_config("export_path", self.widgets["path"]["export_path"])
    
    def import_all(self):
        """
        Imports Json template and Excel source
        """
        
        # Import Excel Data
        excel_path = self.widgets["path"]["excel_path"].get()

        if excel_path != "":
            self.generator.import_dataset(excel_path)
            sheetnames = list(self.generator.data.keys())
            self.widgets["interval"]["sheet"]['values'] = ["None"] + sheetnames
            self.widgets["interval"]["sheet"].set(sheetnames[0])
            self.select_sheet()

        # Import Json Template
        json_path = self.widgets["path"]["templ_path"].get()

        if json_path != "":
            self.generator.import_template(json_path)

        # Clear Options Color
        for button in self.widgets["options"].values():
            button.config(fg="black")
            
    def save_config(self, event=None):
        """
        Save the current state of the panel.
        """
        self.task.write_config()
        self.widgets["save"].config(fg="#00CC00")
    
    ### TODO: Maybe move this into another new python file ###
    def load_config(self):
        """
        Load the last saved state of the panel.
        """
        config = self.task.read_config()
        imported = False
        
        # Paths
        if "excel_path" in config:
            self.widgets["path"]["excel_path"].delete(0, tk.END)
            self.widgets["path"]["excel_path"].insert(0, config["excel_path"])
        else:
            self.set_config("excel_path", self.widgets["path"]["excel_path"])
            
        if "templ_path" in config:
            self.widgets["path"]["templ_path"].delete(0, tk.END)
            self.widgets["path"]["templ_path"].insert(0, config["templ_path"])
        else:
            self.set_config("templ_path", self.widgets["path"]["templ_path"])
            
        if "export_path" in config:
            self.widgets["path"]["export_path"].delete(0, tk.END)
            self.widgets["path"]["export_path"].insert(0, config["export_path"])
        else:
            self.set_config("export_path", self.widgets["path"]["export_path"])
            
        # Interval
        if "start_row" in config:
            self.widgets["interval"]["start"].delete(0, tk.END)
            self.widgets["interval"]["start"].insert(0, config["start_row"])
        else:
            self.set_config("start_row", self.widgets["interval"]["start"])
        
        if "end_row" in config:
            self.widgets["interval"]["end"].delete(0, tk.END)
            self.widgets["interval"]["end"].insert(0, config["end_row"])
        else:
            self.set_config("end_row", self.widgets["interval"]["end"])
            
        if "select_sheet" in config:
            if config["select_sheet"] != "None":
                try:
                    self.import_all()
                except:
                    print("Cannot imported sheet from the last saved state.")
                    self.generator.clear_imports()
                finally:
                    imported = True
                    self.widgets["interval"]["sheet"].set(config["select_sheet"])
        else:
            self.set_config("select_sheet", self.widgets["interval"]["sheet"])
            
        # Column Options
        if imported and "options" in config:
                try:
                    options = config["options"]
                    for sheet in options.keys():
                        for col in options[sheet].keys():
                            opt = self.generator.option_list[sheet][col]  
                            
                            if "remove_spaces" in options[sheet][col] and options[sheet][col]["remove_spaces"]:   
                                opt.remove_spaces = True
                            if "remove_ext" in options[sheet][col] and options[sheet][col]["remove_ext"]:
                                opt.remove_ext_name = True
                            if "str_to_num" in options[sheet][col] and options[sheet][col]["str_to_num"]:
                                opt.string_to_number = True
                            if "num_to_str" in options[sheet][col] and options[sheet][col]["num_to_str"]:
                                opt.number_to_string = True
                                
                    self.select_sheet()
                except:
                    print("Cannot load options from the last saved state.")
                    self.generator.clear_imports()
                    self.widgets["interval"]["sheet"]['values'] = ["None"]
                    self.widgets["interval"]["sheet"].set("None")
        else:
            self.set_config("options", {}, is_widget=False)
    
        
        # CheckBoxes
        if "enable_decoder" in config:
            self.widgets["decoder"].set(config["enable_decoder"])
        else:
            self.set_config("enable_decoder", self.widgets["decoder"])
            
        if "export_one_file" in config:
            self.widgets["one_file"].set(config["export_one_file"])
        else:
            self.set_config("export_one_file", self.widgets["one_file"])
            
        # Save Default Values
        if (config == {}):
            self.save_config()
            
    
    def set_config(self, name:str, obj: any, is_widget = True):
        """
        Set the configuration to the project task.
        """
        # Set Save Icon Color
        if is_widget:
            self.task.register(name, obj.get())
        else:
            self.task.register(name, obj)
        
        if (self.task.is_saved()):
            self.widgets["save"].config(fg="#00CC00")
        else:
            self.widgets["save"].config(fg="red")

        
    def close(self):
        """
        Handle the closing event of the window.
        """
        if not self.task.is_saved():
            if not messagebox.askyesno("Save", "Do you want to save the current configuration?"):
                self.window.destroy()
                return
            self.save_config()
        self.window.destroy()
            
    def run(self):
        """
        Run the main loop of the tkinter window.
        """
        self.window.mainloop()