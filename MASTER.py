from os import listdir, getcwd
from os.path import isfile, join
import pandas as pd

book_dir = getcwd() + r"\excel"
books = [join(book_dir, f) for f in listdir(book_dir) if isfile(join(book_dir, f))]

Characters = pd.read_excel(books[0])
Dune = pd.read_excel(books[1])
