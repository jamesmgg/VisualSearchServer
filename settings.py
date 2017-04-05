import sys
USER = "ubuntu"
HOST = "52.90.19.2"
AWS = sys.platform != 'darwin'
private_key =  "~/.ssh/cs5356"
CONFIG_PATH = __file__.split('settings.py')[0]
INDEX_PATH = "tests/index/"
DATA_PATH = "tests/images/"
DEMO = False