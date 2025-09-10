# define func for cerberus check
import logging


def check_freeform_exists(field, value, error):
    # need revise
    logging.info(f"check freeform {field} {value} {error}")
    if "Freeform Config" not in value:
        error(field, "Path Invalid")
