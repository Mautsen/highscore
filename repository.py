import json

# JONNA read_scores
def read_scores():
    try:
        with open('scores.txt', 'r') as f:
            file_contents = f.read()
            if file_contents.strip() == '':
                # tiedosto on tyhjä, palautetaan tyhjä lista
                return []
            else:
                scores = json.loads(file_contents)
                if isinstance(scores, dict):
                    # jos json-tiedosto sisältää yhden nimen, muutetaan se listaksi
                    scores = [scores]
    except FileNotFoundError:
        scores = []
    return scores

# JONNA save_scores to the scores.txt
def save_scores(scores, id, name, points):
    # tallennetaan tiedot json-muodossa tiedostoon
    with open('scores.txt', 'w') as f:
        json.dumps(scores, f)
    with open("database.txt", 'a') as f:
        f.write(f"\n{id},{name},{points}")