import os
import platform
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

_quality = {
    0: '/default',
    1: '/prepress',
    2: '/printer',
    3: '/ebook',
    4: '/screen'
}


def compress(source: str | os.PathLike | bytes,
             save_path: str | os.PathLike,
             power: int,
             ghostscript_command: str = None) -> None:
    if isinstance(source, bytes):
        _bytes_compress(source=source,
                        save_path=save_path,
                        power=power,
                        ghostscript_command=ghostscript_command)
    else:
        _base_compress(source=source,
                       save_path=save_path,
                       power=power,
                       ghostscript_command=ghostscript_command)


def _base_compress(source: str | os.PathLike,
                   save_path: str | os.PathLike,
                   power: int,
                   ghostscript_command: str | None) -> None:
    source = Path(source)
    save_path = Path(save_path)

    if ghostscript_command is None:
        if platform.system() == 'Windows':
            if platform.machine().endswith('64'):
                ghostscript_command = 'gswin64c'
            else:
                ghostscript_command = 'gswin32c'
        else:
            ghostscript_command = 'gs'

    if not source.is_file():
        raise FileNotFoundError('invalid path for input PDF file')

    if source.suffix != '.pdf':
        raise ValueError('Input file must be a .pdf file')

    subprocess.call([ghostscript_command,
                     '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                     '-dPDFSETTINGS={}'.format(_quality[power]),
                     '-dNOPAUSE', '-dQUIET', '-dBATCH',
                     '-sOutputFile={}'.format(save_path.as_posix()),
                     source.as_posix()],
                    shell=platform.system() == 'Windows'
                    )


def _bytes_compress(source: bytes,
                    save_path: str | os.PathLike,
                    power: int,
                    ghostscript_command: str | None) -> None:
    with NamedTemporaryFile(suffix='.pdf', delete_on_close=platform.system() != 'Windows') as tmp_file:
        tmp_file.write(source)
        _base_compress(source=tmp_file.name,
                       save_path=save_path,
                       power=power,
                       ghostscript_command=ghostscript_command)
