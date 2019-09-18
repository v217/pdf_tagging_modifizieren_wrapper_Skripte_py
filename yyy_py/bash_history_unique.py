#!/usr/bin/env python3.8
from pathlib import Path
from shutil import copyfile


# reversed() ist notwendig damit zuletzt verwendete duplikate Geschichtseintrag erhalten bleibt
def ü(x: str):
    xx = dict.fromkeys(reversed(x.split('\n')))
    return '\n'.join(reversed(xx.keys())) + '\n'


def bash_history_unique(x='/home/v/.bash_history', x_kopie='/home/v/.Sicherungskopie.bash_history'): # fire erkennt keine Path Objekte
    """
    python3.8 bash_history_unique.py bash_history_unique

    python3.8 bash_history_unique.py bash_history_unique '/home/v/.bash_history' '/home/v/.Sicherungskopie.bash_history'


    '/home/v/.bash_history'
    '/home/v/.Sicherungskopie.bash_history'
    """
    x = Path(x)
    x_kopie = Path(x_kopie)

    copyfile(x, x_kopie)

    with open(x, 'r') as y:
        x_r = y.read()

    with open(x, 'w') as y:
        y.write(ü(x_r))


if __name__ == "__main__":
    from fire import Fire

    Fire()
