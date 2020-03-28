# -*- coding: utf-8 -*-
"""
Script to extract the terms for the english language
"""
import re
import json

language_level = ["A1", "A2", "B1", "B2", "C1", "C2"]

"""
In the end, it will contain the entire cefr words data.
"""
complete_list: list = []


def extractionFromPdf(level):
    """
    Takes the level from the language_level list and extracts all vocabularies from the cefr files. Then it stores the results in new text files.
    :level: String
    :return: List
    """
    dateiname = "files/Level " + level + " Word List.txt"
    input_text = open(dateiname, "rb")

    text = input_text.read().decode('iso-8859-1')

    #Suche aller Begriffe mit dem Muster: Newline Word Whitespace Slash(ice)
    muster = r"\n\w+\s/"
    matches = re.findall(muster, text)


    # Spezifisches Wort, wieder durch ein Muster filtern
    liste=[]
    muster = r"\w+"

    for i in matches:
        ergebnisliste = re.findall(muster, i)
        liste.append(ergebnisliste[0])
    #print("Liste ", level, ": ", liste)
    return liste


def processList(complete_list):
    """
    takes the complete_list and overwrites it with the sorted cefr word data.
    :complete_list: List
    :return: List
    """
    A1_set = set(complete_list[0])
    A2_set = set(complete_list[1])
    B1_set = set(complete_list[2])
    B2_set = set(complete_list[3])
    C1_set = set(complete_list[4])
    C2_set = set(complete_list[5])
    
    C2 = list(C2_set - C1_set - B2_set - B1_set - A2_set - A1_set)
    C1 = list(C1_set - B2_set - B1_set - A2_set - A1_set)
    B2 = list(B2_set - B1_set - A2_set - A1_set)
    B1 = list(B1_set - A2_set - A1_set)
    A2 = list(A2_set - A1_set)
    A1 = list(A1_set)
    
    A1.sort()
    A2.sort()
    B1.sort()
    B2.sort()
    C1.sort()
    C2.sort()
    
    complete_list = (A1, A2, B1, B2, C1, C2)
    return complete_list

"""
Add the extracted cefr words to the complete_list, for every language level in the language_level list.
"""    
for level in language_level:
    complete_list.append(extractionFromPdf(level))

"""
Overwrite the current complete list with the processed list data.
"""
complete_list = processList(complete_list)

# Write words into json file
with open("../cefr_vocab_en.json", "w", encoding="utf-8") as output_file:

    words: list = []

    for i in range(0,6):
        for vokabel in complete_list[i]:
            words.append({"word" : str(vokabel.lower()), "level" : str(language_level[i])})

    json.dump(words, output_file)

        
