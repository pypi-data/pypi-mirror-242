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
    save_path = Path(save_path)

    source_was_bytes = False
    if isinstance(source, bytes):
        new_source = NamedTemporaryFile(suffix='.pdf', delete=platform.system() != 'Windows')
        new_source.write(source)
        source = new_source.name
        source_was_bytes = True

    try:
        source = Path(source)

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
    finally:
        if source_was_bytes:
            new_source.close()
