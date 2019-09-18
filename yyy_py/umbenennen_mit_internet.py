#!/usr/bin/env python3.8
from isbnlib import get_isbnlike, isbn_from_words, meta
from subprocess import run
from pathlib import Path
from yyy_py.umbenennen import umbenennen, dateien, erlaubte_zeichen, punkt
from pysnooper import snoop


def text(alterPfad: Path):
    # sudo apt-get install mupdf-tools djvulibre-bin poppler-utils
    s = alterPfad.suffix.lower()
    nn = (punkt / alterPfad).as_posix()
    cmdlist = ["pdftotext", "-f", "1", "-l", "12", nn, "-"] if s == '.pdf' else (
        ["djvutxt", "--pages=1-12", nn] if s == '.djvu' else ['mutool', 'convert', '-F', 'text', nn, '1-15'])

    try:
        tt = (t := run(cmdlist, cwd=punkt, text=True, capture_output=True)).stdout
        print(t.args)
    except:
        return None

    if len(tt) > 9:
        return tt
    return None

# @snoop(prefix='ß_abg__ ')
def abgerufen(text, pfad: Path):
    if text:
        isbns = get_isbnlike(str(text), level='normal')
    if len(isbns) == 0:
        isbns = [isbn_from_words(str(pfad.stem))]
    if len(isbns) == 0:
        return None

    m = None
    for isbn in isbns:
        try:
            m = meta(isbn)
            if m:
                break
        except:
            continue
    return m

# @snoop(prefix='ß_b_mit__ ')
def b_mit_abgerufen(abgerufen):
    autoren_liste = abgerufen['Authors']
    autoren = ' '.join([' '.join(i.split(' ')[-1:]) for i in autoren_liste])
    b = autoren + ' ' + abgerufen['Year'] + ' ' + abgerufen['Title']
    b = autoren_liste[0] + ' ' + abgerufen['Year'] + ' ' + abgerufen['Title'][:190 - len(autoren_liste[0])] if len(
        b) > 190 else b

    # http://stackoverflow.com/questions/7406102/create-sane-safe-filename-from-any-unsafe-string
    return "".join(c for c in b if c.isalnum() or c in erlaubte_zeichen).strip(str(erlaubte_zeichen))


@snoop(prefix='ß__ ')
def neuer_name(alterPfad: Path):
    t = text(alterPfad)
    m = abgerufen(t, alterPfad.suffix.lower())
    if m and alterPfad.stem != (b := b_mit_abgerufen(m)):
        return Path(b + alterPfad.suffix.lower())
    return None


def umbenennen_mit_internet():
    umbenennen()
    for d in dateien(neuer_name):
        pass


if __name__ == "__main__":
    from fire import Fire

    Fire()
