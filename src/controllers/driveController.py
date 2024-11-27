# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# from io import BytesIO
# import os
# from config import drive_service
# import time
# import ssl
# import socket

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2 
# ssl_context.check_hostname = True
# ssl_context.set_ciphers('ALL')  
# socket.setdefaulttimeout(20000)

# def upload_to_drive(file_path, file_name):
#     try:
#         file_metadata = {'name': file_name}
#         media = MediaFileUpload(file_path, resumable=True)
#         uploaded_file = drive_service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id'
#         ).execute()
#         print(f"Archivo '{file_name}' subido exitosamente con ID: {uploaded_file.get('id')}")
#         return uploaded_file.get('id')
#     except Exception as e:
#         print(f"Error al subir el archivo: {e}")
#         return None

# def download_from_drive(file_id):
#     request = drive_service.files().get_media(fileId=file_id)
#     file_data = BytesIO()
#     downloader = MediaIoBaseDownload(file_data, request)
#     done = False
#     while not done:
#         status, done = downloader.next_chunk()
#     file_data.seek(0)
#     return file_data


from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import BytesIO
import os
from config import drive_service

def upload_to_drive(file_path, file_name):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return uploaded_file.get('id')

def download_from_drive(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    file_data = BytesIO()
    downloader = MediaIoBaseDownload(file_data, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_data.seek(0)
    return file_data