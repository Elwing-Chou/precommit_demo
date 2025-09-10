import os
import logging
import yaml
import sys
import importlib
import constants as const
from cerberus import Validator

logging.basicConfig(
    # filename="precommit_yaml_check.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    logging.info("YAML check started.")
    # logging.info(f"args: {sys.argv}")
    yaml_list = sys.argv[1:]

    for yaml_fp in yaml_list:
        if not yaml_fp.startswith("."):
            logging.info(f"Check {yaml_fp}")
            ref_fp = os.path.join(const.YAML_SCHEMA_SAVE_DIR,
                                  yaml_fp)
            module_name = (ref_fp.replace(".yaml", "")
                                 .replace("/", ".")
                                 .replace("\\", "."))
            # with open(ref_fp, "r", encoding="utf-8") as f:
            #     validate_schema = json.load(f)

            try:
                dynamic_module = importlib.import_module(module_name)
                validate_schema = dynamic_module.schema
            except ImportError as e:
                logging.info(f"Error importing module '{module_name}': {e}")

            v = Validator(validate_schema)

            with open(yaml_fp, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            result = v.validate(data)
            if result is False:
                logging.info(v.errors)
                raise SystemExit(1)
    logging.info("YAML check finished.")
    raise SystemExit(0)
