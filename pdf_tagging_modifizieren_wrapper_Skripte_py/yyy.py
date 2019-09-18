#!/usr/bin/env python3.8
from eigene_skripte_py.bash_history_unique import bash_history_unique
from eigene_skripte_py.youtube_dl_subtitel import youtube_dl_subtitel
from eigene_skripte_py.youtube_dl_sync_archive import youtube_dl_sync_archive
from eigene_skripte_py.umbenennen import umbenennen
from eigene_skripte_py.umbenennen_mit_internet import umbenennen_mit_internet
from eigene_skripte_py.pdf_nur_neu_hinzugekommene import pdf_nur_neu_hinzugekommene
from eigene_skripte_py.djvu_nur_neu_hinzugekommene import djvu_nur_neu_hinzugekommene
from eigene_skripte_py.bytes_md5_in_pdf_einbetten import bytes_md5_in_pdf_einbetten
from eigene_skripte_py.doppelt_mit_md5 import doppelt_mit_md5

if __name__ == "__main__":
    from fire import Fire

    Fire()
