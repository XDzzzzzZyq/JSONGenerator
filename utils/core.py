import pandas as pd
# import jsonpath_ng
# from objectpath import Tree

import utils.fileIO as IO


class Preference:
    def __init__(self):
        self.export_folder: str = None


class JSONGenerator:
    def __init__(self):
        self.template: dict = None
        self.dataset: pd.DataFrame = None
        self.data_size: int = -1
        self.data_columns: pd.Index = None
        self.links: dict = None
        self.preference = Preference()

    def import_template(self, template_dir: str):
        self.template = IO.read_json(template_dir)

        if self.dataset is not None:
            self.links = IO.parse_links(self.template, self.data_columns)

    def import_dataset(self, excel_dir: str):
        self.dataset, self.data_columns, self.data_size = IO.read_excel(excel_dir)

        if self.template is not None:
            self.links = IO.parse_links(self.template, self.data_columns)

    def generate_json(self, target_dir: str, g_range: tuple[int, int] = None):
        if g_range is None:
            g_range = (0, self.data_size)

        if target_dir[-1] != '/':
            target_dir += '/'

        for i in range(*g_range):
            data = self.dataset.iloc[i]
            raw = self.template.copy()

            for link_name, link in self.links.items():
                # code = f"{link} = \'{data[link_name]}\'"
                raw = IO.update_json(raw, link, data[link_name])

            IO.write_json(raw, f"{target_dir}{i}.json")

        print(f"total count: {g_range[1]-g_range[0]}")
        print(f"to folder: {target_dir}")


if __name__ == "__main__":
    generator = JSONGenerator()
    generator.import_template("../example/002.json")
    generator.import_dataset("../example/test.xlsx")

    generator.generate_json("../example/result/")
