from .base import *

DEBUG = False
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
   'utils.custom_renderer.CustomRenderer',
)
