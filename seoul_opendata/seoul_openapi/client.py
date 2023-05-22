import os
from typing import Final


class SeoulOpenAPI:
    def __init__(self):
        self.key: Final[str] = os.environ["SEOUL_OPENDATA_KEY"]
    
    def 