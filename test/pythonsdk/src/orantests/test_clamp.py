import logging
import time
from onapsdk.configuration import settings
from onapsdk.exceptions import SDKException, APIError

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test clamp")

# content of test_sample.py
def inc(x):
    return x + 1

def test_clamp():
    logger.info("Seb test")

    assert inc(3) == 4
