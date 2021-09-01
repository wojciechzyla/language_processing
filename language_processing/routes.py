#!/usr/bin/python
# -*- coding: utf-8 -*-
from language_processing import app, preprocess, ranked_documents
from flask import request, Response
import json


@app.route("/preprocess", methods=['POST'])
def preprocess_route():
    if not request.is_json:
        message = json.dumps({"info": "No json file included"})
        resp = Response(message, status=406, mimetype='application/json')
        return resp
    document = request.get_json()["text"]
    try:
        preprocessed = preprocess(document)
    except:
        preprocessed = None
    if preprocessed:
        tokenized_document, document_embedding, page_embeddings = preprocessed
        response_json = {}
        for i, page in enumerate(tokenized_document):
            response_json[f'Page{i}'] = page
            response_json[f'Embedding{i}'] = page_embeddings[i].tolist()
        response_json[f'Doc_embedding'] = document_embedding.tolist()
        resp = Response(json.dumps(response_json), status=200, mimetype='application/json')
        return resp
    else:
        message = json.dumps({"info": "Problem with text preprocessing"})
        resp = Response(json.dumps(message), status=500, mimetype='application/json')
        return resp


@app.route("/rank", methods=['POST'])
def rank_route():
    if not request.is_json:
        message = json.dumps({"info": "No json file included"})
        resp = Response(message, status=406, mimetype='application/json')
        return resp
    query = request.get_json()["query"]
    documents = request.get_json()["documents"]
    doc_amount = request.get_json()["doc_amount"]
    try:
        ranked = ranked_documents(query=query, documents=documents, doc_amount=doc_amount)
    except:
        ranked = None
    if ranked:
        message = {"results": ranked}
        resp = Response(json.dumps(message), status=200, mimetype='application/json')
        return resp
    else:
        message = json.dumps({"info": "Problem with ranking documents"})
        resp = Response(json.dumps(message), status=500, mimetype='application/json')
        return resp
