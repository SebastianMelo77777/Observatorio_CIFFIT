import yaml
from pathlib import Path

def load_config():
    config_path = Path("config/config.yaml")
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)