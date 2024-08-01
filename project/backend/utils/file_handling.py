import os

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'

def save_uploaded_file(file: FileStorage) -> str:
    filename = secure_filename(file.filename)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return file_path

def get_file_content(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
    