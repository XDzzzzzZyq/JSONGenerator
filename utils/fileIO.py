import pandas as pd
from jsonpath_ng import jsonpath, parse
import os
import json


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
    loaded_excel = pd.read_excel(excel_file_path)

    return loaded_excel, loaded_excel.columns, len(loaded_excel)


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

    def to_str_path(path: list):
        if path is None:
            return None
        return "$." + ".".join(path)

    links = dict()

    for column in columns:
        links[column] = to_str_path(find_path(template, column))

    return links


def write_json(json_obj: dict, json_file_path: str):
    dir = os.path.dirname(json_file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(json_file_path, 'w') as json_file:
        json.dump(json_obj, json_file, indent=4)


if __name__ == "__main__":
    # Read
    json_r = read_json("../example/002.json")
    excel_r, columns, num = read_excel("../example/test.xlsx")

    print(json_r)
    print(excel_r)
    print(columns)
    print(num)

    links = parse_links(json_r, columns)
    print(links)

    # Write
    write_json(json_r, "../example/result/003.json")
