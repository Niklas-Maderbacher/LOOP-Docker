from flask import Flask, send_from_directory, request, abort, Response
from flask_cors import CORS
import os
import sys
import json
from werkzeug.utils import secure_filename
from colorama import Fore, Style

from create_dir import SAVE_DIR, create_project_dir, create_project_issue_dir
from save import save_file
from logging_helper import get_cur_time

app = Flask(__name__)
CORS(app)


@app.route("/dump", methods=["POST"])
def insert_file():
    if "file" not in request.files:
        # logs error
        print(
            Fore.RED
            + get_cur_time()
            + "Received no file in request. Stopping"
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        return Response(response="No file in request", status=415)
        # return 415  # 415 Unsupported Media Type

    file = request.files["file"]
    project_id = request.form.get("project_id")
    issue_id = request.form.get("issue_id")
    filename = secure_filename(file.filename)

    # check directory name validity
    if project_id != secure_filename(project_id) or issue_id != secure_filename(issue_id):
        # logs error
        print(
            Fore.RED
            + get_cur_time()
            + "Received invalid characters for saving location"
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        return Response(response="Given save location contains invalid characters", status=422)
        # return 422  # 422 Unprocessable Content

    # logs success
    print(
        Fore.GREEN
        + get_cur_time()
        + "Received file "
        + filename
        + " with project id "
        + project_id
        + " with issue id "
        + issue_id
        + Style.RESET_ALL,
        file=sys.stdout,
    )

    if file.filename == "":
        # logs error
        print(
            Fore.RED
            + get_cur_time()
            + "The received file has no name. Stopping"
            + Style.RESET_ALL,
            file=sys.stdout,
        )

        return Response(response="File has no name", status=409)
        # return 409  # 409 Conflict
    if file:
        # logs exist inside package
        # create dirs
        create_project_dir(project_id)
        create_project_issue_dir(project_id, issue_id)
        # save file
        save_file(project_id, issue_id, filename, file)

        return Response(
            response=json.dumps(
                {
                    "Response": "File uploaded successfully",
                    "filename": filename,
                    "project_id": project_id,
                    "issue_id": issue_id,
                }
            ),
            status=201,
            mimetype="application/json",
        )
        # return 201  # 201 Created

    return Response(response="Bad Request", status=400)
    # return 400  # Bad Request


@app.route("/attachments/<project_id>/<issue_id>/<file_name>", methods=["GET"])
def get_file(project_id, issue_id, file_name):
    # Construct the directory path
    directory = os.path.join(SAVE_DIR, project_id, issue_id)

    # Ensure the directory exists
    if not os.path.exists(directory):
        # logs error
        print(
            Fore.RED
            + get_cur_time()
            + "The directory "
            + directory
            + " does not exist"
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        abort(404, description="Directory not found")

    # Ensure the requested file exists
    file_path = os.path.join(directory, file_name)
    if not os.path.isfile(file_path):
        # logs error
        print(
            Fore.RED
            + get_cur_time()
            + "The file "
            + file_name
            + " does not exist"
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        abort(404, description="File not found")

    # logs success
    print(
        Fore.GREEN
        + get_cur_time()
        + "The file "
        + file_name
        + " exists and can be displayed"
        + Style.RESET_ALL,
        file=sys.stdout,
    )
    # Send the file from the directory
    return send_from_directory(directory, file_name)


@app.route("/attachments/<project_id>/<issue_id>/<file_name>", methods=["DELETE"])
def del_file(project_id, issue_id, file_name):
    try:
        # logs attempt
        print(
            Fore.YELLOW
            + get_cur_time()
            + "Trying to delete file "
            + file_name
            + " in project directory "
            + project_id
            + " in issue directory "
            + issue_id
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        os.remove(os.path.join(SAVE_DIR, project_id, issue_id, file_name))
    except Exception as e:
        # logs error
        print(
            Fore.RED
            + get_cur_time()
            + "Could not delete file "
            + file_name
            + Style.RESET_ALL,
            file=sys.stdout,
        )
        print(e)
        return Response("An exception occured", status=400)

    # logs success
    print(
        Fore.GREEN
        + get_cur_time()
        + "Successfully deleted file "
        + file_name
        + Style.RESET_ALL,
        file=sys.stdout,
    )
    return Response("success", 200)
