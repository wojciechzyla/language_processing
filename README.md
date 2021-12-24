# General information

This applcation is a part of [panelstudenta][pan] project. It is used in two different situations:
- preprocess text which has been extracted from images and convert it to word embeddings and document embedding,
- work as search engine trying to find best matches for user's query among documents and return documents ranked by their similarity to the query.

This application makes calls to panelstudenta api, that is why appropriate environment variable with endpoint needs to be set:

```URL_PANEL=http://host:port/imgtxt/files/nlp_receive```

[pan]:<https://github.com/wojciechzyla/panelstudenta>
