## Bangla Ovidhan

This is an open source Bangla dictionary. I created it for use with [KOReader](https://koreader.rocks), but it can be
used with anything that supports the StarDict format.

The data is located in the file `ovidhan.db`, which is an SQLite database.

The script `convert.py` and the website [dictz.github.io](https://dictz.github.io) are then used to generate the files
inside the `stardict` directory. One can directly copy that directory inside `<koreader>/data/dict` to use it in
KOReader.

An alternative dictionary is located inside `alt`, but it has a different schema, and I offer no scripts for conversion.

## Notes:

1. The database `ovidhan.db` is generated from content provided by [alphatat/ovidhan](https://github.com/alphatat/ovidhan).
1. The database `alt/dictionary.db` is generated from content provided by
   [https://github.com/bipsec/bangla-dictionary-PyPI](https://github.com/bipsec/bangla-dictionary-PyPI).
