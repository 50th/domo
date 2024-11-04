from .base import *

DEBUG = True
LOGGING['handlers']['file']['maxBytes'] = 2 * 1024 * 1024
LOGGING['handlers']['file']['backupCount'] = 1
DEV = True
