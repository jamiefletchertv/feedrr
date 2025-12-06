"""Configuration management for feedrr."""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Configuration files
CONFIG_DIR = PROJECT_ROOT / "src" / "config"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
FEEDS_FILE = CONFIG_DIR / "feeds.yaml"

# Templates and static assets
TEMPLATES_DIR = PROJECT_ROOT / "src" / "templates"
STATIC_DIR = PROJECT_ROOT / "src" / "static"

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Output directory
SITE_DIR = PROJECT_ROOT / "site"


def get_config_path() -> Path:
    """Get the path to config.yaml."""
    return CONFIG_FILE


def get_feeds_path() -> Path:
    """Get the path to feeds.yaml."""
    return FEEDS_FILE


def get_templates_dir() -> Path:
    """Get the templates directory."""
    return TEMPLATES_DIR


def get_static_dir() -> Path:
    """Get the static assets directory."""
    return STATIC_DIR


def get_data_dir() -> Path:
    """Get the data directory."""
    return DATA_DIR


def get_logs_dir() -> Path:
    """Get the logs directory."""
    return LOGS_DIR


def get_site_dir() -> Path:
    """Get the output/site directory."""
    return SITE_DIR
