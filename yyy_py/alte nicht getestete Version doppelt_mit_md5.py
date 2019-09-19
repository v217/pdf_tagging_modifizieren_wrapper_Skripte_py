#!/usr/bin/env python3.8
from subprocess import run
from .umbenennen import punkt
from .pdf_nur_neu_hinzugekommene import schon_fertig
from os import remove
from pathlib import Path  # nur für type hint importiert
from pysnooper import snoop

tag_pfad = {}


def doppelte(tag, datei: Path, rm=False):
    if tag in tag_pfad:
        print('\n #   ' + tag_pfad[tag].as_posix() + "\n rm  '" + datei.as_posix() + "'")
        if rm:
            remove(datei)
    else:
        tag_pfad[tag] = datei


# rglob folgt nicht symlinks
def pdf_dateien_mit_md5(rm=False):
    return (doppelte(m.group(0), i, rm) for i in punkt.rglob('*.pdf') if i.is_file() and (m := schon_fertig.search(
        run(['pdfinfo', (punkt / i).as_posix()], cwd=punkt, text=True, capture_output=True).stdout)))


# @snoop(prefix='ß__ ')
def doppelt_mit_md5(rm=False):
    for i in pdf_dateien_mit_md5(rm):
        pass


if __name__ == "__main__":
    from fire import Fire

    Fire()
