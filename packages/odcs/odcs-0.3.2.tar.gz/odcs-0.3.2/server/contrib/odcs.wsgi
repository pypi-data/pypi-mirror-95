# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level="DEBUG")

from odcs.server import app as application  # noqa: E402, F401
