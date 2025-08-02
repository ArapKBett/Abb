import json
import logging
import os

def load_config():
    with open("config/config.json", "r") as f:
        return json.load(f)

def load_accounts():
    with open("config/accounts.json", "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open("config/accounts.json", "w") as f:
        json.dump(accounts, f, indent=4)

def setup_logging(log_file, log_level):
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
