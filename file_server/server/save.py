import os
from flask import request

from create_dir import SAVE_DIR


def save_file(project_id: int, issue_id: int, filename, file):
    if os.path.exists(os.path.join(SAVE_DIR, project_id)):
        if os.path.exists(os.path.join(SAVE_DIR, project_id, issue_id)):
            file.save(os.path.join(SAVE_DIR, project_id, issue_id, filename))
            return "Success"

    return "operation failed"
