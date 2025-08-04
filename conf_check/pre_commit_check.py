import os
import glob
import json
import yaml
import sys
from cerberus import Validator
import logging

DEFAULT_CHECK_DIR = os.path.dirname(os.path.dirname(__file__)).replace("/.", "", 1)
DEFAILT_SCHEMA = os.path.join(DEFAULT_CHECK_DIR, "conf_schema", "schema_fp.json")

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(levelname)s: %(message)s')


def get_all_yaml(root=DEFAULT_CHECK_DIR):
    path_join = os.path.join(root, "**", "*.yaml")
    return glob.glob(path_join, recursive=True)

if __name__ == "__main__":
    logging.info("Custom hook started.")
    logging.info(__file__)
    logging.info(DEFAULT_CHECK_DIR)
    logging.info(DEFAILT_SCHEMA)
    yaml_list = get_all_yaml()

    # with open(DEFAILT_SCHEMA, "r", encoding="utf-8") as f:
    #     ref_list = json.load(f)


    for yaml_fp in yaml_list:
        logging.info(yaml_fp)
        ref_fp = yaml_fp.replace("network_configs", "conf_schema/schema/network_configs")
        ref_fp = ref_fp.replace(".yaml", ".json")
        with open(ref_fp, "r", encoding="utf-8") as f:
            validate_schema = json.load(f)
        v = Validator(validate_schema)

        with open(yaml_fp, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        result = v.validate(data)
        #logging.info(result)
        if result is False:
            logging.info(v.errors)
            raise SystemExit(1)
    raise SystemExit(0)
