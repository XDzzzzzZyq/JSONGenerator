import pandas as pd
import os
import json
import numpy as np

def read_json(json_file_path: str):
    # Reading JSON file content into a string
    with open(json_file_path, 'r') as json_file:
        json_string = json_file.read()

    json_string = json_string.replace(":,", ": null,")

    # Reading JSON data from a file
    with open(json_file_path, 'r') as json_file:
        loaded_data = json.loads(json_string)

    return loaded_data


def read_excel(excel_file_path: str):
    loaded_excel = pd.read_excel(excel_file_path).dropna(axis=1, how='all')

    return loaded_excel, loaded_excel.columns, len(loaded_excel)


def update_json(tar, path: list[str], value: any):
    """Update JSON dictionnary PATH with VALUE. Return updated JSON"""

    if path is None:
        return tar

    if type(value) is np.int64:
        value = int(value)

    if len(path) == 0:  # the last position
        return value

    tar[path[0]] = update_json(tar[path[0]], path[1:], value)

    return tar


def write_json(json_obj: dict, json_output_path: str):
    dir = os.path.dirname(json_output_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        
    with open(json_output_path, 'w') as json_file:
        json.dump(json_obj, json_file, indent=4)


if __name__ == "__main__":
    # Read
    json_r = read_json("../example/002.json")
    excel_r, columns, num = read_excel("../example/test.xlsx")

    print(json_r)
    print(excel_r)
    print(columns)
    print(num)

    # Write
    write_json(json_r, "../example/result/003.json")
