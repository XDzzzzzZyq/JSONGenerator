import os
import utils.fileIO as IO

_registered_properties = []


def register_property(name):
    _registered_properties.append(name)
    
    def getter(self):
        return getattr(self, f"_{self.__class__.__name__}__{name}")
    
    def setter(self, value):
        setattr(self, f"_{self.__class__.__name__}__{name}", value)
        self._update_is_saved()
        
    return property(getter, setter)


def export_properties(task):
    result = dict()
    for prop_name in _registered_properties:
        result[prop_name] = getattr(task, prop_name)

    return result


def import_properties(task, jsonobj):
    _registered_properties.extend(jsonobj.keys())
    for prop_name in _registered_properties:
        setattr(task, prop_name, jsonobj[prop_name])
    
    task._take_snapshot()


class Task():
    def __init__(self):
        self.__config_path = os.path.join(os.getcwd(), "config.jsg")
        self.__original_state = {}
        self.__is_saved = True
        
    def _take_snapshot(self):
        self.__original_state = export_properties(self)

    def _update_is_saved(self):
        current_state = export_properties(self)
        self.__is_saved = current_state == self.__original_state
        
        # DEBUG: Print current state and original state
        print(f"current state: {current_state}")
        print(f"original state: {self.__original_state}")
        print(f"the same?: {self.__is_saved}")
    
    def register(self, name: str, obj):
        prop = register_property(name)
        setattr(self.__class__, name, prop)
        setattr(self, name, obj)

    def read_config(self, path:str = "") -> dict:
        if path == "":
            path = os.path.realpath(self.__config_path)
        else:
            self.__config_path = path   

        json_obj = IO.read_json(path)
        import_properties(self, json_obj)
        
        return json_obj

    def write_config(self):
        json_obj = export_properties(self)

        path = os.path.realpath(self.__config_path)
        self.__is_saved = True
        IO.write_json(json_obj, path)
        
    def is_saved(self):
        return self.__is_saved


if __name__ == "__main__":
    task = Task()
    task.read_config("../example/config.json")
    task.register("name", "JSGeneratorTask")
    task.write_config()
