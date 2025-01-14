import os
import pandas as pd
from bs4 import BeautifulSoup
from input_processing_functions import text_classification, duplicate_handler, empty_lines_handler

source = r"..\html"
directories = [x[0] for x in os.walk(source)]

# List all files in given directory
files = []
for directory in directories:
    for file in os.listdir(directory):
        if file.endswith(".html") and file[2] == "_" and file[5] != "-":
            files.append(file)

# Create DataFrame with file paths and volume numbers
df_Library = pd.DataFrame(data=files, columns=["filename"])
df_Library["path"] = source + "\\" + df_Library["filename"].str[:2] + "\\" + df_Library["filename"]
df_Library["volume"] = df_Library["filename"].str[1]
df_Library = df_Library[["path", "volume"]]

dune_cronicles = []

for book in range(1, 9):  # Main loop over each book
    Dune = df_Library[df_Library["volume"] == str(book)]["path"]
    chapter = 0

    for html_file in Dune:  # Main loop over each chapter
        with open(html_file, encoding="utf8") as markup:
            soup = BeautifulSoup(markup, 'html.parser')

            AllParagraphs = soup.body.find_all(['p', 'blockquote'])
            for row, paragraph in enumerate(AllParagraphs):
                text_classification(dune_cronicles, book, chapter, paragraph)

# Adjust chapter numbers for 1st pages with volume names
for row, value in enumerate(dune_cronicles):
    if value[1] == 0:
        dune_cronicles[row][1] = 1

df_DuneCronicles = pd.DataFrame(data=dune_cronicles, columns=['Book', 'Chapter', 'Class', 'Text'])

duplicates_list, empty_lines_list = [], []
for row in range(0, len(dune_cronicles)):  # range --> enumerate
    DuneCronicles_row = dune_cronicles[row]
    duplicate_handler(duplicates_list, DuneCronicles_row)
    empty_lines_handler(empty_lines_list, DuneCronicles_row)

duplicates_list.insert(0, False)
duplicates_list = duplicates_list[0:len(duplicates_list) - 1]

df_DuneCronicles['DuplicateLines'] = duplicates_list
df_DuneCronicles['EmptyLines'] = empty_lines_list

df_DuneCronicles = df_DuneCronicles[df_DuneCronicles['DuplicateLines'] == False]
df_DuneCronicles = df_DuneCronicles[df_DuneCronicles['EmptyLines'] == False]
df_DuneCronicles.reset_index(drop=True, inplace=True)

Class_Identifiers = pd.read_excel(r'data\Class_Identifiers.xlsx')

df_DuneCronicles = df_DuneCronicles.merge(Class_Identifiers,
                                          how='left',
                                          on=['Book', 'Class'],
                                          sort=False)

output_columns = ['Book', 'Chapter', 'Class', 'Identifier_A', 'Identifier_B', 'Text']
output_filename = r'output\DuneCronicles.csv'

df_DuneCronicles = df_DuneCronicles[output_columns]
df_DuneCronicles.to_csv(output_filename, index=False, encoding='utf-8')
