import os
import copy


class Options:
    def __init__(self):
        self.remove_spaces = False
        self.remove_ext_name = False
        self.number_to_string = False
        self.string_to_number = False
        # self.expression: str = None  # e.g. 'str(x)+".png"'

def __process_list(list_string: str):
    ## check if the string is a list
    if not list_string.startswith("[") or not list_string.endswith("]") :
        return list_string
    
    ## preprocess the string
    items = list_string.strip('[]').split(',')

    # Process each item
    for i, item in enumerate(items):
        if item.startswith('['):
            items[i] = __process_list(item)
        else:
            # convert numeric items to int or float
            try:
                items[i] = int(item)
            except ValueError:
                try:
                    items[i] = float(item)
                except ValueError:
                    items[i] = item.strip('\'" ')

    return items


def __process_column(dataset: list[dict], column: str, opt: Options) -> list[dict]:
    processed_dataset = copy.deepcopy(dataset)
    
    for row in range(len(processed_dataset)):
        ## process options
        if opt.remove_spaces:
            processed_dataset[row][column] = str(processed_dataset[row][column]).replace("\t", "").replace(" ", "")

        if opt.remove_ext_name:
            processed_dataset[row][column] = os.path.splitext(processed_dataset[row][column])[0]

        if opt.string_to_number:
            processed_dataset[row][column] = float(processed_dataset[row][column])

        if opt.number_to_string:
            processed_dataset[row][column] = str(processed_dataset[row][column])

        # if opt.expression is not None:
        #     processed_dataset[row][column] = eval(processed_dataset[row][column], {'x': x})

        ## process list
        if type(processed_dataset[row][column]) is str:
            processed_dataset[row][column] = __process_list(processed_dataset[row][column])
        
    return processed_dataset


def process_options(dataset: list[dict], opt_list: dict[str, Options]) -> list[dict]:
    processed_dataset = copy.deepcopy(dataset)
    
    for column, options in opt_list.items():
        processed_dataset = __process_column(processed_dataset, column, options)

    return processed_dataset


def parse_links(template, columns: list):
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
