# from flask import Blueprint, request, jsonify, send_file
# from src.controllers.driveController import upload_to_drive, download_from_drive
# import os
# import tempfile
# drive_bp = Blueprint('drive_bp', __name__, url_prefix='/drive')

# import json
# from flask_cors import cross_origin


# @drive_bp.route('/upload', methods=['POST'])
# @cross_origin(origins="http://localhost:4200") 
# def upload_drive():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400

#     file = request.files['file']
#     file_name = file.filename
#     temp_dir = tempfile.gettempdir()
#     file_path = os.path.join(temp_dir, file_name)
#     #file_path = f'/tmp/{file_name}'
#     file.save(file_path)

#     file_id = upload_to_drive(file_path, file_name)
#     google_drive_url = f"http://drive.google.com/uc?id={file_id}"

#     data = {}
#     if os.path.exists('file_ids.json'):
#         with open('file_ids.json', 'r') as f:
#             data = json.load(f)

#     data[file_name] = file_id
#     with open('file_ids.json', 'w') as f:
#         json.dump(data, f)

#     os.remove(file_path)

#     return jsonify({'google_drive_url': google_drive_url}), 200


# @drive_bp.route('/download/<file_id>', methods=['GET'])
# @cross_origin(origins="http://localhost:4200") 













# def download_drive(file_id):
#     file_data = download_from_drive(file_id)
#     return send_file(file_data, mimetype='image/jpeg', as_attachment=True, download_name=f'{file_id}.jpg')


from flask import Blueprint, request, jsonify, send_file
from src.controllers.driveController import upload_to_drive, download_from_drive
import os
import tempfile

drive_bp = Blueprint('drive_bp', __name__, url_prefix='/drive')

import json

@drive_bp.route('/upload', methods=['POST'])
def upload_drive():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}),

    file = request.files['file']
    file_name = file.filename
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file_name)
    #file_path = f'/tmp/{file_name}'
    file.save(file_path)

    file_id = upload_to_drive(file_path, file_name)
    google_drive_url = f"https://drive.google.com/uc?id={file_id}"

    # Guardar el file_id en un archivo JSON
    data = {}
    if os.path.exists('file_ids.json'):
        with open('file_ids.json', 'r') as f:
            data = json.load(f)

    data[file_name] = file_id
    with open('file_ids.json', 'w') as f:
        json.dump(data, f)

    os.remove(file_path)

    return jsonify({
        'google_drive_url': google_drive_url,
        'id_document': file_id
    }), 200


@drive_bp.route('/download/<file_id>', methods=['GET'])
def download_drive(file_id):
    file_data = download_from_drive(file_id)
    return send_file(file_data, mimetype='image/jpeg', as_attachment=True, download_name=f'{file_id}.jpg')