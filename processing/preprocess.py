from unidecode import unidecode
import string
import re
from datetime import datetime
from dateutil.parser import parse
import file_handling as fh

def get_stopwords(filename="./snowball.txt"):
   return fh.read_text_to_list(filename)

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
    # e.g. extract the rows with year values between 1999 and 2019
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

def get_invalid_year_value():
   return 3000


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
            return get_invalid_year_value() 

def get_date(date_string):
   try:
      return parse(date_string)
   except:
      date_pattern = r"(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}"
      match = re.search(date_pattern, date_string)
      if match:
         return parse(match[0])
      else:
         return datetime(3000, 1, 1, 0, 0)

def remove_whitespaces(text,paragraph=False):
    if paragraph:
       return re.sub(' +|\t+', ' ', text)
    else:
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

def pre_process_sentence(text, stopwords=None):
    pattern = pattern = "\.(\n|\s)+"
    text = re.split(pattern, text)
    new_text = []
    for i in range(len(text)):
       sentence = text[i]
       if sentence is not None:
          sentence = strip_punctuation(sentence)
          sentence = remove_whitespaces(sentence)
          sentence = strip_punctuation(sentence).lower().strip()
          new_text.append(sentence)
    return new_text

def pre_process_paragraph(text, stopwords=None):
    text = strip_punctuation(text).lower().strip()
    text = remove_whitespaces(text,paragraph=True)

    pattern = "\n(\s)?\n"
    text = re.split(pattern, text)
    text = list(filter(lambda item: item is not None, text))
    return text
   


def pre_process(text, stopwords=None): #remove punctuation, remove stop words, lower case, and tokenize   
    text = remove_whitespaces(text)
    text = strip_punctuation(text).lower().strip()
    text = tokenize(text,stopwords)
    return text

def MEDIA_FRAMES_CORPUS_TRUNCATION():
   return 225

def clean_student_news_article(headline, content):
    headline = remove_whitespaces(headline)
    headline = strip_punctuation(headline).lower().strip()
    sentences = pre_process_sentence(content)
    n_sentences = len(sentences)
    sentence_count = 0 
    text = tokenize(headline)

    while len(text) < MEDIA_FRAMES_CORPUS_TRUNCATION() and sentence_count < n_sentences:
        next_sentence = sentences[sentence_count]
        sentence_count += 1 
        text.extend(next_sentence.split())
    text = " ".join(text)

    return text

