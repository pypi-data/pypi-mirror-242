# coding: 'utf-8'

from __future__ import annotations

import subprocess
from pathlib import Path
from ryd._tag._handler import ProgramHandler
from typing import Any, TYPE_CHECKING
import ruamel.yaml

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any

pipe_error = '>>>>>> you probably forgot a "|" after "{}" <<<<<<'

class Python(ProgramHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)
        self._pre = ''

    def pre(self, d: Any) -> None:
        """Prefix all following ``!python`` documents with this document (e.g. used for imports)

        This part will not be be shown. The content should be a python snippet, that
        will be used as prefix for following programs which can be incomplete.
        This is useful for  suppressing repetetive import statements.
        """
        self._pre = str(d)

    def __call__(self, d: Any) -> None:
        """
        Include Python program in text. Prefix and mark as executable.
        """
        s = str(d)
        sd = self._pre + s
        # execute, as python-pre might have set something
        self.c.last_output = self.c.check_output(sd)
        if not s.strip():
            return
        self.c.add_code(s, 'python')

    def hidden(self, d: Any) -> None:
        '''Do  not include Python program in text. Prefix and mark as executable.

        This can be used to write files to the output directory, using:
        import pathlib; pathlib.Path("file_name").writetext("""contents of file""")
        No extra newline will be inserted before text following raw output, so
        the program might need to output that
        '''
        s = str(d)
        if not isinstance(d, ruamel.yaml.scalarstring.LiteralScalarString):
            print(pipe_error.format('!python-hidden'))
        sd = self._pre + s
        res = self.c.check_output(sd)
        if res.strip():
            self.c.last_output = res
        # try:
        # except SyntaxError as e:
        #     if not isinstance(d, ruamel.yaml.scalarstring.LiteralScalarString):
        #         print('>>>>>> you probably forgot a "|" after "!python-hidden" <<<<<<')
        #     else:
        #         raise

    def hiddenstdoutraw(self, d: Any) -> None:
        """Do not include Python program in text, insert output as raw in place
        """
        s = str(d)
        if not isinstance(d, ruamel.yaml.scalarstring.LiteralScalarString):
            print(pipe_error.format('!python-hidden'))
        sd = self._pre + s
        res = self.c.check_output(sd)
        if res.strip():
            self.c.last_output = res
        self.c.add_last_output(raw=True)

    def roundtrip(self, s: bytes) -> bytes | None:
        print('python roundtrip')
        # should put
        p = Path('/var/tmp/ryd_roundtrip_doc196.py')
        p.write_bytes(s)
        try:
            subprocess.check_output(['oitnb', str(p)])
        except Exception as e:
            print('error', e)
            if hasattr(e, 'output'):
                print(e.output.decode('utf-8'))
            return None
        return p.read_bytes()
