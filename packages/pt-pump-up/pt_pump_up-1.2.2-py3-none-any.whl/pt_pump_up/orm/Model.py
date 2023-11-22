from beanie import Document, Link
from typing import Optional, List
from pt_pump_up.orm.Conference import Conference
from pt_pump_up.orm.Language import Language
from pydantic import BaseModel
from pt_pump_up.orm.Hrefs import Hrefs
from pt_pump_up.orm.Status import Status
from pt_pump_up.orm.Author import Author
from pt_pump_up.orm.License import License
from pt_pump_up.orm.Architecture import Architecture
from pt_pump_up.orm.Benchmark import Benchmark


class ModelStats(BaseModel):
    languages: List[Link[Language]]
    architecture: Architecture
    number_parameters: Optional[int] = 0
    size_MB: Optional[int] = 0


class Model(Document):
    name: str
    model_stats: ModelStats
    conference: Optional[Conference]
    hrefs: Hrefs
    year: int
    status: Status
    authors: List[Link[Author]]
    license: Optional[Link[License]] = None
    benchmarks: List[Link[Benchmark]]
    nlp_task: List[Link[Language]]
