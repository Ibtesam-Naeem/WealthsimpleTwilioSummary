import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("wealthsimple_summary.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )