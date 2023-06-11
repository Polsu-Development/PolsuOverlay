import os
import sys


def resource_path(relative_path: str) -> str:
    """
    This function is used for when the overlay is an executable file
    The path for an asset isn't the same when the program is an executable

    :param relative_path: A string representing a path
    :return: A string representing the real path
    """
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
