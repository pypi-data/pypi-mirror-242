from beanie import Document
from pt_pump_up.orm.Metric import Metric
from pt_pump_up.orm.Dataset import Dataset
from beanie import Link
from typing import List


class Benchmark(Document):
    train_dataset: List[Link[Dataset]]
    test_dataset: List[Link[Dataset]]
    metric: List[Link[Metric]]
