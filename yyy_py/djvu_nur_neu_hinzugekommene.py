#!/usr/bin/env python3.8
from shutil import move, copy2, rmtree, copystat
from subprocess import run
from pathlib import Path
from .umbenennen import umbenennen, punkt
from .pdf_nur_neu_hinzugekommene import md5_b, alle_neuen_konvertieren
from tempfile import TemporaryDirectory
from pysnooper import snoop


# t = (t := subprocess.run(cmdlist, cwd=punkt, text=True, capture_output=True)).stdout
# "pdftotext", "-f", "1", "-l", "12", alterName, "-"]

# x = true_value if condition else false_value

# if not re.search("bytes [0-9]{1,12} md5 [0-9a-f]{32} (pdf|djvu|epub)",
# str(subprocess.run(["pdfinfo", f"{x}"], stdout=subprocess.PIPE).stdout)) else None


def konvertierung(i: Path, ocr=True):
    with TemporaryDirectory() as tmpDirName:
        tmpDir = Path(tmpDirName)
        ii_original = move(i.as_posix(), tmpDir)
        copy2(ii_original, tmpDir / 'a.djvu')
        run(['ddjvu', '-format=tiff', '-quality=deflate', (tmpDir / 'a.djvu').as_posix(),
             (tmpDir / 'a.tiff').as_posix()], cwd=tmpDir)
        run(['tiff2pdf', '-F', '-z', '-p', 'A4', '-o', (tmpDir / 'a.pdf').as_posix(), (tmpDir / 'a.tiff').as_posix()],
            cwd=tmpDir)
        run(['k2pdfopt', '-mode', 'fp', '-rt', 'auto', '-x', '-ui-', '-o', (tmpDir / 'b.pdf').as_posix(),
             (tmpDir / 'a.pdf').as_posix()], cwd=tmpDir)

        if ocr:
            run(['/usr/local/bin/k2pdfopt', '-n-', '-wrap-', '-col', '1', '-vb', '-2', '-w', '1s', '-h', '1s', '-rt',
                 '0', '-c', '-t-', '-f2p', '-2', '-m', '0', '-om', '0', '-pl', '0', '-pr', '0', '-pt', '0', '-pb', '0',
                 '-mc-', '-g', '1', '-cmax', '1', '-ocr', 't', '-ocrsp', '-lang', 'eng', '-ui-', '-x', '-odpi', '-1',
                 '-nt', '2', '-o', (tmpDir / 'c.pdf').as_posix(), (tmpDir / 'b.pdf').as_posix()], cwd=tmpDir,
                env={"TESSDATA_PREFIX": "/usr/share/tesseract-ocr/4.00/tessdata"})
            rmtree(tmpDir / 'b.pdf', ignore_errors=True)
            move(tmpDir / 'c.pdf', tmpDir / 'b.pdf')

        run(['exiftool', '-Creator=' + md5_b(tmpDir / ii_original), '-overwrite_original',
             (tmpDir / 'b.pdf').as_posix()], cwd=tmpDir)
        run(['qpdf', '--linearize', (tmpDir / 'b.pdf').as_posix(), (tmpDir / 'c.pdf').as_posix()], cwd=tmpDir)
        move(tmpDir / 'c.pdf', i_pdf := punkt / (i.stem + '.pdf'))
        copystat(tmpDir / ii_original, i_pdf)


djvu_dateien = (i for i in punkt.iterdir() if i.name.lower().endswith('.djvu') and i.is_file())


@snoop(prefix='ß__ ')
def djvu_nur_neu_hinzugekommene(ocr=True):
    umbenennen()
    alle_neuen_konvertieren(djvu_dateien, konvertierung)


if __name__ == "__main__":
    from fire import Fire

    Fire()
