#!/usr/bin/env python3

import sqlite3
import struct
import os
from subprocess import run
from pathlib import Path

DB_FILE = "ovidhan.db"
BOOK_NAME = "Ovidhan (Bengali)"

IFO_FILE = "stardict/ovidhan.ifo"
IDX_FILE = "stardict/ovidhan.idx"
DICT_FILE = "stardict/ovidhan.dict"
SYN_FILE = "stardict/ovidhan.syn"
try:
    os.mkdir("stardict")
except FileExistsError:
    pass

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

rows = cur.execute("""
SELECT
    word,
    pronun,
    origlan,
    origetym,
    pos,
    meaning,
    examples,
    engmean
FROM shobdo
ORDER BY word COLLATE NOCASE
""").fetchall()

offset = 0
idx_entries = []
syn_entries = []

with open(DICT_FILE, "wb") as dictfp:
    for article_index, row in enumerate(rows):
        word = (row[0] or "").strip()

        if not word:
            continue

        labels = [
            "উচ্চারণ",  # Pronunciation
            "ভাষাগত উৎস",  # Origin Language
            "শব্দমূল",  # Etymology
            "শব্দের শ্রেণি",  # Part of Speech
            "অর্থ",  # Meaning
            "উদাহরণ",  # Examples
            "ইংরেজি অর্থ",  # English Meaning
        ]

        article_lines = []

        for label, value in zip(labels, row[1:]):
            if value:
                article_lines.append(f"{label}: {value}")

        article_text = "\n".join(article_lines)
        article_bytes = article_text.encode("utf-8")

        dictfp.write(article_bytes)

        idx_entries.append(
            word.encode("utf-8") + b"\0" + struct.pack(">II", offset, len(article_bytes))
        )

        # Optional synonym generation from pronun
        pronun = (row[1] or "").strip()

        if pronun and pronun != word:
            syn_entries.append(pronun.encode("utf-8") + b"\0" + struct.pack(">I", article_index))

        offset += len(article_bytes)

run(f"dictzip {DICT_FILE}", shell=True, check=True)

with open(IDX_FILE, "wb") as fp:
    for item in idx_entries:
        fp.write(item)

with open(SYN_FILE, "wb") as fp:
    for item in sorted(syn_entries):
        fp.write(item)

idxfilesize = Path(IDX_FILE).stat().st_size

with open(IFO_FILE, "w", encoding="utf-8") as fp:
    fp.write("StarDict's dict ifo file\n")
    fp.write("version=2.4.2\n")
    fp.write(f"wordcount={len(idx_entries)}\n")
    fp.write(f"synwordcount={len(syn_entries)}\n")
    fp.write(f"idxfilesize={idxfilesize}\n")
    fp.write(f"bookname={BOOK_NAME}\n")
    fp.write("sametypesequence=m\n")

print("Done.")
print("Words:", len(idx_entries))
print("Synonyms:", len(syn_entries))
print("Generated:")
print(" ", IFO_FILE)
print(" ", IDX_FILE)
print(" ", DICT_FILE + ".dz")
print(" ", SYN_FILE)
