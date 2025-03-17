from flask import Flask, send_from_directory, request, abort, Response
from flask_cors import CORS
import os
import sys
from werkzeug.utils import secure_filename
from colorama import Fore, Style

from create_dir import SAVE_DIR, create_project_dir, create_project_issue_dir
from save import save_file

app = Flask(__name__)
CORS(app)


@app.route("/dump", methods=["POST"])
def insert_file():
    if "file" not in request.files:
        # logs
        print(
            Fore.RED + "Received no file in request. Stopping" + Style.RESET_ALL,
            file=sys.stdout,
        )
        return Response(response="No file in request", status=415)
        # return 415  # 415 Unsupported Media Type

    file = request.files["file"]
    filename = secure_filename(file.filename)
    project_id = request.form.get("project_id")
    issue_id = request.form.get("issue_id")

    # logs
    print(
        Fore.GREEN
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
        # logs
        print(
            Fore.RED + "The received file has no name. Stopping" + Style.RESET_ALL,
            file=sys.stdout,
        )
        return Response(response="File has no name", status=409)
        # return 409  # 409 Conflict
    if file:
        # logs inside package
        # create dirs
        create_project_dir(project_id)
        create_project_issue_dir(project_id, issue_id)
        # save file
        save_file(project_id, issue_id, filename, file)

        return Response(response="File uploaded", status=201)
        # return 201  # 201 Created

    return Response(response="Bad Request", status=400)
    # return 400  # Bad Request


@app.route("/attachments/<project_id>/<issue_id>/<file_name>", methods=["GET"])
def get_file(project_id, issue_id, file_name):
    # Construct the directory path
    directory = os.path.join(SAVE_DIR, project_id, issue_id)

    # Ensure the directory exists
    if not os.path.exists(directory):
        abort(404, description="Directory not found")

    # Ensure the requested file exists
    file_path = os.path.join(directory, file_name)
    if not os.path.isfile(file_path):
        abort(404, description="File not found")

    # Send the file from the directory
    return send_from_directory(directory, file_name)


@app.route("/files/<project_id>/<issue_id>/<file_name>", methods=["DELETE"])
def del_file(project_id, issue_id, file_name):
    try:
        os.remove(os.path.join(SAVE_DIR, project_id, issue_id, file_name))
    except Exception as e:
        return Response(e, status=400)

    return Response("success", 200)
