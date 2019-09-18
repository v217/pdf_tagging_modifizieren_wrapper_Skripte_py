#!/usr/bin/env python3.8
from shutil import move, copy2, copystat
from subprocess import run
from re import compile
from pathlib import Path
from eigene_skripte_py.umbenennen import umbenennen, punkt
from tempfile import TemporaryDirectory
from tempfile import mkdtemp
from hashlib import md5
from os import rmdir
from typing import Callable
from pysnooper import snoop

# t = (t := subprocess.run(cmdlist, cwd=punkt, text=True, capture_output=True)).stdout
# "pdftotext", "-f", "1", "-l", "12", alterName, "-"]

# x = true_value if condition else false_value

# if not re.search("bytes [0-9]{1,12} md5 [0-9a-f]{32} (pdf|djvu|epub)",
# str(subprocess.run(["pdfinfo", f"{x}"], stdout=subprocess.PIPE).stdout)) else None

schon_fertig = compile(r'bytes [0-9]{1,12} md5 [0-9a-f]{32} (pdf|djvu|epub)')


def md5_b(i: Path):  # bytes 28462853 md5 46d53e4784c1f1ea41476aa873dd3122 djvu
    md5_hash = md5(open(i, "rb").read()).hexdigest()
    i_bytes = str(i.stat().st_size)
    return 'bytes ' + i_bytes + ' md5 ' + md5_hash + ' ' + (i.suffix.strip('.')).lower()


def konvertierung(i: Path, ocr=True):
    with TemporaryDirectory() as tmpDirName:
        tmpDir = Path(tmpDirName)
        ii_original = move(i.as_posix(), tmpDir)
        copy2(ii_original, tmpDir / 'a.pdf')
        run(['k2pdfopt', '-mode', 'fp', '-x', '-rt', 'auto', '-ui-', '-o', (tmpDir / 'b.pdf').as_posix(),
             (tmpDir / 'a.pdf').as_posix()], cwd=tmpDir)
        run(['ps2pdf', (tmpDir / 'b.pdf').as_posix(), (tmpDir / 'c.pdf').as_posix()], cwd=tmpDir)
        run(['exiftool', '-Creator=' + md5_b(tmpDir / ii_original), '-overwrite_original',
             (tmpDir / 'c.pdf').as_posix()], cwd=tmpDir)
        run(['qpdf', '--linearize', (tmpDir / 'c.pdf').as_posix(), (tmpDir / 'd.pdf').as_posix()], cwd=tmpDir)
        move(tmpDir / 'd.pdf', i)
        copystat(tmpDir / ii_original, i)


pdf_dateien = (i for i in punkt.iterdir() if i.name.lower().endswith('.pdf') and i.is_file() and (
    not schon_fertig.search(
        run(['pdfinfo', (punkt / i).as_posix()], cwd=punkt, text=True, capture_output=True).stdout)))


def alle_neuen_konvertieren(suffix_dateien: Path, konv: Callable, ocr=True):
    kopien = mkdtemp(prefix='tmp_kopien_zumLoeschen', dir=punkt)
    for i in suffix_dateien:
        copy2(i, kopien)
        konv(i, ocr)
    try:
        rmdir(kopien)
    except OSError:
        pass


# @snoop(prefix='ß__ ')
def pdf_nur_neu_hinzugekommene():
    umbenennen()
    alle_neuen_konvertieren(pdf_dateien, konvertierung)


if __name__ == "__main__":
    from fire import Fire

    Fire()
