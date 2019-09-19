#!/usr/bin/env python3.8
# from .bash_history_unique import bash_history_unique
# from .youtube_dl_subtitel import youtube_dl_subtitel
# from .youtube_dl_sync_archive import youtube_dl_sync_archive
# from .umbenennen import umbenennen
# from .umbenennen_mit_internet import umbenennen_mit_internet
# from .pdf_nur_neu_hinzugekommene import pdf_nur_neu_hinzugekommene
# from .djvu_nur_neu_hinzugekommene import djvu_nur_neu_hinzugekommene
# from .bytes_md5_in_pdf_einbetten import bytes_md5_in_pdf_einbetten
# from .doppelt_mit_md5 import doppelt_mit_md5

from . import *

if __name__ == "__main__":
    from fire import Fire

    Fire()

# Pfad zu yyy_py ist ./yyy_py
# bzw yyy_py befindet sich im python path
# python3.8 -m yyy_py
