#!/usr/bin/env python3.8
from sys import stderr
from pathlib import Path


def ü(x):
    return set(x.split('\n'))


def üü(f_s, x):
    return '\n'.join(f_s - x) + '\n'


def youtube_dl_sync_archive(f1_name='/home/v/Sicherung/Ton_Film/youtube-dl_download-archive.txt',
                            f2_name='/run/user/1000/gvfs/mtp:host=Android_Android_D1AGAD1762018430/SanDisk SD card/0_Ton_Film/youtube-dl_download-archive.txt'):
    # fire erkennt keine Path Objekte
    """
    '/home/v/Sicherung/Ton_Film/youtube-dl_download-archive.txt'
    '/run/user/1000/gvfs/mtp:host=Android_Android_D1AGAD1762018430/SanDisk SD card/0_Ton_Film/youtube-dl_download-archive.txt'
    """
    f1 = Path(f1_name)
    f2 = Path(f2_name)
    if not f1.is_file() or not f2.is_file():
        print('Eine der beiden Dateien existiert nicht', file=stderr)
        return

    with open(f1, 'r'), open(f2, 'r'):
        f1_r = f1.read_text()
        f2_r = f2.read_text()

    f_s = (f1_s := ü(f1_r)) | (f2_s := ü(f2_r))

    with open(f1, 'a'), open(f2, 'a'):
        f1.write_text(üü(f_s, f1_s))
        f2.write_text(üü(f_s, f2_s))


if __name__ == "__main__":
    from fire import Fire

    Fire()

# Usage:
# python3.8 youtube-dl_download-archive.txt.py sync 1.txt 2.txt

# youtube-dl_download-archive(){
#   python3.8 /usr/local/software/Skripte/youtube-dl_download-archive.txt.py sync
# }
