from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import TypedDict

from datamx.models.values import Groups
from datamx.utils.search_utils import find_first


# class Fields:
#     def __init__(self):
#         self.no_op = lambda reading: None
#         self.field_dict = {}
#
#     def add(self, field_name, model_name, value_id):
#         self.field_dict[field_name] = self.create_reading_lambda(model_name, value_id)
#
#     def get_value(self, field_name: str, reading: Groups):
#         get_function = self.field_dict[field_name]
#         return get_function(reading)
#
#     @staticmethod
#     def create_reading_lambda(model_name, value_id):
#         return lambda reading: find_first(reading, model_name, value_id)


@dataclass
class StatusOptions:
    cache: Path
    completed: Path
    publish_limit: int = 30
    net_flag: int = None
    cumulative_flag: int = None
    # fields: Fields = Fields()
