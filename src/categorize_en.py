import pandas as pd
import numpy as np
import json
import os
from textblob import TextBlob
import textacy


def categorizeText(input_text: str):
    """
    :Returns: List = [MainLevel, Difficulty] (some sort of language level)
    """

    if (not(isinstance(input_text, str)) or (len(input_text) <= 0)):
        dicti = {"unknown": "NOT OKAY!", "A1": "THIS!", "A2" : "IS!", "B1": "NOT!", "B2": "A!", "C1": "TEXT!", "C2": "NO!"}
        return ["NO!", "NO!", dicti]

    # normalize text with NLP
    input_text = processText(input_text)
    
    # store words of text lowercase in list
    words: list = [item.lower() for item in input_text.split()]

    # count frequency of word in text
    word_frequency: dict = getWordFrequency(words)

    # Dataframe, set der Worte mit Sprachniveau
    # word, level
    set_word_table = getWordLevelDataFrameForText(set(words))

    # Betrachtung der Verteilung
    verteilung = {}
    tmp_count = 0
    
    #TODO : DEVIDE BY ZERO ?!?!?!
    #für jedes Wort aus dem Text, geordnet nach Level, 
    for lvl in ["unknown", "A1", "A2", "B1", "B2", "C1", "C2"]:
        for word in set_word_table.loc[set_word_table['level']== lvl, "word"]:
            tmp_count += word_frequency[word]
        tmp_result = tmp_count/ len(words) * 100
        verteilung[lvl] = round(tmp_result)
        tmp_count = 0
    
    #Einstufung anhand des höchsten Levels, das mehr als n verschiedene Wörter enthält
    # sehr unschön bisher!
    n = 4
    levels, counts = np.unique(set_word_table['level'], return_counts=True)
    
    if (len(levels) > 0):
        tmp_index, = np.where(levels == "unknown") # löschen der Stellen, an denen die Werte für UNKNOWN Worte stehen, da diese kein Sprachniveau sind
        levels = np.delete(levels, tmp_index)
        counts = np.delete(counts, tmp_index)
    max_level = np.max(levels[counts > n])
    
    # TODO : Satzlänge!
    #Einstufung des Schwierigkeitgrades der unbekannten Worte, Grenze: m
    # wenn Worte, die länger als m sind, werden als schwer eingestuft. dann einfach, wovon es mehr gibt
    count_easy = 0
    count_hard = 0
    m = 6 # siehe Wolfram alpha 5.1
    
    for word in set_word_table.loc[set_word_table['level']== "unknown", "word"]:
        if len(word) > m:
            count_hard += 1
        elif len(word) <= m:
            count_easy += 1   
    
    if count_easy <= count_hard:
        difficulty = "hard"
    else:
        difficulty = "easy"

    # return Liste [mainLevel, Schwierigkeitsgrad, Sprachniveaus_Verteilung]
    return [max_level, difficulty, verteilung]


def getWordFrequency(words: list) -> dict:
    """
    :Return: dictionary with word and count
    """
    dici = {}

    for word in words:
        if word in dici:     
            dici[word] += 1
        else:
            dici[word] = 1
            
    return dici


def getWordLevelDataFrameForText(text):
    """
    Eingabe: set(text)
    Ausgabe: DataFrame mit word und level (A1 - C2, unknown) für das gegebene Set des Textes
    """

    # create DataFrame
    word_level_table = pd.DataFrame(columns=['word', 'level'])

    # open CEFR vocabulary file for english
    scriptDir = os.path.dirname(__file__) 
    relPath = "../cefr/cefr_vocab_en.json"
    cefr_file = open(os.path.join(scriptDir, relPath))
    cefr_data = json.load(cefr_file)

    for w in set(text):

        level: str = ""

        # find the CEFR level info for the current word
        for data in cefr_data:

            if data["word"] == w:
                if data["level"]:
                    level  = data["level"]
                else:
                    level = "unknown"

        # add row WORD LEVEL
        word_level_table = word_level_table.append(
            pd.DataFrame(
                [
                    [w, level]
                ], 
                    columns=['word', 'level']
            )
        )
        
    # close cefr json file
    cefr_file.close()

    return word_level_table


def processText(text):

    preprocessedText = textacy.preprocess_text(
        text,
        no_accents=True,
        no_punct=True,
        lowercase=False,
        fix_unicode=True,
        no_emails=True,
        no_phone_numbers=True,
        no_contractions=True
    )

    # lemmatize the entire text
    # first, split the text to a list of words
    words = TextBlob(preprocessedText).words
    # then, lemmatize each word
    lemmatizedText = ""
    for w in words:
        lemmatizedText += "{} ".format(w.lemmatize())

    # normalize the whitespaces for texts which include s.l. 'Title    And I am ...'
    return textacy.preprocess.normalize_whitespace(lemmatizedText)