from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml
from datamx.models.values import BaseSchema
from marshmallow import fields, post_load
from pysunspec_read.options import ConnectOptions, ReadOptions, ReadOptionsSchema, ConnectOptionsSchema, PathField


@dataclass
class PvOutputOptions:
    secret_api_key: str
    system_id: int
    publish_limit: int = 30
    completed_path: Path = None
    cache_path: Path = None
    net_flag: int = None
    cumulative_flag: int = None


class PvOutputOptionsSchema(BaseSchema):
    cache_path = PathField()
    completed_path = PathField()
    secret_api_key = fields.String()
    system_id = fields.Integer()
    publish_limit = fields.Integer()
    net_flag = fields.Integer()
    cumulative_flag = fields.Integer()

    @post_load
    def make_request(self, data, **kwargs):
        return PvOutputOptions(**data)


@dataclass
class Config:
    connect_options: ConnectOptions = None
    read_options: ReadOptions = None
    pvoutput: PvOutputOptions = None


def move_to_completed(readings: List[Path], cache):
    for reading in readings:
        cache.move_to_processed(reading)


def load_config(config_path: Path) -> Config:
    with open(config_path) as configFile:
        yaml_conf = yaml.safe_load(configFile)
    config = Config()

    config.pvoutput = PvOutputOptionsSchema().load(yaml_conf.get("pvoutput"), partial=True)
    config.connect_options = ConnectOptionsSchema().load(yaml_conf.get("inverter"), partial=True)
    config.read_options = ReadOptionsSchema().load(yaml_conf.get("read_options"), partial=True)
    config.pvoutput.cache_path = config.read_options.output_path
    return config

