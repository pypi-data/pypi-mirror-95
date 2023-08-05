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

# TODO: cron job - run approx daylight hours
#       probably at least every 1-5 mins
# TODO: do we want to have two runs? One with little data and one with a lot of output data - all fields
#       do we want a describe output that will document the ids
# TODO: reduce file size for storage of fields that never change
#       or take out some of the models?
# TODO: Add output - daily figures subtracting start of one day with start of next to give yesterdays data
#       The inverter is lifetime figure
# TODO: simplify publish library?
# TODO: publish to PiPi Prod
#       set version numbers
# TODO: data backup
#       external drive/sd card?
#       Amazon S3/Dynamo?
# TODO: create a web interface?
#       flask/react?
# TODO: consider using last reading of the day as a new reading at the start of the next day
#       this might make for an odd file?
#       as long as we start early enough and late enough, it should be fine
# TODO: get dusk and dawn times - https://astral.readthedocs.io/en/latest/index.html
