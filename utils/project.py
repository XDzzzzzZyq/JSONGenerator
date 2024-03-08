import os
from utils import fileIO as IO

_registered_properties = []


def register_property(prop_name):
    _registered_properties.append(prop_name)

    def getter(self):
        return getattr(self, '_Task__' + prop_name)

    def setter(self, value):
        setattr(self, '_Task__is_saved', False)
        setattr(self, '_Task__' + prop_name, value)

    return property(getter, setter)


def export_properties(task):
    result = dict()
    for prop_name in _registered_properties:
        result[prop_name] = getattr(task, prop_name)

    return result


def import_properties(task, jsonobj):
    for prop_name in _registered_properties:
        setattr(task, prop_name, jsonobj[prop_name])


class Task():
    def __init__(self, excel_path="", templ_path="", export_path=""):
        # Configurations
        self.__excel_path = excel_path
        self.__templ_path = templ_path
        self.__export_path = export_path
        self.__export_with_folder = True

        # "Private" Members
        self.__config_path = os.getcwd() + "\\config.json"
        self.__is_saved = False

    # Define all serializable members
    excel_path = register_property("excel_path")
    templ_path = register_property("templ_path")
    export_path = register_property("export_path")
    export_with_folder = register_property("export_with_folder")

    def read_config(self, path):
        json_obj = IO.read_json(path)
        import_properties(self, json_obj)

        self.__config_path = path
        self.__is_saved = False

    def write_config(self):
        json_obj = export_properties(self)

        path = os.path.realpath(self.__config_path)
        self.__is_saved = True
        IO.write_json(json_obj, path)


if __name__ == "__main__":
    task = Task()
    task.read_config("../example/config.json")
    task.excel_path = "123123"
    task.write_config()
