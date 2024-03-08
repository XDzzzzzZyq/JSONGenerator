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

    def generate_json(self, g_range: tuple[int, int] = None):
        if g_range is None:
            g_range = (0, self.data_size)

        self.links = PS.parse_links(self.template, self.data_columns)
        self.dataset = PS.process_options(self.dataset, self.option_list)

        for i in range(*g_range):
            data = self.dataset[i]
            raw = copy.deepcopy(self.template)

            for link_name, link in self.links.items():
                # code = f"{link} = \'{data[link_name]}\'"
                print(link)
                raw = IO.update_json_dict(raw, link, data[link_name])

            self.previews[i] = raw

    def export_json(self, target_dir: str, g_range: tuple[int, int] = None):

        if g_range is None:
            g_range = (0, self.data_size)

        for i in range(*g_range):
            if(self.previews[i] != {}):
                id = self.previews[i]["identifier"]
                
                if id:
                    IO.write_json(self.previews[i], f"{target_dir}/{self.name}/{id}.json")
                else:
                    raise ValueError("No 'identifier' column!")

        print(f"total count: {g_range[1] - g_range[0]}")
        print(f"to folder: {target_dir}")
        self.task.export_path = target_dir

    def pick_preview(self, index: int, indent: int = 4) -> str:
        return str(json.dumps(self.previews[index], indent=indent))

    def search(self, path: str, value: any) -> int:
        for i in range(self.data_size):
            if self.previews[path] is value:
                return i
        return -1


if __name__ == "__main__":
    generator = JSONGenerator()
    generator.import_template("../example/003.json")
    generator.import_dataset("../example/test2.xlsx")

    generator.generate_json()
    generator.export_json("../example/result/")
    print(generator.pick_preview(0))
