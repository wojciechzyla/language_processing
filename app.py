#!/usr/bin/python
# -*- coding: utf-8 -*-
from language_processing import app
import os

if __name__ == '__main__':
    port = os.environ.get("PORT")
    app.run('0.0.0.0', port=port, debug=False)

