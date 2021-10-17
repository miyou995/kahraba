from __future__ import absolute_import, unicode_literals
from django import get_version
from .celery_settings import app as celery_app

VERSION = (1, 0, 0, "final", 0)

__version__ = get_version(VERSION)
__all__ = ('celery_app',)