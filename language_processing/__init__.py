#!/usr/bin/python
# -*- coding: utf-8 -*-
from language_processing.preprocesssing import preprocess
from language_processing.file_search import ranked_documents
from flask import Flask


app = Flask(__name__)
from language_processing import routes
