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
def save_to_scores(scores):
    # tallennetaan tiedot json-muodossa tiedostoon
    with open('scores.txt', 'w') as f:
        json.dump(scores, f)
    # with open("database.txt", 'a') as f:
    #     f.write(f"\n{id},{name},{points}")

# def fetch_customers():
#     scores = []
#     with open('scores.txt', 'r') as f:
#         scores = json.load(f)
#     for data in scores:
#         customer = {'id': int(data['id']), 'name': data['name'], 'points': data['points']}
#         scores.append(customer)
#     return scores

def main():
    print(read_scores())

if __name__ == "__main__":
    main()