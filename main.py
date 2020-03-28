from src.categorize_en import categorizeText

text = input('Type your text: ')

level_data = categorizeText(text)

print(level_data)