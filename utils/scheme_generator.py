import os
import glob
import json
import yaml

DEFAULT_SAVE_DIR="../conf_schema/schema"
DEFAULT_REFERENCE = "../conf_schema/schema_fp.json"

def get_all_yaml(dir_name=None):
    if dir_name is None:
        root = ".."
    else:
        root = dir_name
    path_join = os.path.join(root, "**", "*.yaml")
    return glob.glob(path_join, recursive=True)


def safe_read_json(fp):
    if not os.path.exists(fp):
        with open(fp, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def convert_to_schema(yaml_list):
    ref_list = safe_read_json(DEFAULT_REFERENCE)
    for yaml_fp in yaml_list:
        if yaml_fp not in ref_list:
            with open(yaml_fp, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file)
            data_schema = infer_cerberus_schema(data)

            if yaml_fp.startswith(".."):
                save_dp = os.path.dirname(yaml_fp.replace("../", "", 1))
            else:
                save_dp = os.path.dirname(yaml_fp)
            save_dir = os.path.join(DEFAULT_SAVE_DIR, save_dp)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            json_fp = os.path.basename(yaml_fp).replace(".yaml", ".json")
            save_fp = os.path.join(save_dir, json_fp)
            print("Save to:", save_fp)
            ref_list[yaml_fp.replace("../", "")] = save_fp.replace("../", "", 1)

            with open(save_fp, "w", encoding="utf-8") as f:
                json.dump(data_schema, f, ensure_ascii=False, indent=4)
    with open(DEFAULT_REFERENCE, "w", encoding="utf-8") as f:
        json.dump(ref_list, f, indent=4, ensure_ascii=False)


def infer_cerberus_schema(data):
    schema = {}
    for key, value in data.items():
        if isinstance(value, dict):
            schema[key] = {'type': 'dict', 'schema': infer_cerberus_schema(value)}
        elif isinstance(value, list):
            if value:  # If list is not empty, infer type of first element
                item_type = type(value[0]).__name__
                # change
                if item_type == 'dict':
                    schema[key] = {'type': 'list',
                                   'schema': {'type': 'dict', 'schema': infer_cerberus_schema(value[0])}}
                else:
                    if item_type == "str":
                        item_type = "string"
                    elif item_type =="int":
                        item_type = "integer"
                    elif item_type == "bool":
                        item_type = "boolean"
                    schema[key] = {'type': 'list', 'schema': {'type': item_type}}
            else:  # Empty list
                schema[key] = {'type': 'list'}
        elif isinstance(value, str):
            schema[key] = {'type': 'string'}
        elif isinstance(value, int):
            schema[key] = {'type': 'integer'}
        elif isinstance(value, float):
            schema[key] = {'type': 'float'}
        elif isinstance(value, bool):
            schema[key] = {'type': 'boolean'}
        # Add more type handling as needed (e.g., datetime)
    return schema



if __name__ == "__main__":
    yaml_list = get_all_yaml()
    convert_to_schema(yaml_list)
