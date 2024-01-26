import pandas as pd
import os


class Options:
    def __init__(self):
        self.remove_spaces = False
        self.remove_ext_name = False
        self.number_to_string = False
        self.string_to_number = False
        # self.expression: str = None  # e.g. 'str(x)+".png"'
        
def parse_links(template, columns: pd.Index):
    def find_path(json_obj, target_value, current_path=[]):
        """
        Recursively find the first path with the given value in a JSON structure.
        """
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                new_path = current_path + [key]
                if value == target_value:
                    return new_path
                result = find_path(value, target_value, new_path)
                if result:
                    return result
        elif isinstance(json_obj, list):
            for i, value in enumerate(json_obj):
                new_path = current_path + [i]
                if value == target_value:
                    return new_path
                result = find_path(value, target_value, new_path)
                if result:
                    return result
        return None

    # def to_str_path(path: list):
    #     if path is None:
    #         return None
    #     return "$." + ".".join(path)

    links = dict()

    for column in columns:
        links[column] = find_path(template, column)

    return links

def process_value(value: any):
    if type(value) is str:
        if value.startswith('[') and value.endswith(']'):  # e.g. [0,100]
            value_r = value.replace(' ', '').replace(']', '').replace('[', '').split(",")
            if len(value_r) == 2:
                value = [float(v) for v in value_r]

        elif value.startswith('l[') and value.endswith(']'):  # e.g. l["123", "asda", "12313"]
            value = value.replace(' ', '').replace(']', '').replace('l[', '').replace('\"', '').split(",")

    return value


def process_column(datacol: pd.DataFrame, opt: Options) -> pd.DataFrame:
    datacol = datacol.apply(process_value)

    if opt.remove_spaces:
        datacol = datacol.astype(str).str.strip()

    if opt.remove_ext_name:
        datacol = datacol.apply(lambda x: os.path.splitext(x)[0])

    if opt.string_to_number:
        datacol = datacol.astype(float)

    if opt.number_to_string:
        datacol = datacol.astype(str)

    # if opt.expression is not None:
    #     datacol = datacol.apply(lambda x: eval(opt.expression, {'x': x}))

    return datacol


def process(dataset: pd.DataFrame, opt_list: dict[str, Options]) -> pd.DataFrame:
    for column, option in opt_list.items():
        dataset[column] = process_column(dataset[column], option)

    return dataset
