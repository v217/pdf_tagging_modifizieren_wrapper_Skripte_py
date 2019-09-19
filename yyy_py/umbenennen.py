#!/usr/bin/env python3.8
from subprocess import run
from pathlib import Path
from re import sub
from shutil import move
from typing import Callable
from pysnooper import snoop

punkt = Path.cwd()

erlaubte_zeichen = ' _-'


def duplikate_loeschen():  # r('set -xv; cd ' + cwd + ' ; fdupes -I .')
    print(run(['fdupes', '-dN', '--order=time', punkt.as_posix()], cwd=punkt).args)


def neuer_name(n: Path):
    b = sub(r'Muster1|Muster2|[-_ .]+', ' ', n.stem)
    b = "".join(c for c in b if c.isalnum() or c in erlaubte_zeichen).strip(erlaubte_zeichen + '.')
    if (neu := b + n.suffix.lower()) != n.name:
        return Path(neu)
    else:
        return None


def namenskollision(n: Path, i=0):
    if i == 0:
        n_neu = n
    else:
        b_neu = n.stem + ' ' + str(i)
        n_neu = Path(b_neu + n.suffix.lower())
    if n_neu.exists():
        return namenskollision(n, i + 1)
    else:
        return n_neu


def verschieben(i: Path, i_neu: Path):
    print(i.name + '\n' + i_neu.name + '\n')
    move(i, i_neu)


def dateien(neuer_name: Callable):
    return (verschieben(i, namenskollision(neu)) for i in punkt.iterdir() if
            i.name.lower().endswith(('.epub', '.pdf', '.djvu')) and i.is_file() and (neu := neuer_name(i)))


# @snoop(prefix='ß__ ')
def umbenennen():
    duplikate_loeschen()
    for d in dateien(neuer_name):
        pass


if __name__ == "__main__":
    from fire import Fire

    Fire()
