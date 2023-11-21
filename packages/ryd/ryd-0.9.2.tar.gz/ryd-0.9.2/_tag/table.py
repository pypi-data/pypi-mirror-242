# coding: 'utf-8'

from __future__ import annotations

import os
from ryd._tag._handler import BaseHandler
import ruamel.yaml
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Table(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)

    def __call__(self, d: Any) -> None:
        """
        create a table, for now headerless
        input can be
        - a mapping from first column to second column (if scalar), or other columns (if sequence)
        - a list of lists
        calls add_table with a list of lists
        """
        if isinstance(d, dict):
            # assume a mapping from first column to either second column or list of other columns
            s = []
            for col1 in d:
                row = [col1]
                s.append(row)
                if isinstance(d[col1], list):
                    for x in d[col1]:
                        row.append(self.expand_env(x))
                    row.extend(d[col1])
                else:
                    row.append(self.expand_env(d[col1]))
        else:
            assert isinstance(d, list)
            assert isinstance(d[0], list)
            s = d
        self.c.add_table(s)

    def expand_env(self, s):
        if isinstance(s, ruamel.yaml.comments.TaggedScalar) and s.tag == '!Env':
             env_s = os.environ.get(str(s).upper(), s)
             # print('s', s, env_s)
             return env_s
        return s
