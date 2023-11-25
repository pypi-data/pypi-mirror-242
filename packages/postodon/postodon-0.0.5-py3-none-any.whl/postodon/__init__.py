#!/usr/bin/env python3

import json
import platformdirs
import sys

from . import append_post
from . import select_post
from . import submit_post

CONFIG_FILENAME = "config.json"
CONFIG_DIR = platformdirs.user_config_path(
    appname="postodon", appauthor=None, version=None, roaming=False, ensure_exists=True
)
CONFIG_PATH = CONFIG_DIR / CONFIG_FILENAME

blue = "\033[94m"
reset = "\033[0m"

# Helpers


def read_config():
    try:
        with open(CONFIG_PATH, "r") as file_pointer:
            config = json.load(file_pointer)
    except FileNotFoundError:
        print(f"ERROR: config file not found at {blue}{CONFIG_PATH}{reset}")
        print("Have you run `postodon init`?")
        sys.exit()
    return config


def write_config(config):
    if CONFIG_PATH.exists():
        print(
            f"Refusing to overwrite existing config file at {blue}{CONFIG_PATH}{reset}"
        )
    else:
        print(f"Creating initial config file at {blue}{CONFIG_PATH}{reset}")
        with open(CONFIG_PATH, "w") as file_pointer:
            json.dump(config, file_pointer, indent=True)
    return config


# Actions


def post():
    config = read_config()
    post = select_post.main(config["post_list"])
    print(post)
    if "-n" not in sys.argv:
        submit_post.main(config["instance_name"], post)


def add(post_text):
    config = read_config()
    append_post.main(config["post_list"], post_text)


def init():
    config = {
        "instance_name": "",
        "post_list": "",
    }
    write_config(config)


# Main - entry point


def main(action="post"):
    try:
        action = sys.argv[1]
    except IndexError:
        action = "post"
    try:
        post_text = sys.argv[2]
    except IndexError:
        if action == "add":
            print("Provide post text")
            sys.exit()
    if action == "post":
        post()
    elif action == "add":
        add(post_text)
    elif action == "init":
        init()
    else:
        print("Unknown action:", action)
        sys.exit()
