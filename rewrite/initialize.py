import logging
import urllib3

from rich.logging import RichHandler

from bristle import Bristle
from scuttle import Scuttle


# We init logging here since this is the first thing that gets initialized on run
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler()
    ]
)
logging.getLogger("urllib3").disabled = True
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.info("Logging Started")

lcu = Bristle()
scuttle = Scuttle()
