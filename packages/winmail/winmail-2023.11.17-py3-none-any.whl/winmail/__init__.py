# -*- coding:utf-8 -*-

from .OpenApi import OpenApi, Base, OpenApi12
from .Winmail import Winmail
from .utils import start_winmail_service, stop_winmail_service

__all__ = ["OpenApi", "OpenApi12", "Base", "Winmail", "start_winmail_service", "stop_winmail_service"]

import os
if os.name == "nt":
    from .ComApi import ComApi
    
    __all__.append("ComApi")
