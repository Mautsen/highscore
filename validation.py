import re
from typing import List

def validate_username(name):
    invalid_usernames: List[str] = ['admin', 'root', "anal", "anus", "arse", "ass", "ballsack", "balls", "bastard", "bitch", "biatch", "bloody",
                                    "blowjob", "blow", "bollock", "bollok", "boner", "boob", "bugger", "bum", "butt", "buttplug", "clitoris",
                                    "cock", "coon", "crap", "cunt", "damn", "dick", "dildo", "dyke", "fag", "feck", "fellate", "fellatio",
                                    "felching", "fuck", "f u c k", "fudgepacker", "fudge packer", "flange", "Goddamn", "God damn", "hell",
                                    "homo", "jerk", "jizz", "knobend", "knob end", "labia", "lmao", "lmfao", "muff", "nigger", "nigga", "omg",
                                    "penis", "piss", "poop", "prick", "pube","pussy", "queer", "scrotum", "sex", "shit", "s hit", "sh1t", "slut",
                                    "smegma", "spunk", "tit", "tosser", "turd", "twat", "vagina", "wank", "whore", "wtf", "huora", "perse", "paska",
                                    "pillu", "mulkku", "vittu", "kyrpä", "neekeri", "kusi", "perkele", "saatana", "helvetti", "lutka", "kusipää",
                                    "wittu", "ripuli", "kakka", "seksi", "pallihiki", "palli", "pylly", "pimppi", "nekru", "sperma"]
    pattern = r'^(?!.*(' + '|'.join(invalid_usernames) + '))[a-zA-ZäÄöÖåÅ]{1,10}$'
    if re.match(pattern, name):
        return True
    else:
        return False