import os
from flask import jsonify, json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage, firestore
import tempfile

# luetaan firebase ympäristömuuttuja
# tee render.comiin uusi muuttuja nimeltä firebase jonka
# sisältö on json tiedosto jonka saat firebaselta
json_str = os.environ.get('firebase')

# tallennetaan ympäristömuuttujan sisältö väliaikaiseen tiedostoon
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write(json_str)
    temp_path = f.name

# luetaan tiedostosta json filu
cred = credentials.Certificate(temp_path)

# tee render.comiin ympäristömuuttuja bucket, jonka sisältö
# esim: mydatabase-38cf0.appspot.com
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('bucket')
})
bucket = storage.bucket()

FILE = 'scores.txt'

# load Dropbox access token from environment variable
# access_token = os.getenv("avain")
# if not access_token:
#     raise ValueError("Please set the 'DBX_ACCESS_TOKEN' environment variable")

# # create a Dropbox API client
# dbx = dropbox.Dropbox(access_token)

# def read_scores():
#     try:
#         # download scores file from Dropbox
#         _, file = dbx.files_download('/scores.json')
#         file_contents = file.content.decode('utf-8')
#         if file_contents.strip() == '':
#             # file is empty, return empty list
#             return []
#         else:
#             scores = json.loads(file_contents)
#             if isinstance(scores, dict):
#                 # if the JSON file contains a single score, convert it to a list
#                 scores = [scores]
#     except dropbox.exceptions.HttpError as e:
#         print(f"Error downloading scores file: {e}")
#         scores = []
#     return scores

#def save_to_scores(scores):
##     upload scores file to Dropbox
    #scores_json = json.dumps(scores)
    #try:
        #dbx.files_upload(scores_json.encode('utf-8'), '/scores.json', mode=dropbox.files.WriteMode('overwrite'))
    #except dropbox.exceptions.HttpError as e:
        #print(f"Error uploading scores file: {e}")

# def main():
#     print(read_scores())

# if __name__ == "__main__":
#     main()

# JONNA read_scores
def read_scores():
    # try:
    #     with open('scores.txt', 'r') as f:
    #         file_contents = f.read()
    #         if file_contents.strip() == '':
    #             # tiedosto on tyhjä, palautetaan tyhjä lista
    #             return []
    #         else:
    #             scores = json.loads(file_contents)
    #             if isinstance(scores, dict):
    #                 # jos json-tiedosto sisältää yhden nimen, muutetaan se listaksi
    #                 scores = [scores]
    # except FileNotFoundError:
    #     scores = []
    # return scores

    try:
        blob = bucket.blob(FILE)
        scores_json = blob.download_as_string().decode('utf-8')
        return json.loads(scores_json)
    except:
        return []

# JONNA save_scores to the scores.txt
def save_to_scores(scores):
    scores=read_scores()
    with open('scores.txt', 'w') as f:
        blob = bucket.blob(FILE)
        blob.upload_from_string(json.dumps(scores), content_type='text/plain')

def main():
    print(read_scores())

if __name__ == "__main__":
    main()