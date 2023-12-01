import pandas as pd
import os


class Options:
    def __init__(self):
        self.remove_spaces = False
        self.remove_ext_name = False
        self.number_to_string = False
        self.string_to_number = False
        self.expression: str = None  # e.g. 'str(x)+".png"'


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

    if opt.expression is not None:
        datacol = datacol.apply(lambda x: eval(opt.expression, {'x': x}))

    return datacol


def process(dataset: pd.DataFrame, opt_list: dict[str, Options]) -> pd.DataFrame:
    for column, option in opt_list.items():
        dataset[column] = process_column(dataset[column], option)

    return dataset
