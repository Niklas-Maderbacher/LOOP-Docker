from flask import Flask, send_from_directory, request, abort
import os
from werkzeug.utils import secure_filename

from create_dir import SAVE_DIR, create_project_dir, create_project_issue_dir
from save import save_file

app = Flask(__name__)


@app.route("/dump", methods=["POST"])
def insert_file():
    if "file" not in request.files:
        return "No file part \n", 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    project_id = request.form.get("project_id")
    issue_id = request.form.get("issue_id")

    print(project_id)
    print(issue_id)

    if file.filename == "":
        return "No selected file \n", 400
    if file:
        # create dirs
        create_project_dir(project_id)
        create_project_issue_dir(project_id, issue_id)
        # save file
        save_file(project_id, issue_id, filename, file)
        return f"file '{file.filename}' uploaded successfully \n", 200
    return "Failed upload\n", 400


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
    return_msg = ""
    status_code = 0
    try:
        os.remove(os.path.join(SAVE_DIR, project_id, issue_id, file_name))
        return_msg = "Success \n"
        status_code = 204
    except Exception as e:
        return_msg = e + "\n"
        status_code = 400

    return return_msg, status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FILE_SERVER_PORT")), debug=True)
