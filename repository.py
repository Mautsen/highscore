import json

def read_scores():
    data = open("database.txt", "r")
    return data.read()

def save_to_scores(name, id):
    f = open("database.txt", "a")
    f.write(f"\n{id},{name}")
    f.close()

#used with delete
def overwrite_scores(db_list):
    f = open("database.txt", "w")
    for i in range(len(db_list)):
        id = db_list[i]['id']
        name = db_list[i]['name']
        if len(db_list) - 1 > i:
            f.writelines(str(id) + ',' + name + '\n')
        else:
            #last line of database.txt must not be empty,
            #pr it will break the code
            f.writelines(str(id) + ',' + name)
    f.close()

def fetch_scores():
    customers = []
    database_content = read_scores()
    db_split = database_content.split('\n')
    for data in db_split:
        attributes = data.split(',')
        customer = {'id': int(attributes[0]), 'name': attributes[1]}
        customers.append(customer)
    return customers

def main():
    print(read_scores())

if __name__ == "__main__":
    main()

# # JONNA read_scores
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

# # JONNA save_scores to the scores.txt
# def save_scores(scores):
#     # tallennetaan tiedot json-muodossa tiedostoon
#     with open('scores.txt', 'w') as f:
#         json.dump(scores, f)
#     # with open("database.txt", 'a') as f:
#     #     f.write(f"\n{id},{name},{points}")

# def fetch_customers():
#     scores = []
#     with open('scores.txt', 'r') as f:
#         scores = json.load(f)
#     for data in scores:
#         customer = {'id': int(data['id']), 'name': data['name'], 'points': data['points']}
#         scores.append(customer)
#     return scores
