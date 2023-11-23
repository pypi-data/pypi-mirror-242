"""
Medias locator
==============

Medias locator returns a path on the file system from the *src* of an img tag.

.. data:: PLACEHOLDER

    A special object that indicates to the renderer to use a placeholder
    instead of a media.
"""

import os.path


PLACEHOLDER = object()


class PathMediasLocator:
    """
    Returns medias relatively to the root directory *base*.
    """
    def __init__(self, base):
        self.base = base

    def __call__(self, path):
        path = path.lstrip('/')
        return os.path.join(self.base, path)


class NoMediasLocator:
    """
    Raises an error when a media is asked.
    """
    def __call__(self, path):
        raise RuntimeError('No media path')


class DebugMediasLocator:
    """
    Return :data:`PLACEHOLDER`
    """

    def __call__(self, path):
        return PLACEHOLDER
