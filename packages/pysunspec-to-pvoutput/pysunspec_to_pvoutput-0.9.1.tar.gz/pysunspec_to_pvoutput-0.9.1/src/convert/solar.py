import logging

from pysunspec_read.options import ConnectOptions, ReadOptions
from pysunspec_read.reader import Reader
from requests import HTTPError
from sunspec.core.modbus.client import ModbusClientError

from convert.add_status import publish
from convert.config import PvOutputOptions

logger = logging.getLogger(__name__)


def read(connect_options: ConnectOptions, read_options: ReadOptions = None, retry_times: int = 1):
    try:
        Reader().read(connect_options, read_options)
    except ModbusClientError as e:
        if retry_times > 0:
            remaining_tries = retry_times - 1
            logger.warning("Retry reading from Inverter %s, retry count remaining after this attempt: %s",
                           e, remaining_tries)
            read(connect_options, read_options, remaining_tries)
        else:
            logger.info("No more retries")
            raise


def read_and_publish_add_status(add_status_creator, connect_options: ConnectOptions, read_options: ReadOptions,
                                publish_options: PvOutputOptions):
    try:
        read(connect_options, read_options)
    except ModbusClientError as e:
        logger.error("Error reading from inverter: %s", e)
    # there may be cached files still to upload so even if read failed we still want to progress to publishing
    try:
        publish(add_status_creator, publish_options)
    except HTTPError as e:
        logger.error("Error publishing to pvoutput: %s", e.response.content)
        raise