import logging
import sys

logging.basicConfig(level=logging.INFO,
                    stream=sys.stderr,
                    format='%(levelname)s: %(message)s')


if __name__ == "__main__":
    logging.info("Test hook started.")
    raise SystemExit(0)
