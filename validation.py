import re
from typing import List
from repository import *

def validate_username(name):
    """
    Validates a username against a set of predefined rules.
    
    Args:
        name: A string containing the username to be validated.
    
    Returns:
        A boolean indicating whether the username is valid or not.
    """
    invalid_usernames: List[str] = ['Admin', 'Root', "Anal", "Anus", "Arse", "Ass", "Aallsack", "Aalls", "Bastard", "Bitch", "Biatch", "Bloody",
                                    "Blowjob", "Blow", "Bollock", "Bollok", "Boner", "Boob", "Bugger", "Bum", "Butt", "Buttplug", "Clitoris",
                                    "Cock", "Coon", "Crap", "Cunt", "Damn", "Dick", "Dildo", "Dyke", "Fag", "Feck", "Fellate", "Fellatio",
                                    "Felching", "Fuck", "Fudgepacker", "Flange", "Goddamn", "God damn", "Hell",
                                    "Homo", "Jerk", "Jizz", "Knobend", "Labia", "Lmao", "Lmfao", "Muff", "Nigger", "Nigga", "Omg",
                                    "Penis", "Piss", "Poop", "Prick", "Pube","Pussy", "Queer", "Scrotum", "Sex", "Shit", "Slut",
                                    "smegma", "Spunk", "Tit", "Tosser", "Turd", "Twat", "Vagina", "Wank", "Whore", "Wtf", "Huora", "Perse", "Paska",
                                    "Pillu", "Mulkku", "Vittu", "Kyrpä", "Neekeri", "Kusi", "Perkele", "Saatana", "Helvetti", "Lutka", "Kusipää",
                                    "Wittu", "Ripuli", "Kakka", "Seksi", "Pallihiki", "Palli", "Pylly", "Pimppi", "Nekru", "Sperma", "Kyrpa",
                                    "Kusipaa", "Tissi", "Tissit", "Mälli", "Idiootti", "Transu", "Trans", "Lesbo", "Hintti", "Vammanen",
                                    "Wammanen", "Kehari", "Boobs", ]
    pattern = r'^(?!.*(' + '|'.join(invalid_usernames) + '))[A-ZÄÖÅ][a-zA-ZäÄöÖåÅ]{2,9}$'
    if re.match(pattern, name):
        return True
    else:
        return False
    
def username_in_use(name):
    """
    Checks whether a given username is already in use.
    
    Args:
        name: A string containing the username to be checked.
    
    Returns:
        A boolean indicating whether the username is in use or not.
    """
    scores = read_scores()
    for score in scores:
        if score['name'] == name:
            return False
    return True
