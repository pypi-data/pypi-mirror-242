from __future__ import absolute_import, division, print_function

from applitools.common.runner import ClassicEyesRunner

from .__version__ import __version__
from .protocol import Images


class ClassicRunner(ClassicEyesRunner):
    BASE_AGENT_ID = "eyes.images.python", __version__
    Protocol = Images
