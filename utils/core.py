import json

import pandas as pd
# import jsonpath_ng
# from objectpath import Tree

import utils.fileIO as IO
import utils.process as PS


class Preference:
    def __init__(self):
        self.template_dir: str = None
        self.dataset_dir: str = None
        self.export_folder: str = None


class JSONGenerator:
    def __init__(self):
        self.template: dict = None
        self.dataset: pd.DataFrame = None
        self.data_size: int = -1
        self.data_columns: pd.Index = None
        self.links: dict = None
        self.preference = Preference()
        self.option_list = dict()

    def import_template(self, template_dir: str):
        self.template = IO.read_json(template_dir)
        self.preference.template_dir = template_dir

        if self.dataset is not None:
            self.links = IO.parse_links(self.template, self.data_columns)

    def import_dataset(self, excel_dir: str):
        self.dataset, self.data_columns, self.data_size = IO.read_excel(excel_dir)
        self.preference.dataset_dir = excel_dir

        if self.template is not None:
            self.links = IO.parse_links(self.template, self.data_columns)

        # column-wise data pre-processing
        for column in self.data_columns:
            self.option_list[column] = PS.Options()

        self.buffer = [dict() for _ in range(self.data_size)]

    def generate_json(self, g_range: tuple[int, int] = None):

        if g_range is None:
            g_range = (0, self.data_size)

        self.dataset = PS.process(self.dataset, self.option_list)

        for i in range(*g_range):
            data = self.dataset.iloc[i]
            raw = self.template.copy()

            for link_name, link in self.links.items():
                # code = f"{link} = \'{data[link_name]}\'"
                raw = IO.update_json(raw, link, data[link_name])

            self.buffer[i] = raw

    def export_json(self, target_dir: str, g_range: tuple[int, int] = None):

        if g_range is None:
            g_range = (0, self.data_size)

        if target_dir[-1] != '/':
            target_dir += '/'
        self.preference.export_folder = target_dir

        for i in range(*g_range):
            IO.write_json(self.buffer[i], f"{target_dir}{i}.json")

        print(f"total count: {g_range[1] - g_range[0]}")
        print(f"to folder: {target_dir}")

    def pick_preview(self, index: int, indent: int = 4) -> str:
        return str(json.dumps(self.buffer[index], indent=indent))


if __name__ == "__main__":
    generator = JSONGenerator()
    generator.import_template("../example/002.json")
    generator.import_dataset("../example/test.xlsx")

    generator.generate_json()
    generator.export_json("../example/result/")
    print(generator.pick_preview(0))
