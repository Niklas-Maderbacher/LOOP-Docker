import os


SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "attachments")


def create_project_dir(project_id: str):
    if not os.path.exists(os.path.join(SAVE_DIR, project_id)):
        os.mkdir(os.path.join(SAVE_DIR, project_id))
        return "Success"

    return "failed operation on creating project dir"


def create_project_issue_dir(project_id: str, issue_id: str):
    if os.path.exists(os.path.join(SAVE_DIR, project_id)):
        if not os.path.exists(os.path.join(SAVE_DIR, project_id, issue_id)):
            os.mkdir(os.path.join(SAVE_DIR, project_id, issue_id))
            return "Success"

    return "failed operation on creating issue dir"
