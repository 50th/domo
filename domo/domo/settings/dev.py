from .base import *

DEBUG = True
LOGGING['handlers']['file']['maxBytes'] = 1024 * 1024
LOGGING['handlers']['file']['backupCount'] = 5
DEV = True
