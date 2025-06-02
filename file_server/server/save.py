import os
import sys

from colorama import Fore, Style

from create_dir import SAVE_DIR
from logging_helper import get_cur_time


def save_file(project_id: int, issue_id: int, filename: str, file):
    if os.path.exists(os.path.join(SAVE_DIR, project_id)):
        if os.path.exists(os.path.join(SAVE_DIR, project_id, issue_id)):
            file.save(os.path.join(SAVE_DIR, project_id, issue_id, filename))
            # logs success
            print(
                Fore.GREEN
                + get_cur_time()
                + "Saved file "
                + filename
                + " in project directory "
                + project_id
                + " in issue directory "
                + issue_id
                + Style.RESET_ALL,
                file=sys.stdout,
            )
            return

    # logs error
    print(
        Fore.RED
        + get_cur_time()
        + "Could not save file "
        + filename
        + " in project directory "
        + project_id
        + " in issue directory "
        + issue_id
        + Style.RESET_ALL,
        file=sys.stdout,
    )
    return
