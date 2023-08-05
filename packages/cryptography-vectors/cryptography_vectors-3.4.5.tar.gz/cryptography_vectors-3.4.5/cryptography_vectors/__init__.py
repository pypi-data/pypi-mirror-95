# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

import os
import typing

from cryptography_vectors.__about__ import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __uri__,
    __version__,
)


__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]


def open_vector_file(filename: str, mode: str) -> typing.IO:
    base = os.path.dirname(__file__)
    return open(os.path.join(base, filename), mode)
