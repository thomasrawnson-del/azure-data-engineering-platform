from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yaml"


def load_config() -> dict:
    """Load project configuration from YAML."""

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)