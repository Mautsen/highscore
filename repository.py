# import os
# from flask import jsonify, json
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage, firestore
# import tempfile

# # luetaan firebase ympäristömuuttuja
# # tee render.comiin uusi muuttuja nimeltä firebase jonka
# # sisältö on json tiedosto jonka saat firebaselta
# json_str = os.environ.get('firebase')
# """
# A JSON string containing Firebase credentials.
# """

# # tallennetaan ympäristömuuttujan sisältö väliaikaiseen tiedostoon
# with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
#     f.write(json_str)
#     temp_path = f.name
# """
# A temporary file containing the Firebase credentials JSON string.
# """

# # luetaan tiedostosta json filu
# cred = credentials.Certificate(temp_path)
# """
# Firebase credentials object.
# """

# # tee render.comiin ympäristömuuttuja bucket, jonka sisältö
# # esim: mydatabase-38cf0.appspot.com
# firebase_admin.initialize_app(cred, {
#     'storageBucket': os.environ.get('bucket')
# })
# bucket = storage.bucket()
# """
# Firebase Storage bucket object.
# """

# FILE = 'scores.txt'
# """
# Name of the file that stores scores data.
# """

# # JONNA read_scores
# def read_scores():
#     """
#     Read scores data from Firebase Storage.

#     Returns:
#     A list of scores in JSON format.
#     """
#     try:
#         blob = bucket.blob(FILE)
#         scores_json = blob.download_as_string().decode('utf-8')
#         return json.loads(scores_json)
#     except:
#         return []

# # JONNA save_scores to the scores.txt
# def save_to_scores(scores):
#     """
#     Save scores data to Firebase Storage.

#     Args:
#     - scores: A list of scores in JSON format.
#     """
#     with open('scores.txt', 'w') as f:
#         blob = bucket.blob(FILE)
#         blob.upload_from_string(json.dumps(scores), content_type='text/plain')


# def main():
#     """
#     Print scores data.
#     """
#     print(read_scores())

# if __name__ == "__main__":
#     main()

# KÄYTÄ NÄITÄ KOODEJA KUN TEET PDOCSIT: (KOMMENTOI KAIKKI YLLÄOLEVA POIS SIKSI AIKAA) TAI JOS HALUAT AJAA APP.PY !!!!!!
import json

FILE = 'scores.txt'
"""
Name of the file that stores scores data.
"""

# JONNA read_scores
def read_scores():
    """
    Read scores data from the scores.txt file.

    Returns:
    A list of scores in JSON format.
    """
    try:
        with open(FILE, 'r') as f:
            scores_json = f.read()
            return json.loads(scores_json)
    except:
        return []

# JONNA save_scores to the scores.txt
def save_to_scores(scores):
    """
    Save scores data to the scores.txt file.

    Args:
    - scores: A list of scores in JSON format.
    """
    with open(FILE, 'w') as f:
        f.write(json.dumps(scores))


def main():
    """
    Print scores data.
    """
    print(read_scores())

if __name__ == "__main__":
    main()