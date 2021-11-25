import logging
import time
from orantests.configuration import settings
from onapsdk.exceptions import SDKException, APIError

__logger = logging.getLogger(__name__)
# content of test_sample.py
def inc(x):
    return x + 1

def test_clamp():
    assert inc(3) == 5
