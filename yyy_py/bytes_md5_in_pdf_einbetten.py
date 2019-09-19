#!/usr/bin/env python3.8
from shutil import move, copy2, rmtree, copystat
from subprocess import run
from pathlib import Path
from .pdf_nur_neu_hinzugekommene import md5_b, schon_fertig
from .umbenennen import punkt
from tempfile import TemporaryDirectory
from tempfile import mkdtemp
from pysnooper import snoop


# t = (t := subprocess.run(cmdlist, cwd=punkt, text=True, capture_output=True)).stdout
# "pdftotext", "-f", "1", "-l", "12", alterName, "-"]

# x = true_value if condition else false_value

# if not re.search("bytes [0-9]{1,12} md5 [0-9a-f]{32} (pdf|djvu|epub)",
# str(subprocess.run(["pdfinfo", f"{x}"], stdout=subprocess.PIPE).stdout)) else None


def konvertierung(i: Path):
    with TemporaryDirectory() as tmpDirName:
        tmpDir = Path(tmpDirName)
        ii_original = move(i.as_posix(), tmpDir)
        copy2(ii_original, tmpDir / 'a.pdf')
        run(['ps2pdf', (tmpDir / 'a.pdf').as_posix(), (tmpDir / 'b.pdf').as_posix()], cwd=tmpDir)
        rmtree(tmpDir / 'a.pdf', ignore_errors=True)
        run(['exiftool', '-Creator=' + md5_b(tmpDir / ii_original), '-overwrite_original',
             (tmpDir / 'a.pdf').as_posix()], cwd=tmpDir)
        run(['qpdf', '--linearize', (tmpDir / 'a.pdf').as_posix(), (tmpDir / 'b.pdf').as_posix()], cwd=tmpDir)
        move(tmpDir / 'b.pdf', i)
        copystat(tmpDir / ii_original, i)


@snoop(prefix='ß__ ')
def bytes_md5_in_pdf_einbetten(i_name: str):  # fire erkennt keine Path Objekte
    i = Path(i_name)
    kopien = mkdtemp(prefix='tmp_kopien_zumLoeschen', dir=punkt)
    if i.name.lower().endswith('.pdf') and i.is_file() and not schon_fertig.search(
            run(['pdfinfo', (punkt / i).as_posix()], cwd=punkt, text=True, capture_output=True).stdout):
        copy2(i, kopien)
        konvertierung(i)


if __name__ == "__main__":
    from fire import Fire

    Fire()
