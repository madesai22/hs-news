from unidecode import unidecode
import string
import re
from datetime import datetime

def match_gun_violence(text):
    march_match = re.findall(r"\bMarch for Our Lives\b|\bStudents Demand Action\b|\bNational School Walkout\b|\bsecond amendment\b|\bNRA\b|\bNever Again MSD\b|\b2nd amendment\b|\bstand for the second\b",text, re.IGNORECASE)
    gun_match = re.findall(r"\b(gun)\b|\b(firearm)\b", text, re.IGNORECASE)
    sports_pattern = r"ball|lacrosse|score|point|film|movie|hoop|win|soccer|court|hockey|polo|champ|game|varsity|lax|trophy|sweep|flu|vaccin|photo|star|playoff|competition|finals"
    sports_match = re.findall(sports_pattern, text, re.IGNORECASE)
    shooting_match = re.findall(r"\b(?!(?:shot[\s-]?put(?:t|s)?(?:ter)?\b))(?:shoot|shot)\w*\b", text, re.IGNORECASE)
    long_shot_match = re.findall(r"(\blong\s+shot\w*)|(call\s+the\s+shot\w*)", text, re.IGNORECASE)
    shooter_likely = re.findall(r"\b(?:active|mass|school)\s+(?:shoot|shot)\w*\b", text, re.IGNORECASE)
    match = gun_match or shooter_likely or march_match or (shooting_match and not sports_match and not long_shot_match)
    return match

def get_year(date_string):
    try:
        year = datetime.strptime(date_string, "%B %d, %Y").year
        return year
    except:
        year_pattern = r"(19[1-9][0-9]|20[0-9][0-9])"
        year_string  = re.findall(year_pattern, date_string)
        if year_string:
            return int(year_string[0])
        else:
            return 3000 

def remove_whitespaces(text):
    return re.sub(' +|\n+|\t+', ' ', text)

def strip_punctuation(text):
    text =  unidecode(text)
    return text.translate(str.maketrans('', '', string.punctuation))

def tokenize(text, stopwords=None):
    if stopwords:
        text = [token for token in text.split() if token not in stopwords]
    else: 
        text = [token for token in text.split()]
    return text

def pre_process(text, stopwords): #remove punctuation, remove stop words, lower case, and tokenize   
    text = remove_whitespaces(text)
    text = strip_punctuation(text).lower().strip()
    text = tokenize(text,stopwords)
    return text
