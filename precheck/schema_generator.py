import os
import glob
import json
import logging
import sys

import constants as const
import yaml

logging.basicConfig(level=logging.INFO)
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_all_yaml(dir_name=ROOT_DIR):
    path_join = os.path.join("**", "*.yaml")
    fp_list = glob.glob(path_join,
                        recursive=True,
                        root_dir=dir_name)
    return fp_list


def safe_read_json(fp):
    if not os.path.exists(fp):
        with open(fp, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def convert_to_schema(yaml_list, root=ROOT_DIR):
    for yaml_fp in yaml_list:
        logging.info(f"Root {root}")
        yaml_full_path = os.path.join(root,
                                      yaml_fp)
        logging.info(f"Converting {yaml_fp}")

        with open(yaml_full_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
        data_schema = generate_default_schema(data)

        save_dir = os.path.join(os.path.dirname(__file__),
                                const.YAML_SCHEMA_SAVE_DIR,
                                os.path.dirname(yaml_fp))
        save_dir = os.path.abspath(save_dir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        json_fp = os.path.basename(yaml_fp).replace(".yaml", ".py")
        save_fp = os.path.join(save_dir, json_fp)
        logging.info(f"Writing schema to {save_fp}")

        with open(save_fp, "w", encoding="utf-8") as f:
            f.write("schema = ")
            json.dump(data_schema, f, ensure_ascii=False, indent=4)
            f.write("\n")


def generate_default_schema(data):
    schema = {}
    for key, value in data.items():
        if isinstance(value, dict):
            schema[key] = {
                'type': 'dict',
                'schema': generate_default_schema(value)
            }
        elif isinstance(value, list):
            if value:  # If list is not empty, infer type of first element
                item_type = type(value[0]).__name__
                # change
                if item_type == 'dict':
                    schema[key] = {
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'schema': generate_default_schema(value[0])
                        }
                    }
                else:
                    if item_type == "str":
                        item_type = "string"
                    elif item_type == "int":
                        item_type = "integer"
                    elif item_type == "bool":
                        item_type = "boolean"
                    schema[key] = {
                        'type': 'list',
                        'schema': {'type': item_type}
                    }
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
    # add white list for first time
    if len(sys.argv) == 1:
        yaml_list = get_all_yaml()
        convert_to_schema(yaml_list)
    else:
        fp_list = [arg for arg in sys.argv[1:]]
        convert_to_schema(fp_list)
