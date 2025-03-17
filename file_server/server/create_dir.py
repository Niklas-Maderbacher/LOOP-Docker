import os
import sys

from colorama import Fore, Style


SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "attachments")


def create_project_dir(project_id: str):
    if not os.path.exists(os.path.join(SAVE_DIR, project_id)):
        os.mkdir(os.path.join(SAVE_DIR, project_id))
        # logs
        print(
            Fore.GREEN
            + "Created new project directory with id "
            + project_id
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        return

    # logs
    print(
        Fore.YELLOW
        + "Skipping - Project directory with id "
        + project_id
        + " already exists"
        + Style.RESET_ALL,
        file=sys.stdout,
    )
    return


def create_project_issue_dir(project_id: str, issue_id: str):
    if os.path.exists(os.path.join(SAVE_DIR, project_id)):
        if not os.path.exists(os.path.join(SAVE_DIR, project_id, issue_id)):
            os.mkdir(os.path.join(SAVE_DIR, project_id, issue_id))
            # logs
            print(
                Fore.GREEN
                + "Created new issue directory with id "
                + issue_id
                + " in project directory "
                + project_id
                + Style.RESET_ALL,
                file=sys.stdout,
            )
            return

    # logs
    print(
        Fore.YELLOW
        + "Skipping - Issue directory with id "
        + issue_id
        + " in project directory "
        + project_id
        + " already exists"
        + Style.RESET_ALL,
        file=sys.stdout,
    )
