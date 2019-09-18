#!/usr/bin/env python3.8
from subprocess import run
from itertools import groupby
from os import remove
from yyy_py.umbenennen import punkt
from yyy_py.pdf_nur_neu_hinzugekommene import schon_fertig
from pathlib import Path  # nur für type hint importiert
from pysnooper import snoop

pfad_tag = []


def doppelte(pfad: Path, tag: str):
    pfad_tag.append((pfad, tag))


def ordnen(ordn):
    return ordn[1]


# rglob folgt nicht symlinks
pdf_dateien_mit_md5 = (doppelte(i, m.group(0)) for i in punkt.rglob('*.pdf') if i.is_file() and (
    m := schon_fertig.search(
        run(['pdfinfo', (punkt / i).as_posix()], cwd=punkt, text=True, capture_output=True).stdout)))


# @snoop(prefix='ß__ ')
def doppelt_mit_md5(rm=False):
    for i in pdf_dateien_mit_md5:
        pass
    # file:///usr/share/doc/python3.8/html/howto/functional.html?highlight=itertools#grouping-elements
    # vor groupby immer sorted
    d = sorted(pfad_tag, key=ordnen)
    dd = groupby(d, ordnen)
    # aufgrund von groupby konnte ich len Kondition nicht in folgender list comprehension verwenden??
    for (a, *aa) in filter(lambda x: len(x) > 1, [[j[0] for j in i[1]] for i in dd]):
        print("\n #   {}".format(a.as_posix()))
        for k in aa:
            print(" rm '{}'".format(k.as_posix()))
            if rm:
                remove(k)


if __name__ == "__main__":
    from fire import Fire

    Fire()

# for i in dd:
#     a, *aa = [j[0] for j in i[1]]
#     if len(aa) > 0:
#         print("\n #   {}".format(a.as_posix()))
#         for k in aa:
#             print(" rm '{}'".format(k.as_posix()))
#             if rm:
#                 remove(k)
