import json
import dropbox

# create a Dropbox API client
dbx = dropbox.Dropbox("avain")

def read_scores():
    try:
        # download scores file from Dropbox
        _, file = dbx.files_download('/scores.txt')
        file_contents = file.content.decode('utf-8')
        if file_contents.strip() == '':
            # tiedosto on tyhjä, palautetaan tyhjä lista
            return []
        else:
            scores = json.loads(file_contents)
            if isinstance(scores, dict):
                # jos json-tiedosto sisältää yhden nimen, muutetaan se listaksi
                scores = [scores]
    except dropbox.exceptions.HttpError as e:
        print(f"Error downloading scores file: {e}")
        scores = []
    return scores

# JONNA read_scores
# def read_scores():
#     try:
#         with open('scores.txt', 'r') as f:
#             file_contents = f.read()
#             if file_contents.strip() == '':
#                 # tiedosto on tyhjä, palautetaan tyhjä lista
#                 return []
#             else:
#                 scores = json.loads(file_contents)
#                 if isinstance(scores, dict):
#                     # jos json-tiedosto sisältää yhden nimen, muutetaan se listaksi
#                     scores = [scores]
#     except FileNotFoundError:
#         scores = []
#     return scores


#Save scores to the dropbox:
def save_to_scores(scores):
    # tallennetaan tiedot json-muodossa tiedostoon
    scores_json = json.dumps(scores)
    try:
        # upload scores file to Dropbox
        dbx.files_upload(scores_json.encode('utf-8'), '/scores.txt', mode=dropbox.files.WriteMode('overwrite'))
    except dropbox.exceptions.HttpError as e:
        print(f"Error uploading scores file: {e}")
        
# JONNA save_scores to the scores.txt
# def save_to_scores(scores):
#     # tallennetaan tiedot json-muodossa tiedostoon
#     with open('scores.txt', 'w') as f:
#         json.dump(scores, f)


def main():
    print(read_scores())

if __name__ == "__main__":
    main()