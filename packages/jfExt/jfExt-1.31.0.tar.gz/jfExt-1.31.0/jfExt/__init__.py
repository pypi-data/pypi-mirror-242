# -*- coding: utf-8 -*-
# flake8: noqa : F401
"""
jf-ext.__init__.py
~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018-2022 by the Ji Fu, see AUTHORS for more details.
:license: MIT, see LICENSE for more details.
"""

# pragma mark - BasicType
# --------------------------------------------------------------------------------
from .BasicType.DictExt import *
from .BasicType.FloatExt import *
from .BasicType.JsonExt import *
from .BasicType.ListExt import *
from .BasicType.StringExt import *
from .BasicType.BooleanExt import *

# pragma mark - Time
# --------------------------------------------------------------------------------
from .Time.DateExt import *
from .Time.TimeExt import *

# pragma mark - Mgr
# --------------------------------------------------------------------------------
from .Mgr.mailMgr import MailMgr
from .Mgr.redisMgr import RedisMgr
from .Mgr.responseMgr import APIResponse, APIResponseType

# pragma mark - Math
# --------------------------------------------------------------------------------
from .Math.coordinateExt import *


from .CommonExt import *
from .CurrencyExt import *
from .EncryptExt import *
from .IpExt import *
from .PrintExt import *
from .RequestExt import *
from .SingletonExt import *
from .ValidExt import *
from .fileExt import *
