#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from stempel import StempelStemmer
from autocorrect import Speller
from typing import List, Text, Tuple
from gensim.models import KeyedVectors
import numpy as np
import os


path_to_model = os.path.abspath("language_processing/files/nkjp+wiki-lemmas-all-100-cbow-ns.txt")
model = KeyedVectors.load_word2vec_format(path_to_model, binary=False)
stemmer = StempelStemmer.polimorf()


def get_embedding(word):
    if word in model.key_to_index:
        return model[word]
    else:
        return np.zeros(100)


def preprocess(document: List[Text], query=False) -> Tuple[List[List[List[Text]]], np.array, List[np.array]]:
    """
    Function is used to preprocess and tokenize documents
    :param document: List of pages in document. One page is made of text.
    :param query: Is this preprocessing done for query or document.
    :return: List of pages where each page is list of sentences and each sentence is list of words. Word  embedding
    representing the whole document. List of word embeddings representing each page.
    """
    tokenized_document = []
    page_embeddings = []
    # create list of stopwords from provided file
    stopwords = []
    with open("language_processing/files/polish_stopwords.txt", "r") as file:
        for line in file:
            stopwords.append(line.strip())

    spell = Speller('pl')
    for page, txt in enumerate(document):
        tokenized_document.append([])
        page_embeddings.append(np.zeros(100))
        # remove moving sentences to the next line
        txt = re.sub(r'-\n', "", txt)
        # correct spelling
        txt = spell(txt)
        # remove stopwords
        txt = " ".join(str(word) for word in txt.split() if word.lower() not in stopwords)
        # remove words consisting of 1-3 letters
        txt = re.sub(r'\b[a-zA-ZĄąĆćęĘŁłŃńÓóŚśŹźŻż]{1,3}\b', "", txt)
        # tokenize sentences
        sentence_tokens = sent_tokenize(txt)

        for token in sentence_tokens:
            # remove words containing non word symbols like 'exampl)e'
            token_txt = re.sub(r'(\w*[^a-zA-Z\n\sĄąĆćęĘŁłŃńÓóŚśŹźŻż]\w*)+', "", token)
            # replace unwanted signs with space
            token_txt = re.sub(r'[^a-zA-Z\n\sĄąĆćęĘŁłŃńÓóŚśŹźŻż]', " ", token_txt)
            # remove words consisting of multiple capital letters
            token_txt = re.sub(r"\w*[A-Z]\w*[A-Z]\w*", "", token_txt)
            # apply stemming and change letters to lower
            token_txt = token_txt.split()
            none_words = []
            for i in range(len(token_txt)):
                token_txt[i] = stemmer.stem(token_txt[i].lower())
                if token_txt[i] is None:
                    none_words.append(i)
            for el in none_words:
                # romove words which are equal to None
                token_txt.pop(el)
            token_txt = " ".join(token_txt)
            # remove words with repeated characters like 'dfrrrw'
            token_txt = re.sub(r'\b\w*(\w)\1\w*\b', "", token_txt)
            # remove words consisting of 1-3 words
            token_txt = re.sub(r'\b(\w{1,3})\b', "", token_txt)
            # replace multiple spaces with one space
            token_txt = re.sub(r'\s{2,}', " ", token_txt)
            # remove repeating words
            token_txt = re.sub(r'\b(\w+)(\s\1)+\b', "\1", token_txt)
            # remove line breaks
            token_txt = re.sub(r'\n+', "", token_txt)
            token_txt = word_tokenize(token_txt)

            if query or (not query and len(token_txt) > 3):
                tokenized_document[page].append(token_txt)
                page_embeddings[page] = np.mean(np.array([get_embedding(x) for x in token_txt]), axis=0)

    document_embedding = np.mean(np.array(page_embeddings), axis=0)

    return tokenized_document, document_embedding, page_embeddings
