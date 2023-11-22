from beanie import Document
from typing import Optional


class Architecture(Document):
    name: str
    year: Optional[int]
    link_paper: Optional[str]
