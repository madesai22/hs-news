from unidecode import unidecode
import string
import re
from datetime import datetime
import file_handling as fh

def match_gun_violence(text):
    march_match = re.search(r"\bMarch(ing|es|ed)? for Our Lives\b|neveragain|\bStudents Demand Action\b|\bNational School Walkout\b|\bsecond amendment\b|\bNRA\b|Never Again MSD|2nd amendment|stand for the second|moms demand action|\beverytown\b|sandy hook promise|bear(ing)* arms|(conceal(ed)*|assault|automatic)+ (rifle|weapon|carry)+|national walk(-|\s)?out",text, re.IGNORECASE)
    alice_match = re.search(r"\bALICE\b", text)
    gun_match = re.search(r"\b(gun(s)*)\b|\b(firearm+(s)*)\b|\b(gunfir)|(^(?=.*teach)(?=.*arm).*)", text, re.IGNORECASE)
    mgk = re.search(r"machine gun kelly|\btop gun",text, re.IGNORECASE)
    sports_pattern = r"ball\b|lacrosse|score|film|movie|hoop|win|soccer|court|hockey|polo|champ|game|varsity|lax|trophy|sweep|flu|vaccin|photo|star|playoff|competition|finals|drink|alcohol"
    sports_match = re.search(sports_pattern, text, re.IGNORECASE)
    shooting_match = re.search(r"\b(?!(?:shot[\s-]?put(?:t|s)?(?:ter)?\b))(?:shoot|shot)\w*\b", text, re.IGNORECASE)
    long_shot_match = re.search(r"(long\s+shot|big\s+shot|best\s+shot\w*)|(call+(ing|ed|s)* the shot)", text, re.IGNORECASE)
    shooter_likely = re.search(r"\b(?:active|mass|school|campus)\s+(?:shoot|shot)\w*", text, re.IGNORECASE)
    match = (gun_match and not mgk) or alice_match or shooter_likely or march_match or (shooting_match and not sports_match and not long_shot_match)
    return match

def match_gun_violence_simple(text):
    shooter_likely = re.search(r"\b(?:active|mass|school|campus)\s+(?:shoot|shot)\w*|(\bgun violence)", text, re.IGNORECASE)
    return  shooter_likely

def df_slice(df, start, end, column):
    # Extract the rows with year values between 1999 and 2019
    data = df[(df[column] >= start) & (df[column] <= end)].sort_values(by=column)
    return data

def year_to_election_year(year):
  election_years = range(1980,2024,4)
  if year in election_years:
    ey = year
  else:
    for i in range(1,4):
      if year-i in election_years:
        ey = year-i
  return ey 


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

