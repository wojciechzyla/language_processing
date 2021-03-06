#!/usr/bin/python
# -*- coding: utf-8 -*-
from scipy.spatial.distance import cosine
from language_processing.preprocesssing import preprocess
from language_processing.utils import HeapSort, ListElement
from typing import List, Dict
import numpy as np


def get_sim(query_embedding, average_vector_doc):
    """
    :param query_embedding: Word embedding of query
    :param average_vector_doc: Word embedding of documents
    :return: Cosine similarity of two vectors
    """
    sim = [1 - cosine(query_embedding, average_vector_doc)]
    return sim


def ranked_documents(query: str, documents: List[Dict], doc_amount: int) -> List[List]:
    """
    This function is used to rank documents based on their similarity to searched query.

    :param query: Query provided by user
    :param documents: List of dictionaries, where each dictionary consists of following
    keys and values: name -> name of document, embedding -> embedding of the whole document,
    pages -> list of embeddings of consecutive pages.
    :param doc_amount: Number of sorted documents to return
    :return: Sorted list of lists, where first element of each of embedded list is name of the document and
    the second element is index of most accurate page in that document.
    """
    # Get embedding of query
    _, query_embedding, _ = preprocess([query], query=True)
    # List for storing ranked documents
    rank = []
    heap_sort = HeapSort()
    for document in documents:
        # Similarity between query and document
        doc_sim = get_sim(query_embedding, np.array(document["embedding"]))
        # Best matching page in document
        best_page = 0
        # Similarity between query and best page
        best_page_sim = get_sim(query_embedding, np.array(document["pages"][0]))
        for i, page in enumerate(document["pages"]):
            page_sim = get_sim(query_embedding, np.array(page))
            if page_sim > best_page_sim and np.mean(np.array(page)) > 0:
                best_page = i
                best_page_sim = page_sim
        rank.append(ListElement(priority=doc_sim, data=[document["name"], best_page]))
    heap_sort.heapify(rank)
    rank = heap_sort.sort(amount=doc_amount)
    return rank
