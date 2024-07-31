import json
import copy

import utils.fileIO as IO
import utils.process as PS
import utils.project as PJ

class JSONGenerator:
    def __init__(self):
        self.task = PJ.Task()

        self.name = ""
        self.current_sheet = ""
        self.template: dict = None
        self.data: dict = None
        self.links: dict = None
        self.transforms: dict = None
        self.option_list = {}
        self.previews = []
        self.decoder = True

    def import_template(self, template_dir: str):
        self.template = IO.read_json(template_dir)
        self.task.templ_path = template_dir

    def import_dataset(self, excel_dir: str):
        self.data = IO.read_excel(excel_dir)
        self.name = excel_dir.split("/")[-1].split(".")[0]

        # column-wise data pre-processing
        for sheetname in self.data.keys():
            self.option_list[sheetname] = {}
            for column in self.data[sheetname]["data_columns"]:
                self.option_list[sheetname][column] = PS.Options()
            
        self.task.excel_path = excel_dir

    def generate_json(self, sheetname: str, generate_range: tuple[int, int] = None, decoder: bool = True):        
        if sheetname == "None":
            return
        
        if generate_range is None:
            generate_range = (0, self.data[sheetname]["data_size"])
            
        self.decoder = decoder
        self.current_sheet = sheetname

        self.links = PS.parse_links(self.template, self.data[sheetname]["data_columns"])
        self.transforms = PS.process_options(self.data[sheetname]["dataset"], self.option_list[sheetname])
        self.previews = [{} for _ in range(self.data[sheetname]["data_size"])]

        for i in range(*generate_range):
            data = self.transforms[i]
            raw = copy.deepcopy(self.template)

            for link_name, link in self.links.items():
                # DEBUG: Print Excel Column and Template Value link
                print(link)
                raw = IO.update_json_dict(raw, link, data[link_name])

            self.previews[i] = raw

    def export_json(self, target_dir: str, generate_range: tuple[int, int] = None, one_file: bool = False):
        if generate_range is None:
            generate_range = (0, self.data_size)

        one_file_list = []
        export_dir = f"{target_dir}/{self.name}" if len(self.data.keys()) == 1 else f"{target_dir}/{self.name}/{self.current_sheet}"
        for i in range(*generate_range):
            if(self.previews[i] != {}):
                if one_file:
                    one_file_list.append(self.previews[i])
                else:    
                    if self.previews[i].get("id") is not None:
                        id = self.previews[i]["id"]
                        IO.write_json(self.previews[i], f"{export_dir}/{id}.json", self.decoder)
                    else:
                        IO.write_json(self.previews[i], f"{export_dir}/{i}.json", self.decoder)

        if one_file and len(one_file_list) > 0:
            IO.write_json(one_file_list, f"{target_dir}/{self.name}-{self.current_sheet}.json", 0, self.decoder)

        for dict in self.previews:
            if dict != {}:
                dict.clear()

        # DEBUG: Print Summary
        print(f"total count: {generate_range[1] - generate_range[0]}")
        print(f"to folder: {target_dir}")

        self.task.export_path = target_dir

    def pick_preview(self, index: int, indent: int = 4) -> str:
        return json.dumps(self.previews[index], indent=indent, ensure_ascii=not self.decoder)

    def search(self, path: str, value: any) -> int:
        for i in range(self.data_size):
            if self.previews[path] is value:
                return i
        return -1
