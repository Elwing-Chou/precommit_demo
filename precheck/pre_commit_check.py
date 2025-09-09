import os
import json
import logging
import yaml
import sys
import constants as const
from cerberus import Validator

logging.basicConfig(
    filename="precommit_yaml_check.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# def get_all_yaml(root=YAML_DIR):
#     path_join = os.path.join("**", "*.yaml")
#     fp_list = glob.glob(path_join, recursive=True, root_dir=YAML_DIR)
#     return fp_list


if __name__ == "__main__":
    logging.info("YAML check started.")
    # logging.info(f"args: {sys.argv}")
    yaml_list = sys.argv[1:]

    for yaml_fp in yaml_list:
        if not yaml_fp.startswith("."):
            logging.info(f"Check {yaml_fp}")
            ref_fp = os.path.join(os.path.dirname(__file__),
                                  const.YAML_SCHEMA_SAVE_DIR,
                                  yaml_fp)
            ref_fp = ref_fp.replace(".yaml", ".json")
            with open(ref_fp, "r", encoding="utf-8") as f:
                validate_schema = json.load(f)
            v = Validator(validate_schema)

            with open(yaml_fp, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            result = v.validate(data)
            if result is False:
                logging.info(v.errors)
                raise SystemExit(1)
    raise SystemExit(0)
