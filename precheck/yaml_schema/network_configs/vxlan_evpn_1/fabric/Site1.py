import precheck.pattern_regex as custom_regex
import precheck.pattern_func as custom_func

schema = {
    "Fabric": {
        "type": "dict",
        "schema": {
            "type": {
                "type": "string"
            },
            "Location": {
                "type": "string"
            }
        }
    },
    "General Parameter": {
        "type": "dict",
        "schema": {
            "BGP ASN": {
                "type": "integer"
            }
        }
    },
    "Resources": {
        "type": "dict",
        "schema": {
            "Underlay Routing Loopback IP Range": {
                "type": "string",
                "regex": custom_regex.IP_MASK_REQUIRED
            },
            "Underlay VTEP Loopback IP Range": {
                "type": "string"
            },
            "Underlay Subnet IP Range": {
                "type": "string"
            }
        }
    },
    "Manageability": {
        "type": "dict",
        "schema": {
            "NTP Server IPs": {
                "type": "string"
            },
            "Syslog Server IPs": {
                "type": "string",
                "regex": custom_regex.MULTIPLE_IP_COMMA_SEP
            },
            "AAA Freeform Config": {
                "type": "dict",
                "schema": {
                    "Freeform": {
                        "type": "string"
                    }
                }
            }
        }
    },
    "Advanced": {
        "type": "dict",
        "schema": {
            "Leaf Freeform Config": {
                "type": "dict",
                "schema": {
                    "Freeform": {
                        "type": "string"
                    }
                }
            },
            "Spine Freeform Config": {
                "type": "dict",
                "schema": {
                    "Freeform": {
                        "type": "string",
                        "check_with": custom_func.check_freeform_exists
                    }
                }
            },
            "Intra-fabric Links Additional Config": {
                "type": "dict",
                "schema": {
                    "Freeform": {
                        "type": "string"
                    }
                }
            }
        }
    }
}
