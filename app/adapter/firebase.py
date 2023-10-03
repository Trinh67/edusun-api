import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

bucket = storage.bucket("worduptest-e5ac4.appspot.com")


# -------------------------------------------------------------------------------

# all_files = bucket.list_blobs(prefix="image/")
# for file in all_files:
#     print(file.name)
# file.download_to_filename(file.name)


# -------------------------------------------------------------------------------
class FirebaseService:
    @classmethod
    def upload_file(cls, file_name, file_data):
        blob = bucket.blob(file_name)
        blob.upload_from_string(file_data)
        return file_name
