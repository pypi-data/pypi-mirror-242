import os
import time
from base64 import b64decode
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Self

from selenium import webdriver

from simplehtmltopdf.compress import compress


class WebDriverWrapper(AbstractContextManager):
    def __init__(self,
                 wait_before_print: int = 2,
                 implicit_wait: int = 10):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(implicit_wait)
        self.wait_before_print = wait_before_print

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.quit()

    def html_to_pdf(self,
                    url: str,
                    save_path: str | os.PathLike,
                    compression: int = None,
                    ghostscript_command: str = None) -> None:
        save_path = Path(save_path)
        self.driver.get(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(self.wait_before_print)
        b64 = self.driver.print_page()
        bites = b64decode(b64, validate=True)
        if compression is not None:
            compress(source=bites,
                     save_path=save_path,
                     power=compression,
                     ghostscript_command=ghostscript_command)
        else:
            with save_path.open(mode='wb') as f:
                f.write(bites)

    def quit(self):
        self.driver.quit()