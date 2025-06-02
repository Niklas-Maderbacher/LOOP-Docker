import os
import sys

from colorama import Fore, Style
from werkzeug.utils import secure_filename

from logging_helper import get_cur_time


SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "attachments")


def create_project_dir(project_id: str):
    project_id = secure_filename(project_id)
    if not os.path.exists(os.path.join(SAVE_DIR, project_id)):
        os.mkdir(os.path.join(SAVE_DIR, project_id))
        # logs success
        print(
            Fore.GREEN
            + get_cur_time()
            + "Created new project directory with name "
            + project_id
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        return

    # logs skipping
    print(
        Fore.CYAN
        + get_cur_time()
        + "Skipping - Project directory with name "
        + project_id
        + " already exists"
        + Style.RESET_ALL,
        file=sys.stdout,
    )
    return


def create_project_issue_dir(project_id: str, issue_id: str):
    project_id = secure_filename(project_id)
    issue_id = secure_filename(issue_id)
    if os.path.exists(os.path.join(SAVE_DIR, project_id)):
        if not os.path.exists(os.path.join(SAVE_DIR, project_id, issue_id)):
            os.mkdir(os.path.join(SAVE_DIR, project_id, issue_id))
            # logs success
            print(
                Fore.GREEN
                + get_cur_time()
                + "Created new issue directory with name "
                + issue_id
                + " in project directory "
                + project_id
                + Style.RESET_ALL,
                file=sys.stdout,
            )
            return

    # logs skipping
    print(
        Fore.CYAN
        + get_cur_time()
        + "Skipping - Issue directory with name "
        + issue_id
        + " in project directory "
        + project_id
        + " already exists"
        + Style.RESET_ALL,
        file=sys.stdout,
    )
