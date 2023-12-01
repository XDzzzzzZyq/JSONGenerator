import pandas as pd
import os


class Options:
    def __init__(self):
        self.remove_spaces = False
        self.remove_ext_name = False
        self.number_to_string = False
        self.string_to_number = False
        self.expression: str = None # e.g. 'str(x)+".png"'


def process_column(datacol: pd.DataFrame, opt: Options) -> pd.DataFrame:
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
