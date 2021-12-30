import pandas as pd
a = pd.read_excel('Standard streets.xlsx')
a['Unnamed: 0']=a['Unnamed: 0'].str.lower()
a['Unnamed: 1']=a['Unnamed: 1'].str.lower()
dict(zip(a['Unnamed: 0'], a['Unnamed: 1']))
dict1 = a.set_index('Unnamed: 0').to_dict()['Unnamed: 1']
from nltk import word_tokenize
from nltk.tokenize import MWETokenizer
def multiword_tokenize(text, mwe):
    # Initialize the MWETokenizer
    print(mwe)
    protected_tuples = [word_tokenize(word) for word in mwe]
    protected_tuples_underscore = ['_'.join(word) for word in protected_tuples]
    tokenizer = MWETokenizer(protected_tuples)
    # Tokenize the text.
    tokenized_text = tokenizer.tokenize(word_tokenize(text))
    # Replace the underscored protected words with the original MWE
    for i, token in enumerate(tokenized_text):
        if token in protected_tuples_underscore:
            tokenized_text[i] = mwe[protected_tuples_underscore.index(token)]
    return tokenized_text
