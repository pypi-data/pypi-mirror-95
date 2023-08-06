"""This package provides a codec for bencoded data.

The official Bencoding specification can be found at the following address:
https://wiki.theory.org/index.php/BitTorrentSpecification#Bencoding
"""


from .decoder import decode                 # noqa: F401
from .encoder import encode, iterencode     # noqa: F401
