from .goldenset import *
import logging

# The httpx logs are too verbose
logging.getLogger("httpx").setLevel(logging.CRITICAL)
