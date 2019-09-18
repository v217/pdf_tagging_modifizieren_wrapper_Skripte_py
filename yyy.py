#!/usr/bin/env python3.8
from yyy_py.bash_history_unique import bash_history_unique
from yyy_py.youtube_dl_subtitel import youtube_dl_subtitel
from yyy_py.youtube_dl_sync_archive import youtube_dl_sync_archive
from yyy_py.umbenennen import umbenennen
from yyy_py.umbenennen_mit_internet import umbenennen_mit_internet
from yyy_py.pdf_nur_neu_hinzugekommene import pdf_nur_neu_hinzugekommene
from yyy_py.djvu_nur_neu_hinzugekommene import djvu_nur_neu_hinzugekommene
from yyy_py.bytes_md5_in_pdf_einbetten import bytes_md5_in_pdf_einbetten
from yyy_py.doppelt_mit_md5 import doppelt_mit_md5

if __name__ == "__main__":
    from fire import Fire

    Fire()
