# define func for cerberus check

def check_freeform_exists(field, value, error):
    # need revise
    if "FreeForm" not in value:
        error(field, "Path Invalid")
