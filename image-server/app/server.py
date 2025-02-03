from flask import Flask, send_from_directory, request
import os
from datetime import datetime, timezone

app = Flask(__name__)

image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_filename(filename):
    new_filename = str(datetime.now(timezone.utc)) + filename
    new_filename = new_filename.replace(" ", "-")
    return new_filename


@app.route("/image", methods=["POST"])
def insert_image():
    if "image" not in request.files:
        return "No file part \n", 400
    file = request.files["image"]
    if file.filename == "":
        return "No selected file \n", 400
    if file and allowed_file(file.filename):
        filename = create_filename(file.filename)
        file.save(os.path.join(image_dir, filename))
        return f"Image '{filename}' uploaded successfully \n", 200
    return "Invalid file type \n", 400


@app.route("/image/<image_name>", methods=["GET"])
def get_image(image_name):
    return send_from_directory(image_dir, image_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("IMAGE_SERVER_PORT")))
