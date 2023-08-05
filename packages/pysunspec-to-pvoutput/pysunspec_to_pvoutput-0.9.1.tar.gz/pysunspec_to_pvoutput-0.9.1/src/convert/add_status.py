from dataclasses import dataclass
from pathlib import Path
from typing import List

from datamx.cache.file_process_cache import FileProcessCache
from datamx.utils.groups_util import load_groups
from pvoutput_api.constants import ADD_BATCH_STATUS_SERVICE_NAME, ADD_BATCH_STATUS_URL, ADD_STATUS_SERVICE_NAME, \
    ADD_STATUS_URL
from pvoutput_api.publisher import publish_data
from pvoutput_api.services.common.common import SystemDetails
from pvoutput_api.services.status.add_batch_status_service import AddBatchStatus
from convert.config import PvOutputOptions, move_to_completed
import logging

logger = logging.getLogger(__name__)


def convert_to_batch(readings: List[Path], options: PvOutputOptions, add_status_creator):
    statuses = AddBatchStatus()
    for reading in readings:
        reading_groups = load_groups(reading)
        status = add_status_creator(reading_groups, options)
        statuses.add_status(status)
    return statuses


def publish(add_status_creator, options: PvOutputOptions):
    system_details = SystemDetails(api_key=options.secret_api_key, system_id=str(options.system_id))
    cache = FileProcessCache(options.cache_path, options.completed_path)
    cache.load_cache()
    readings = cache.get_entries()

    if cache.size() > 1:
        readings_batch = readings[:options.publish_limit]
        statuses = convert_to_batch(readings_batch, options, add_status_creator)
        response = publish_data(ADD_BATCH_STATUS_SERVICE_NAME, statuses, system_details, ADD_BATCH_STATUS_URL)
        for status in response.statuses:
            if status.status_added:
                logger.info("Batch reading was added or modified %s %s", status.date, status.time)
        move_to_completed(readings_batch, cache)
    elif cache.size() == 1:
        reading_groups = load_groups(readings[0])
        status = add_status_creator(reading_groups, options)
        publish_data(ADD_STATUS_SERVICE_NAME, status, system_details, ADD_STATUS_URL)
        logger.info("Single reading was published")
        move_to_completed([readings[0]], cache)
    else:
        logger.info("No readings in cache location, all caught up, cache: %s", options.cache_path)