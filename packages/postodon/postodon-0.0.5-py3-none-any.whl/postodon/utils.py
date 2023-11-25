import json
import shutil
import sys


def read_db(post_list):
    try:
        with open(post_list, "r") as file_pointer:
            data = json.load(file_pointer)
    except FileNotFoundError:
        print(f"ERROR: cannot find post list at {post_list}")
        print("Check your config file points to a valid post list")
        sys.exit()
    return data


def write_db(post_list, data):
    shutil.copy(post_list, post_list + ".bup")
    with open(post_list, "w") as file_pointer:
        json.dump(data, file_pointer, sort_keys=True, indent=4)
