import json
from pathlib import Path
from datetime import datetime

from ._version import __version__

Y = datetime.now().year
HELP_TXT = '''
~~ pdgsubsurface version %s ~~
    Ian Nesbitt / NCEAS %s
''' % (__version__, Y)

MOD_LOC = Path(__file__).parent.absolute()

LOGCONFIG = MOD_LOC.joinpath('log/config.json')
with open(LOGCONFIG, 'r') as lc:
    LOGGING_CONFIG = json.load(lc)
