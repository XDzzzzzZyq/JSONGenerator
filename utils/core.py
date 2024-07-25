import json
import copy

import utils.fileIO as IO
import utils.process as PS
import utils.project as PJ

class JSONGenerator:
    def __init__(self):
        self.task = PJ.Task()

        self.name = ""
        self.template: dict = None
        self.dataset: list[dict] = None
        self.data_size: int = -1
        self.data_columns: list = None
        self.links: dict = None
        self.option_list = dict()
        self.decoder = True
        self.previews = []

    def import_template(self, template_dir: str):
        self.template = IO.read_json(template_dir)
        self.task.templ_path = template_dir

    def import_dataset(self, excel_dir: str):
        self.dataset, self.data_columns, self.data_size = IO.read_excel(excel_dir)
        self.name = excel_dir.split("/")[-1].split(".")[0]

        # column-wise data pre-processing
        self.option_list = dict()
        for column in self.data_columns:
            self.option_list[column] = PS.Options()

        self.previews = [dict() for _ in range(self.data_size)]
        self.task.excel_path = excel_dir

    def generate_json(self, g_range: tuple[int, int] = None, decoder: bool = True):
        if g_range is None:
            g_range = (0, self.data_size)

        self.decoder = decoder

        self.links = PS.parse_links(self.template, self.data_columns)
        self.dataset = PS.process_options(self.dataset, self.option_list)

        for i in range(*g_range):
            data = self.dataset[i]
            raw = copy.deepcopy(self.template)

            for link_name, link in self.links.items():
                print(link)
                raw = IO.update_json_dict(raw, link, data[link_name])

            self.previews[i] = raw

    def export_json(self, target_dir: str, g_range: tuple[int, int] = None, one_file: bool = False):
        if g_range is None:
            g_range = (0, self.data_size)

        one_file_list = []
        for i in range(*g_range):
            if(self.previews[i] != {}):
                if one_file:
                    one_file_list.append(self.previews[i])
                else:    
                    if self.previews[i].get("id") is not None:
                        id = self.previews[i]["id"]
                        IO.write_json(self.previews[i], f"{target_dir}/{self.name}/{id}.json", self.decoder)
                    else:
                        IO.write_json(self.previews[i], f"{target_dir}/{self.name}/{i}.json", self.decoder)

        if one_file and len(one_file_list) > 0:
            IO.write_json(one_file_list, f"{target_dir}/{self.name}.json", 0, self.decoder)

        for dict in self.previews:
            if dict != {}:
                dict.clear()

        # DEBUG: Print Summary
        print(f"total count: {g_range[1] - g_range[0]}")
        print(f"to folder: {target_dir}")

        self.task.export_path = target_dir

    def pick_preview(self, index: int, indent: int = 4) -> str:
        return json.dumps(self.previews[index], indent=indent, ensure_ascii=not self.decoder)

    def search(self, path: str, value: any) -> int:
        for i in range(self.data_size):
            if self.previews[path] is value:
                return i
        return -1
