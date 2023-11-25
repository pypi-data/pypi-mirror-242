# coding: UTF-8
import sys
bstack11l_opy_ = sys.version_info [0] == 2
bstack1ll11l1_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack11lll1l_opy_ (bstack111lll_opy_):
    global bstack11lllll_opy_
    bstack111l1ll_opy_ = ord (bstack111lll_opy_ [-1])
    bstack1ll1ll_opy_ = bstack111lll_opy_ [:-1]
    bstack1l1l_opy_ = bstack111l1ll_opy_ % len (bstack1ll1ll_opy_)
    bstack1ll1l1l_opy_ = bstack1ll1ll_opy_ [:bstack1l1l_opy_] + bstack1ll1ll_opy_ [bstack1l1l_opy_:]
    if bstack11l_opy_:
        bstack1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l1_opy_ - (bstack111l11_opy_ + bstack111l1ll_opy_) % bstack1ll111_opy_) for bstack111l11_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1l11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l1_opy_ - (bstack111l11_opy_ + bstack111l1ll_opy_) % bstack1ll111_opy_) for bstack111l11_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1l11_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
import time
import requests
def bstack11llllll1_opy_():
  global CONFIG
  headers = {
        bstack11lll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡵ"): bstack11lll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡶ"),
      }
  proxies = bstack11lll1111_opy_(CONFIG, bstack111llll1_opy_)
  try:
    response = requests.get(bstack111llll1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1lllll1l_opy_ = response.json()[bstack11lll1l_opy_ (u"ࠫ࡭ࡻࡢࡴࠩࡷ")]
      logger.debug(bstack1111ll1ll_opy_.format(response.json()))
      return bstack1l1lllll1l_opy_
    else:
      logger.debug(bstack11ll111l_opy_.format(bstack11lll1l_opy_ (u"ࠧࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡋࡕࡒࡒࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴࠣࠦࡸ")))
  except Exception as e:
    logger.debug(bstack11ll111l_opy_.format(e))
def bstack1lllll11l_opy_(hub_url):
  global CONFIG
  url = bstack11lll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣࡹ")+  hub_url + bstack11lll1l_opy_ (u"ࠢ࠰ࡥ࡫ࡩࡨࡱࠢࡺ")
  headers = {
        bstack11lll1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧࡻ"): bstack11lll1l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬࡼ"),
      }
  proxies = bstack11lll1111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll111111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11111111l_opy_.format(hub_url, e))
def bstack1l111l111_opy_():
  try:
    global bstack1lll1l1l_opy_
    bstack1l1lllll1l_opy_ = bstack11llllll1_opy_()
    bstack1ll1l11111_opy_ = []
    results = []
    for bstack111l1lll1_opy_ in bstack1l1lllll1l_opy_:
      bstack1ll1l11111_opy_.append(bstack1lll1l111l_opy_(target=bstack1lllll11l_opy_,args=(bstack111l1lll1_opy_,)))
    for t in bstack1ll1l11111_opy_:
      t.start()
    for t in bstack1ll1l11111_opy_:
      results.append(t.join())
    bstack11ll111ll_opy_ = {}
    for item in results:
      hub_url = item[bstack11lll1l_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫࡽ")]
      latency = item[bstack11lll1l_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬࡾ")]
      bstack11ll111ll_opy_[hub_url] = latency
    bstack1l1l1lll_opy_ = min(bstack11ll111ll_opy_, key= lambda x: bstack11ll111ll_opy_[x])
    bstack1lll1l1l_opy_ = bstack1l1l1lll_opy_
    logger.debug(bstack1ll1l1l1_opy_.format(bstack1l1l1lll_opy_))
  except Exception as e:
    logger.debug(bstack11l1l111l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1l11l1_opy_, bstack1lllll11ll_opy_, bstack11lll111_opy_, bstack1l1l11l1_opy_, Notset, bstack1l111l1l_opy_, \
  bstack1l11l1ll_opy_, bstack11l1111l1_opy_, bstack1ll11ll1_opy_, bstack1ll11111_opy_, bstack1ll1111111_opy_, bstack1l1l1llll_opy_, bstack1ll111l1l1_opy_, \
  bstack1lll111lll_opy_, bstack111l11l1l_opy_, bstack11llll11l_opy_, bstack1l1ll11l_opy_, bstack1ll11llll_opy_, bstack1ll11l111l_opy_
from bstack_utils.bstack1ll1l1l11_opy_ import bstack111lll111_opy_
from bstack_utils.proxy import bstack1ll11l1l1_opy_, bstack11lll1111_opy_, bstack11lllll1l_opy_, bstack1llllll1ll_opy_
import bstack_utils.bstack1111llll1_opy_ as bstack1111l11ll_opy_
from browserstack_sdk.bstack1ll1l11ll_opy_ import *
from browserstack_sdk.bstack1llll1111_opy_ import *
from bstack_utils.bstack11lll11ll_opy_ import bstack11l11l111_opy_
bstack11l111ll_opy_ = bstack11lll1l_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬࡿ")
bstack1111llll_opy_ = bstack11lll1l_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࢀ")
from ._version import __version__
bstack1l1lllllll_opy_ = None
CONFIG = {}
bstack1llll1lll1_opy_ = {}
bstack1111111ll_opy_ = {}
bstack11ll1ll1_opy_ = None
bstack111ll1ll_opy_ = None
bstack11l1ll11l_opy_ = None
bstack1l11ll1ll_opy_ = -1
bstack1l1l1l111_opy_ = 0
bstack1ll11lll11_opy_ = bstack1l1l1l1l_opy_
bstack1l11111l_opy_ = 1
bstack1l11llll1_opy_ = False
bstack1l1111l11_opy_ = False
bstack11l11ll1_opy_ = bstack11lll1l_opy_ (u"ࠧࠨࢁ")
bstack1l1ll11ll_opy_ = bstack11lll1l_opy_ (u"ࠨࠩࢂ")
bstack1l1lllll_opy_ = False
bstack1l11ll1l_opy_ = True
bstack1l1ll1l1l_opy_ = bstack11lll1l_opy_ (u"ࠩࠪࢃ")
bstack1lll111ll_opy_ = []
bstack1lll1l1l_opy_ = bstack11lll1l_opy_ (u"ࠪࠫࢄ")
bstack1ll111l11_opy_ = False
bstack1l1l1l1ll_opy_ = None
bstack1l1l11lll_opy_ = None
bstack1lllllll11_opy_ = -1
bstack1l1lll1ll_opy_ = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠫࢃ࠭ࢅ")), bstack11lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࢆ"), bstack11lll1l_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫࢇ"))
bstack1llllll11l_opy_ = 0
bstack1ll1l11lll_opy_ = []
bstack1llll1llll_opy_ = []
bstack1ll11l1l11_opy_ = []
bstack1ll111lll1_opy_ = []
bstack1ll1ll1lll_opy_ = bstack11lll1l_opy_ (u"ࠧࠨ࢈")
bstack1ll1ll11ll_opy_ = bstack11lll1l_opy_ (u"ࠨࠩࢉ")
bstack1l11l111l_opy_ = False
bstack11lll1l1l_opy_ = False
bstack111l111l1_opy_ = {}
bstack11ll11ll_opy_ = None
bstack1111l111_opy_ = None
bstack1lll1lll_opy_ = None
bstack1l1l1ll1l_opy_ = None
bstack11ll1l111_opy_ = None
bstack1llll1ll1l_opy_ = None
bstack1ll1lll11l_opy_ = None
bstack11ll1111l_opy_ = None
bstack1llll1l11_opy_ = None
bstack1ll1l11l1l_opy_ = None
bstack11ll1l11_opy_ = None
bstack1l1l1111_opy_ = None
bstack111ll1l11_opy_ = None
bstack1l1llll111_opy_ = None
bstack1lllll111l_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack11l1ll1l_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack1ll1lll11_opy_ = bstack11lll1l_opy_ (u"ࠤࠥࢊ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll11lll11_opy_,
                    format=bstack11lll1l_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨࢋ"),
                    datefmt=bstack11lll1l_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ࢌ"),
                    stream=sys.stdout)
bstack1lll1l1111_opy_ = Config.get_instance()
percy = bstack1l111ll11_opy_()
def bstack11lll1l11_opy_():
  global CONFIG
  global bstack1ll11lll11_opy_
  if bstack11lll1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࢍ") in CONFIG:
    bstack1ll11lll11_opy_ = bstack1ll1111l_opy_[CONFIG[bstack11lll1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ")]]
    logging.getLogger().setLevel(bstack1ll11lll11_opy_)
def bstack1llllllll1_opy_():
  global CONFIG
  global bstack1l11l111l_opy_
  bstack1llll1l1l1_opy_ = bstack1lll1l11ll_opy_(CONFIG)
  if (bstack11lll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ࢏") in bstack1llll1l1l1_opy_ and str(bstack1llll1l1l1_opy_[bstack11lll1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐")]).lower() == bstack11lll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ࢑")):
    bstack1l11l111l_opy_ = True
def bstack1l111l11l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1ll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11l11l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11lll1l_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡧࡴࡴࡦࡪࡩࡩ࡭ࡱ࡫ࠢ࢒") == args[i].lower() or bstack11lll1l_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡨ࡬࡫ࠧ࢓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1ll1l1l_opy_
      bstack1l1ll1l1l_opy_ += bstack11lll1l_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࡋ࡯࡬ࡦࠢࠪ࢔") + path
      return path
  return None
bstack111l11l1_opy_ = re.compile(bstack11lll1l_opy_ (u"ࡸࠢ࠯ࠬࡂࡠࠩࢁࠨ࠯ࠬࡂ࠭ࢂ࠴ࠪࡀࠤ࢕"))
def bstack11l111lll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111l11l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11lll1l_opy_ (u"ࠢࠥࡽࠥ࢖") + group + bstack11lll1l_opy_ (u"ࠣࡿࠥࢗ"), os.environ.get(group))
  return value
def bstack111l1ll1_opy_():
  bstack1lll1ll1l1_opy_ = bstack1l11l11l1_opy_()
  if bstack1lll1ll1l1_opy_ and os.path.exists(os.path.abspath(bstack1lll1ll1l1_opy_)):
    fileName = bstack1lll1ll1l1_opy_
  if bstack11lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭࢘") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")])) and not bstack11lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    fileName = os.environ[bstack11lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")]
  if bstack11lll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    bstack111l_opy_ = os.path.abspath(fileName)
  else:
    bstack111l_opy_ = bstack11lll1l_opy_ (u"ࠧࠨ࢝")
  bstack1l11lll11_opy_ = os.getcwd()
  bstack1ll11ll111_opy_ = bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ࢞")
  bstack1ll1111l1_opy_ = bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭࢟")
  while (not os.path.exists(bstack111l_opy_)) and bstack1l11lll11_opy_ != bstack11lll1l_opy_ (u"ࠥࠦࢠ"):
    bstack111l_opy_ = os.path.join(bstack1l11lll11_opy_, bstack1ll11ll111_opy_)
    if not os.path.exists(bstack111l_opy_):
      bstack111l_opy_ = os.path.join(bstack1l11lll11_opy_, bstack1ll1111l1_opy_)
    if bstack1l11lll11_opy_ != os.path.dirname(bstack1l11lll11_opy_):
      bstack1l11lll11_opy_ = os.path.dirname(bstack1l11lll11_opy_)
    else:
      bstack1l11lll11_opy_ = bstack11lll1l_opy_ (u"ࠦࠧࢡ")
  if not os.path.exists(bstack111l_opy_):
    bstack1llll11l1_opy_(
      bstack11lll1l1_opy_.format(os.getcwd()))
  try:
    with open(bstack111l_opy_, bstack11lll1l_opy_ (u"ࠬࡸࠧࢢ")) as stream:
      yaml.add_implicit_resolver(bstack11lll1l_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࢣ"), bstack111l11l1_opy_)
      yaml.add_constructor(bstack11lll1l_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣࢤ"), bstack11l111lll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack111l_opy_, bstack11lll1l_opy_ (u"ࠨࡴࠪࢥ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1llll11l1_opy_(bstack1l1l1l1l1_opy_.format(str(exc)))
def bstack11ll1ll1l_opy_(config):
  bstack1111l111l_opy_ = bstack1lll1l1ll_opy_(config)
  for option in list(bstack1111l111l_opy_):
    if option.lower() in bstack1l1l1ll1_opy_ and option != bstack1l1l1ll1_opy_[option.lower()]:
      bstack1111l111l_opy_[bstack1l1l1ll1_opy_[option.lower()]] = bstack1111l111l_opy_[option]
      del bstack1111l111l_opy_[option]
  return config
def bstack1ll1ll1l1l_opy_():
  global bstack1111111ll_opy_
  for key, bstack1lll11ll1_opy_ in bstack1l1lll11l_opy_.items():
    if isinstance(bstack1lll11ll1_opy_, list):
      for var in bstack1lll11ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1111111ll_opy_[key] = os.environ[var]
          break
    elif bstack1lll11ll1_opy_ in os.environ and os.environ[bstack1lll11ll1_opy_] and str(os.environ[bstack1lll11ll1_opy_]).strip():
      bstack1111111ll_opy_[key] = os.environ[bstack1lll11ll1_opy_]
  if bstack11lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫࢦ") in os.environ:
    bstack1111111ll_opy_[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢧ")] = {}
    bstack1111111ll_opy_[bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢨ")][bstack11lll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢩ")] = os.environ[bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࢪ")]
def bstack11l111l1_opy_():
  global bstack1llll1lll1_opy_
  global bstack1l1ll1l1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11lll1l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢫ").lower() == val.lower():
      bstack1llll1lll1_opy_[bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢬ")] = {}
      bstack1llll1lll1_opy_[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢭ")][bstack11lll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢮ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lll11ll11_opy_ in bstack111111l11_opy_.items():
    if isinstance(bstack1lll11ll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lll11ll11_opy_:
          if idx < len(sys.argv) and bstack11lll1l_opy_ (u"ࠫ࠲࠳ࠧࢯ") + var.lower() == val.lower() and not key in bstack1llll1lll1_opy_:
            bstack1llll1lll1_opy_[key] = sys.argv[idx + 1]
            bstack1l1ll1l1l_opy_ += bstack11lll1l_opy_ (u"ࠬࠦ࠭࠮ࠩࢰ") + var + bstack11lll1l_opy_ (u"࠭ࠠࠨࢱ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11lll1l_opy_ (u"ࠧ࠮࠯ࠪࢲ") + bstack1lll11ll11_opy_.lower() == val.lower() and not key in bstack1llll1lll1_opy_:
          bstack1llll1lll1_opy_[key] = sys.argv[idx + 1]
          bstack1l1ll1l1l_opy_ += bstack11lll1l_opy_ (u"ࠨࠢ࠰࠱ࠬࢳ") + bstack1lll11ll11_opy_ + bstack11lll1l_opy_ (u"ࠩࠣࠫࢴ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1llll1111l_opy_(config):
  bstack11l1lll1l_opy_ = config.keys()
  for bstack1l1l1ll11_opy_, bstack1lll11l1ll_opy_ in bstack1l1ll1ll1_opy_.items():
    if bstack1lll11l1ll_opy_ in bstack11l1lll1l_opy_:
      config[bstack1l1l1ll11_opy_] = config[bstack1lll11l1ll_opy_]
      del config[bstack1lll11l1ll_opy_]
  for bstack1l1l1ll11_opy_, bstack1lll11l1ll_opy_ in bstack1llll11l_opy_.items():
    if isinstance(bstack1lll11l1ll_opy_, list):
      for bstack1ll111l1l_opy_ in bstack1lll11l1ll_opy_:
        if bstack1ll111l1l_opy_ in bstack11l1lll1l_opy_:
          config[bstack1l1l1ll11_opy_] = config[bstack1ll111l1l_opy_]
          del config[bstack1ll111l1l_opy_]
          break
    elif bstack1lll11l1ll_opy_ in bstack11l1lll1l_opy_:
      config[bstack1l1l1ll11_opy_] = config[bstack1lll11l1ll_opy_]
      del config[bstack1lll11l1ll_opy_]
  for bstack1ll111l1l_opy_ in list(config):
    for bstack1lllll1l1l_opy_ in bstack111l111ll_opy_:
      if bstack1ll111l1l_opy_.lower() == bstack1lllll1l1l_opy_.lower() and bstack1ll111l1l_opy_ != bstack1lllll1l1l_opy_:
        config[bstack1lllll1l1l_opy_] = config[bstack1ll111l1l_opy_]
        del config[bstack1ll111l1l_opy_]
  bstack1llll1l1_opy_ = []
  if bstack11lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ") in config:
    bstack1llll1l1_opy_ = config[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࢶ")]
  for platform in bstack1llll1l1_opy_:
    for bstack1ll111l1l_opy_ in list(platform):
      for bstack1lllll1l1l_opy_ in bstack111l111ll_opy_:
        if bstack1ll111l1l_opy_.lower() == bstack1lllll1l1l_opy_.lower() and bstack1ll111l1l_opy_ != bstack1lllll1l1l_opy_:
          platform[bstack1lllll1l1l_opy_] = platform[bstack1ll111l1l_opy_]
          del platform[bstack1ll111l1l_opy_]
  for bstack1l1l1ll11_opy_, bstack1lll11l1ll_opy_ in bstack1llll11l_opy_.items():
    for platform in bstack1llll1l1_opy_:
      if isinstance(bstack1lll11l1ll_opy_, list):
        for bstack1ll111l1l_opy_ in bstack1lll11l1ll_opy_:
          if bstack1ll111l1l_opy_ in platform:
            platform[bstack1l1l1ll11_opy_] = platform[bstack1ll111l1l_opy_]
            del platform[bstack1ll111l1l_opy_]
            break
      elif bstack1lll11l1ll_opy_ in platform:
        platform[bstack1l1l1ll11_opy_] = platform[bstack1lll11l1ll_opy_]
        del platform[bstack1lll11l1ll_opy_]
  for bstack111111l1_opy_ in bstack1ll1ll1l_opy_:
    if bstack111111l1_opy_ in config:
      if not bstack1ll1ll1l_opy_[bstack111111l1_opy_] in config:
        config[bstack1ll1ll1l_opy_[bstack111111l1_opy_]] = {}
      config[bstack1ll1ll1l_opy_[bstack111111l1_opy_]].update(config[bstack111111l1_opy_])
      del config[bstack111111l1_opy_]
  for platform in bstack1llll1l1_opy_:
    for bstack111111l1_opy_ in bstack1ll1ll1l_opy_:
      if bstack111111l1_opy_ in list(platform):
        if not bstack1ll1ll1l_opy_[bstack111111l1_opy_] in platform:
          platform[bstack1ll1ll1l_opy_[bstack111111l1_opy_]] = {}
        platform[bstack1ll1ll1l_opy_[bstack111111l1_opy_]].update(platform[bstack111111l1_opy_])
        del platform[bstack111111l1_opy_]
  config = bstack11ll1ll1l_opy_(config)
  return config
def bstack1lll1l111_opy_(config):
  global bstack1l1ll11ll_opy_
  if bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ") in config and str(config[bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࢸ")]).lower() != bstack11lll1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࢹ"):
    if not bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ") in config:
      config[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")] = {}
    if not bstack11lll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢼ") in config[bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")]:
      bstack11l1l1111_opy_ = datetime.datetime.now()
      bstack1lll1111ll_opy_ = bstack11l1l1111_opy_.strftime(bstack11lll1l_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩࢾ"))
      hostname = socket.gethostname()
      bstack1lll1ll1_opy_ = bstack11lll1l_opy_ (u"࠭ࠧࢿ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11lll1l_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩࣀ").format(bstack1lll1111ll_opy_, hostname, bstack1lll1ll1_opy_)
      config[bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack11lll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")] = identifier
    bstack1l1ll11ll_opy_ = config[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack11lll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")]
  return config
def bstack1l11lll1_opy_():
  bstack1l11llll_opy_ =  bstack1ll11111_opy_()[bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠫࣅ")]
  return bstack1l11llll_opy_ if bstack1l11llll_opy_ else -1
def bstack1ll11111l1_opy_(bstack1l11llll_opy_):
  global CONFIG
  if not bstack11lll1l_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨࣆ") in CONFIG[bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")]:
    return
  CONFIG[bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")] = CONFIG[bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")].replace(
    bstack11lll1l_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ࣊"),
    str(bstack1l11llll_opy_)
  )
def bstack111ll1lll_opy_():
  global CONFIG
  if not bstack11lll1l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ࣋") in CONFIG[bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")]:
    return
  bstack11l1l1111_opy_ = datetime.datetime.now()
  bstack1lll1111ll_opy_ = bstack11l1l1111_opy_.strftime(bstack11lll1l_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫ࣍"))
  CONFIG[bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")] = CONFIG[bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")].replace(
    bstack11lll1l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ࣐"),
    bstack1lll1111ll_opy_
  )
def bstack1lll111l_opy_():
  global CONFIG
  if bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ") in CONFIG and not bool(CONFIG[bstack11lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭")]):
    del CONFIG[bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]
    return
  if not bstack11lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ") in CONFIG:
    CONFIG[bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")] = bstack11lll1l_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫࣖ")
  if bstack11lll1l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣗ") in CONFIG[bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]:
    bstack111ll1lll_opy_()
    os.environ[bstack11lll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨࣙ")] = CONFIG[bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]
  if not bstack11lll1l_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨࣛ") in CONFIG[bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]:
    return
  bstack1l11llll_opy_ = bstack11lll1l_opy_ (u"ࠨࠩࣝ")
  bstack1ll1ll1ll1_opy_ = bstack1l11lll1_opy_()
  if bstack1ll1ll1ll1_opy_ != -1:
    bstack1l11llll_opy_ = bstack11lll1l_opy_ (u"ࠩࡆࡍࠥ࠭ࣞ") + str(bstack1ll1ll1ll1_opy_)
  if bstack1l11llll_opy_ == bstack11lll1l_opy_ (u"ࠪࠫࣟ"):
    bstack1ll1ll11l1_opy_ = bstack1ll11l1ll_opy_(CONFIG[bstack11lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ࣠")])
    if bstack1ll1ll11l1_opy_ != -1:
      bstack1l11llll_opy_ = str(bstack1ll1ll11l1_opy_)
  if bstack1l11llll_opy_:
    bstack1ll11111l1_opy_(bstack1l11llll_opy_)
    os.environ[bstack11lll1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ࣡")] = CONFIG[bstack11lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣢")]
def bstack1ll1lll1_opy_(bstack1llllll11_opy_, bstack1ll1l11l1_opy_, path):
  bstack11111lll_opy_ = {
    bstack11lll1l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࣣࠫ"): bstack1ll1l11l1_opy_
  }
  if os.path.exists(path):
    bstack11l1l1l11_opy_ = json.load(open(path, bstack11lll1l_opy_ (u"ࠨࡴࡥࠫࣤ")))
  else:
    bstack11l1l1l11_opy_ = {}
  bstack11l1l1l11_opy_[bstack1llllll11_opy_] = bstack11111lll_opy_
  with open(path, bstack11lll1l_opy_ (u"ࠤࡺ࠯ࠧࣥ")) as outfile:
    json.dump(bstack11l1l1l11_opy_, outfile)
def bstack1ll11l1ll_opy_(bstack1llllll11_opy_):
  bstack1llllll11_opy_ = str(bstack1llllll11_opy_)
  bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠪࢂࣦࠬ")), bstack11lll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"))
  try:
    if not os.path.exists(bstack111ll1111_opy_):
      os.makedirs(bstack111ll1111_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠬࢄࠧࣨ")), bstack11lll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"), bstack11lll1l_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩ࣪"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11lll1l_opy_ (u"ࠨࡹࠪ࣫")):
        pass
      with open(file_path, bstack11lll1l_opy_ (u"ࠤࡺ࠯ࠧ࣬")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11lll1l_opy_ (u"ࠪࡶ࣭ࠬ")) as bstack1lll1lll11_opy_:
      bstack1ll1l11l11_opy_ = json.load(bstack1lll1lll11_opy_)
    if bstack1llllll11_opy_ in bstack1ll1l11l11_opy_:
      bstack1ll1l11l_opy_ = bstack1ll1l11l11_opy_[bstack1llllll11_opy_][bstack11lll1l_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣮")]
      bstack1ll1llll1l_opy_ = int(bstack1ll1l11l_opy_) + 1
      bstack1ll1lll1_opy_(bstack1llllll11_opy_, bstack1ll1llll1l_opy_, file_path)
      return bstack1ll1llll1l_opy_
    else:
      bstack1ll1lll1_opy_(bstack1llllll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1l111l1_opy_.format(str(e)))
    return -1
def bstack11lllll1_opy_(config):
  if not config[bstack11lll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫࣯ࠧ")] or not config[bstack11lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࣰࠩ")]:
    return True
  else:
    return False
def bstack111111lll_opy_(config, index=0):
  global bstack1l1lllll_opy_
  bstack111111ll1_opy_ = {}
  caps = bstack1l1llll1_opy_ + bstack1l11l1111_opy_
  if bstack1l1lllll_opy_:
    caps += bstack1l1ll111l_opy_
  for key in config:
    if key in caps + [bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]:
      continue
    bstack111111ll1_opy_[key] = config[key]
  if bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ") in config:
    for bstack1111l1l11_opy_ in config[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")][index]:
      if bstack1111l1l11_opy_ in caps + [bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣴ"), bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࣵ")]:
        continue
      bstack111111ll1_opy_[bstack1111l1l11_opy_] = config[bstack11lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣶ")][index][bstack1111l1l11_opy_]
  bstack111111ll1_opy_[bstack11lll1l_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨࣷ")] = socket.gethostname()
  if bstack11lll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ") in bstack111111ll1_opy_:
    del (bstack111111ll1_opy_[bstack11lll1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࣹࠩ")])
  return bstack111111ll1_opy_
def bstack11l1llll_opy_(config):
  global bstack1l1lllll_opy_
  bstack111l1lll_opy_ = {}
  caps = bstack1l11l1111_opy_
  if bstack1l1lllll_opy_:
    caps += bstack1l1ll111l_opy_
  for key in caps:
    if key in config:
      bstack111l1lll_opy_[key] = config[key]
  return bstack111l1lll_opy_
def bstack11111llll_opy_(bstack111111ll1_opy_, bstack111l1lll_opy_):
  bstack1ll1l1ll1l_opy_ = {}
  for key in bstack111111ll1_opy_.keys():
    if key in bstack1l1ll1ll1_opy_:
      bstack1ll1l1ll1l_opy_[bstack1l1ll1ll1_opy_[key]] = bstack111111ll1_opy_[key]
    else:
      bstack1ll1l1ll1l_opy_[key] = bstack111111ll1_opy_[key]
  for key in bstack111l1lll_opy_:
    if key in bstack1l1ll1ll1_opy_:
      bstack1ll1l1ll1l_opy_[bstack1l1ll1ll1_opy_[key]] = bstack111l1lll_opy_[key]
    else:
      bstack1ll1l1ll1l_opy_[key] = bstack111l1lll_opy_[key]
  return bstack1ll1l1ll1l_opy_
def bstack111l1l11_opy_(config, index=0):
  global bstack1l1lllll_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack111l1lll_opy_ = bstack11l1llll_opy_(config)
  bstack11ll111l1_opy_ = bstack1l11l1111_opy_
  bstack11ll111l1_opy_ += bstack1lll11l1l1_opy_
  if bstack1l1lllll_opy_:
    bstack11ll111l1_opy_ += bstack1l1ll111l_opy_
  if bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ") in config:
    if bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ") in config[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index]:
      caps[bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")] = config[bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index][bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")]
    if bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ") in config[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index]:
      caps[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")] = str(config[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index][bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")])
    bstack1ll111l11l_opy_ = {}
    for bstack1ll11l1111_opy_ in bstack11ll111l1_opy_:
      if bstack1ll11l1111_opy_ in config[bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1ll11l1111_opy_ == bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack1ll111l11l_opy_[bstack1ll11l1111_opy_] = str(config[bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1ll11l1111_opy_] * 1.0)
          except:
            bstack1ll111l11l_opy_[bstack1ll11l1111_opy_] = str(config[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1ll11l1111_opy_])
        else:
          bstack1ll111l11l_opy_[bstack1ll11l1111_opy_] = config[bstack11lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1ll11l1111_opy_]
        del (config[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1ll11l1111_opy_])
    bstack111l1lll_opy_ = update(bstack111l1lll_opy_, bstack1ll111l11l_opy_)
  bstack111111ll1_opy_ = bstack111111lll_opy_(config, index)
  for bstack1ll111l1l_opy_ in bstack1l11l1111_opy_ + [bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऋ"), bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧऌ")]:
    if bstack1ll111l1l_opy_ in bstack111111ll1_opy_:
      bstack111l1lll_opy_[bstack1ll111l1l_opy_] = bstack111111ll1_opy_[bstack1ll111l1l_opy_]
      del (bstack111111ll1_opy_[bstack1ll111l1l_opy_])
  if bstack1l111l1l_opy_(config):
    bstack111111ll1_opy_[bstack11lll1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = True
    caps.update(bstack111l1lll_opy_)
    caps[bstack11lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩऎ")] = bstack111111ll1_opy_
  else:
    bstack111111ll1_opy_[bstack11lll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = False
    caps.update(bstack11111llll_opy_(bstack111111ll1_opy_, bstack111l1lll_opy_))
    if bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ") in caps:
      caps[bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬऑ")] = caps[bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ")]
      del (caps[bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫओ")])
    if bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ") in caps:
      caps[bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪक")] = caps[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख")]
      del (caps[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫग")])
  return caps
def bstack111l11111_opy_():
  global bstack1lll1l1l_opy_
  if bstack1ll1ll11_opy_() <= version.parse(bstack11lll1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫघ")):
    if bstack1lll1l1l_opy_ != bstack11lll1l_opy_ (u"ࠬ࠭ङ"):
      return bstack11lll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢच") + bstack1lll1l1l_opy_ + bstack11lll1l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦछ")
    return bstack11l11111l_opy_
  if bstack1lll1l1l_opy_ != bstack11lll1l_opy_ (u"ࠨࠩज"):
    return bstack11lll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦझ") + bstack1lll1l1l_opy_ + bstack11lll1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦञ")
  return bstack1lllll11_opy_
def bstack1l11l11ll_opy_(options):
  return hasattr(options, bstack11lll1l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬट"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1llll11ll_opy_(options, bstack1ll1l1lll_opy_):
  for bstack1ll11llll1_opy_ in bstack1ll1l1lll_opy_:
    if bstack1ll11llll1_opy_ in [bstack11lll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪठ"), bstack11lll1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪड")]:
      continue
    if bstack1ll11llll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll11llll1_opy_] = update(options._experimental_options[bstack1ll11llll1_opy_],
                                                         bstack1ll1l1lll_opy_[bstack1ll11llll1_opy_])
    else:
      options.add_experimental_option(bstack1ll11llll1_opy_, bstack1ll1l1lll_opy_[bstack1ll11llll1_opy_])
  if bstack11lll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ") in bstack1ll1l1lll_opy_:
    for arg in bstack1ll1l1lll_opy_[bstack11lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ण")]:
      options.add_argument(arg)
    del (bstack1ll1l1lll_opy_[bstack11lll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत")])
  if bstack11lll1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ") in bstack1ll1l1lll_opy_:
    for ext in bstack1ll1l1lll_opy_[bstack11lll1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨद")]:
      options.add_extension(ext)
    del (bstack1ll1l1lll_opy_[bstack11lll1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध")])
def bstack1ll11l1ll1_opy_(options, bstack1lllll1l11_opy_):
  if bstack11lll1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन") in bstack1lllll1l11_opy_:
    for bstack11l1lllll_opy_ in bstack1lllll1l11_opy_[bstack11lll1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")]:
      if bstack11l1lllll_opy_ in options._preferences:
        options._preferences[bstack11l1lllll_opy_] = update(options._preferences[bstack11l1lllll_opy_], bstack1lllll1l11_opy_[bstack11lll1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप")][bstack11l1lllll_opy_])
      else:
        options.set_preference(bstack11l1lllll_opy_, bstack1lllll1l11_opy_[bstack11lll1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")][bstack11l1lllll_opy_])
  if bstack11lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨब") in bstack1lllll1l11_opy_:
    for arg in bstack1lllll1l11_opy_[bstack11lll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩभ")]:
      options.add_argument(arg)
def bstack11ll11lll_opy_(options, bstack1lll1l1ll1_opy_):
  if bstack11lll1l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭म") in bstack1lll1l1ll1_opy_:
    options.use_webview(bool(bstack1lll1l1ll1_opy_[bstack11lll1l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧय")]))
  bstack1llll11ll_opy_(options, bstack1lll1l1ll1_opy_)
def bstack1lll1ll111_opy_(options, bstack1lll1111l_opy_):
  for bstack1lllll1lll_opy_ in bstack1lll1111l_opy_:
    if bstack1lllll1lll_opy_ in [bstack11lll1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫर"), bstack11lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      continue
    options.set_capability(bstack1lllll1lll_opy_, bstack1lll1111l_opy_[bstack1lllll1lll_opy_])
  if bstack11lll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧल") in bstack1lll1111l_opy_:
    for arg in bstack1lll1111l_opy_[bstack11lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      options.add_argument(arg)
  if bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨऴ") in bstack1lll1111l_opy_:
    options.bstack1ll1llllll_opy_(bool(bstack1lll1111l_opy_[bstack11lll1l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩव")]))
def bstack1l11l111_opy_(options, bstack1l11ll1l1_opy_):
  for bstack1ll1l1111l_opy_ in bstack1l11ll1l1_opy_:
    if bstack1ll1l1111l_opy_ in [bstack11lll1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश"), bstack11lll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬष")]:
      continue
    options._options[bstack1ll1l1111l_opy_] = bstack1l11ll1l1_opy_[bstack1ll1l1111l_opy_]
  if bstack11lll1l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस") in bstack1l11ll1l1_opy_:
    for bstack1l111lll1_opy_ in bstack1l11ll1l1_opy_[bstack11lll1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ह")]:
      options.bstack11111l1ll_opy_(
        bstack1l111lll1_opy_, bstack1l11ll1l1_opy_[bstack11lll1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ")][bstack1l111lll1_opy_])
  if bstack11lll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩऻ") in bstack1l11ll1l1_opy_:
    for arg in bstack1l11ll1l1_opy_[bstack11lll1l_opy_ (u"ࠬࡧࡲࡨࡵ़ࠪ")]:
      options.add_argument(arg)
def bstack1ll1ll1ll_opy_(options, caps):
  if not hasattr(options, bstack11lll1l_opy_ (u"࠭ࡋࡆ࡛ࠪऽ")):
    return
  if options.KEY == bstack11lll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1llll11ll_opy_(options, caps[bstack11lll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack11lll1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1ll11l1ll1_opy_(options, caps[bstack11lll1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack11lll1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1lll1ll111_opy_(options, caps[bstack11lll1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack11lll1l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack11ll11lll_opy_(options, caps[bstack11lll1l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack11lll1l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॆ") and options.KEY in caps:
    bstack1l11l111_opy_(options, caps[bstack11lll1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨे")])
def bstack1l11l1lll_opy_(caps):
  global bstack1l1lllll_opy_
  if isinstance(os.environ.get(bstack11lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫै")), str):
    bstack1l1lllll_opy_ = eval(os.getenv(bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬॉ")))
  if bstack1l1lllll_opy_:
    if bstack1l111l11l_opy_() < version.parse(bstack11lll1l_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫॊ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11lll1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ो")
    if bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ") in caps:
      browser = caps[bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    elif bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॎ") in caps:
      browser = caps[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫॏ")]
    browser = str(browser).lower()
    if browser == bstack11lll1l_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫॐ") or browser == bstack11lll1l_opy_ (u"ࠬ࡯ࡰࡢࡦࠪ॑"):
      browser = bstack11lll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮॒࠭")
    if browser == bstack11lll1l_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨ॓"):
      browser = bstack11lll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ॔")
    if browser not in [bstack11lll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩॕ"), bstack11lll1l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨॖ"), bstack11lll1l_opy_ (u"ࠫ࡮࡫ࠧॗ"), bstack11lll1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬक़"), bstack11lll1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧख़")]:
      return None
    try:
      package = bstack11lll1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩग़").format(browser)
      name = bstack11lll1l_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩज़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11l11ll_opy_(options):
        return None
      for bstack1ll111l1l_opy_ in caps.keys():
        options.set_capability(bstack1ll111l1l_opy_, caps[bstack1ll111l1l_opy_])
      bstack1ll1ll1ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11111lll1_opy_(options, bstack1111lllll_opy_):
  if not bstack1l11l11ll_opy_(options):
    return
  for bstack1ll111l1l_opy_ in bstack1111lllll_opy_.keys():
    if bstack1ll111l1l_opy_ in bstack1lll11l1l1_opy_:
      continue
    if bstack1ll111l1l_opy_ in options._caps and type(options._caps[bstack1ll111l1l_opy_]) in [dict, list]:
      options._caps[bstack1ll111l1l_opy_] = update(options._caps[bstack1ll111l1l_opy_], bstack1111lllll_opy_[bstack1ll111l1l_opy_])
    else:
      options.set_capability(bstack1ll111l1l_opy_, bstack1111lllll_opy_[bstack1ll111l1l_opy_])
  bstack1ll1ll1ll_opy_(options, bstack1111lllll_opy_)
  if bstack11lll1l_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨड़") in options._caps:
    if options._caps[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")] and options._caps[bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़")].lower() != bstack11lll1l_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭य़"):
      del options._caps[bstack11lll1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬॠ")]
def bstack1l111l1ll_opy_(proxy_config):
  if bstack11lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ") in proxy_config:
    proxy_config[bstack11lll1l_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪॢ")] = proxy_config[bstack11lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ")]
    del (proxy_config[bstack11lll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ।")])
  if bstack11lll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ॥") in proxy_config and proxy_config[bstack11lll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")].lower() != bstack11lll1l_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭१"):
    proxy_config[bstack11lll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")] = bstack11lll1l_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨ३")
  if bstack11lll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧ४") in proxy_config:
    proxy_config[bstack11lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭५")] = bstack11lll1l_opy_ (u"ࠫࡵࡧࡣࠨ६")
  return proxy_config
def bstack1ll111ll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11lll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७") in config:
    return proxy
  config[bstack11lll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")] = bstack1l111l1ll_opy_(config[bstack11lll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९")])
  if proxy == None:
    proxy = Proxy(config[bstack11lll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")])
  return proxy
def bstack1l11l1l1l_opy_(self):
  global CONFIG
  global bstack11ll1l11_opy_
  try:
    proxy = bstack11lllll1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11lll1l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॱ")):
        proxies = bstack1ll11l1l1_opy_(proxy, bstack111l11111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1llllll_opy_ = proxies.popitem()
          if bstack11lll1l_opy_ (u"ࠥ࠾࠴࠵ࠢॲ") in bstack1l1llllll_opy_:
            return bstack1l1llllll_opy_
          else:
            return bstack11lll1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧॳ") + bstack1l1llllll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11lll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤॴ").format(str(e)))
  return bstack11ll1l11_opy_(self)
def bstack1lll1ll11_opy_():
  global CONFIG
  return bstack1llllll1ll_opy_(CONFIG) and bstack1l1l1llll_opy_() and bstack1ll1ll11_opy_() >= version.parse(bstack1l1lll1l_opy_)
def bstack1lll1l11_opy_():
  global CONFIG
  return (bstack11lll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩॵ") in CONFIG or bstack11lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॶ") in CONFIG) and bstack1ll111l1l1_opy_()
def bstack1lll1l1ll_opy_(config):
  bstack1111l111l_opy_ = {}
  if bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॷ") in config:
    bstack1111l111l_opy_ = config[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॸ")]
  if bstack11lll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॹ") in config:
    bstack1111l111l_opy_ = config[bstack11lll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॺ")]
  proxy = bstack11lllll1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack11lll1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")) and os.path.isfile(proxy):
      bstack1111l111l_opy_[bstack11lll1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩॼ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11lll1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")):
        proxies = bstack11lll1111_opy_(config, bstack111l11111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1llllll_opy_ = proxies.popitem()
          if bstack11lll1l_opy_ (u"ࠣ࠼࠲࠳ࠧॾ") in bstack1l1llllll_opy_:
            parsed_url = urlparse(bstack1l1llllll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11lll1l_opy_ (u"ࠤ࠽࠳࠴ࠨॿ") + bstack1l1llllll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1111l111l_opy_[bstack11lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ঀ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1111l111l_opy_[bstack11lll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧঁ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1111l111l_opy_[bstack11lll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨং")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1111l111l_opy_[bstack11lll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩঃ")] = str(parsed_url.password)
  return bstack1111l111l_opy_
def bstack1lll1l11ll_opy_(config):
  if bstack11lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ঄") in config:
    return config[bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭অ")]
  return {}
def bstack111ll1l1_opy_(caps):
  global bstack1l1ll11ll_opy_
  if bstack11lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪআ") in caps:
    caps[bstack11lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack11lll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪঈ")] = True
    if bstack1l1ll11ll_opy_:
      caps[bstack11lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack11lll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨঊ")] = bstack1l1ll11ll_opy_
  else:
    caps[bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬঋ")] = True
    if bstack1l1ll11ll_opy_:
      caps[bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩঌ")] = bstack1l1ll11ll_opy_
def bstack11lll111l_opy_():
  global CONFIG
  if bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭঍") in CONFIG and CONFIG[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ঎")]:
    bstack1111l111l_opy_ = bstack1lll1l1ll_opy_(CONFIG)
    bstack1111ll11l_opy_(CONFIG[bstack11lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧএ")], bstack1111l111l_opy_)
def bstack1111ll11l_opy_(key, bstack1111l111l_opy_):
  global bstack1l1lllllll_opy_
  logger.info(bstack1llll111l1_opy_)
  try:
    bstack1l1lllllll_opy_ = Local()
    bstack11ll11111_opy_ = {bstack11lll1l_opy_ (u"ࠬࡱࡥࡺࠩঐ"): key}
    bstack11ll11111_opy_.update(bstack1111l111l_opy_)
    logger.debug(bstack1111l1ll_opy_.format(str(bstack11ll11111_opy_)))
    bstack1l1lllllll_opy_.start(**bstack11ll11111_opy_)
    if bstack1l1lllllll_opy_.isRunning():
      logger.info(bstack1lllll11l1_opy_)
  except Exception as e:
    bstack1llll11l1_opy_(bstack1l1lll1ll1_opy_.format(str(e)))
def bstack11l1llll1_opy_():
  global bstack1l1lllllll_opy_
  if bstack1l1lllllll_opy_.isRunning():
    logger.info(bstack111l1l1l_opy_)
    bstack1l1lllllll_opy_.stop()
  bstack1l1lllllll_opy_ = None
def bstack1llll1l111_opy_(bstack1lllllll1_opy_=[]):
  global CONFIG
  bstack111lll1l_opy_ = []
  bstack1llllll1l1_opy_ = [bstack11lll1l_opy_ (u"࠭࡯ࡴࠩ঑"), bstack11lll1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ঒"), bstack11lll1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬও"), bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫঔ"), bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨক"), bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬখ")]
  try:
    for err in bstack1lllllll1_opy_:
      bstack1l1llll1l_opy_ = {}
      for k in bstack1llllll1l1_opy_:
        val = CONFIG[bstack11lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨগ")][int(err[bstack11lll1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬঘ")])].get(k)
        if val:
          bstack1l1llll1l_opy_[k] = val
      bstack1l1llll1l_opy_[bstack11lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭ঙ")] = {
        err[bstack11lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭চ")]: err[bstack11lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")]
      }
      bstack111lll1l_opy_.append(bstack1l1llll1l_opy_)
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬজ") + str(e))
  finally:
    return bstack111lll1l_opy_
def bstack11llll11_opy_(file_name):
  bstack11l1lll1_opy_ = []
  try:
    bstack1l1l11l11_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l11l11_opy_):
      with open(bstack1l1l11l11_opy_) as f:
        bstack1l111l1l1_opy_ = json.load(f)
        bstack11l1lll1_opy_ = bstack1l111l1l1_opy_
      os.remove(bstack1l1l11l11_opy_)
    return bstack11l1lll1_opy_
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ঝ") + str(e))
def bstack111l1111_opy_():
  global bstack1ll1lll11_opy_
  global bstack1lll111ll_opy_
  global bstack1ll1l11lll_opy_
  global bstack1llll1llll_opy_
  global bstack1ll11l1l11_opy_
  global bstack1ll1ll11ll_opy_
  percy.shutdown()
  bstack1l1111lll_opy_ = os.environ.get(bstack11lll1l_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ঞ"))
  if bstack1l1111lll_opy_ in [bstack11lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬট"), bstack11lll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ঠ")]:
    bstack1llll111_opy_()
  if bstack1ll1lll11_opy_:
    logger.warning(bstack1ll1l111l1_opy_.format(str(bstack1ll1lll11_opy_)))
  else:
    try:
      bstack11l1l1l11_opy_ = bstack1l11l1ll_opy_(bstack11lll1l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧড"), logger)
      if bstack11l1l1l11_opy_.get(bstack11lll1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧঢ")) and bstack11l1l1l11_opy_.get(bstack11lll1l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")).get(bstack11lll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ত")):
        logger.warning(bstack1ll1l111l1_opy_.format(str(bstack11l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪথ")][bstack11lll1l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨদ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1111l1l1l_opy_)
  global bstack1l1lllllll_opy_
  if bstack1l1lllllll_opy_:
    bstack11l1llll1_opy_()
  try:
    for driver in bstack1lll111ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1111l11l1_opy_)
  if bstack1ll1ll11ll_opy_ == bstack11lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ধ"):
    bstack1ll11l1l11_opy_ = bstack11llll11_opy_(bstack11lll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩন"))
  if bstack1ll1ll11ll_opy_ == bstack11lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ঩") and len(bstack1llll1llll_opy_) == 0:
    bstack1llll1llll_opy_ = bstack11llll11_opy_(bstack11lll1l_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨপ"))
    if len(bstack1llll1llll_opy_) == 0:
      bstack1llll1llll_opy_ = bstack11llll11_opy_(bstack11lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪফ"))
  bstack1llllll1l_opy_ = bstack11lll1l_opy_ (u"ࠬ࠭ব")
  if len(bstack1ll1l11lll_opy_) > 0:
    bstack1llllll1l_opy_ = bstack1llll1l111_opy_(bstack1ll1l11lll_opy_)
  elif len(bstack1llll1llll_opy_) > 0:
    bstack1llllll1l_opy_ = bstack1llll1l111_opy_(bstack1llll1llll_opy_)
  elif len(bstack1ll11l1l11_opy_) > 0:
    bstack1llllll1l_opy_ = bstack1llll1l111_opy_(bstack1ll11l1l11_opy_)
  elif len(bstack1ll111lll1_opy_) > 0:
    bstack1llllll1l_opy_ = bstack1llll1l111_opy_(bstack1ll111lll1_opy_)
  if bool(bstack1llllll1l_opy_):
    bstack1111l1ll1_opy_(bstack1llllll1l_opy_)
  else:
    bstack1111l1ll1_opy_()
  bstack11l1111l1_opy_(bstack11ll1l1l1_opy_, logger)
def bstack1l1llll11l_opy_(self, *args):
  logger.error(bstack1ll1l1l11l_opy_)
  bstack111l1111_opy_()
  sys.exit(1)
def bstack1llll11l1_opy_(err):
  logger.critical(bstack1l1llllll1_opy_.format(str(err)))
  bstack1111l1ll1_opy_(bstack1l1llllll1_opy_.format(str(err)))
  atexit.unregister(bstack111l1111_opy_)
  bstack1llll111_opy_()
  sys.exit(1)
def bstack1l1lll1lll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1111l1ll1_opy_(message)
  atexit.unregister(bstack111l1111_opy_)
  bstack1llll111_opy_()
  sys.exit(1)
def bstack1l1lll11_opy_():
  global CONFIG
  global bstack1llll1lll1_opy_
  global bstack1111111ll_opy_
  global bstack1l11ll1l_opy_
  CONFIG = bstack111l1ll1_opy_()
  bstack1ll1ll1l1l_opy_()
  bstack11l111l1_opy_()
  CONFIG = bstack1llll1111l_opy_(CONFIG)
  update(CONFIG, bstack1111111ll_opy_)
  update(CONFIG, bstack1llll1lll1_opy_)
  CONFIG = bstack1lll1l111_opy_(CONFIG)
  bstack1l11ll1l_opy_ = bstack1l1l11l1_opy_(CONFIG)
  bstack1lll1l1111_opy_.bstack1lll11l1_opy_(bstack11lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧভ"), bstack1l11ll1l_opy_)
  if (bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪম") in CONFIG and bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫয") in bstack1llll1lll1_opy_) or (
          bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in CONFIG and bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") not in bstack1111111ll_opy_):
    if os.getenv(bstack11lll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨল")):
      CONFIG[bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঳")] = os.getenv(bstack11lll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ঴"))
    else:
      bstack1lll111l_opy_()
  elif (bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in CONFIG and bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪশ") in CONFIG) or (
          bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬষ") in bstack1111111ll_opy_ and bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭স") not in bstack1llll1lll1_opy_):
    del (CONFIG[bstack11lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭হ")])
  if bstack11lllll1_opy_(CONFIG):
    bstack1llll11l1_opy_(bstack1llllllll_opy_)
  bstack1llll11lll_opy_()
  bstack1lll1111_opy_()
  if bstack1l1lllll_opy_:
    CONFIG[bstack11lll1l_opy_ (u"ࠬࡧࡰࡱࠩ঺")] = bstack1lll1l11l_opy_(CONFIG)
    logger.info(bstack111l11l11_opy_.format(CONFIG[bstack11lll1l_opy_ (u"࠭ࡡࡱࡲࠪ঻")]))
def bstack1lll111111_opy_(config, bstack11l11l1ll_opy_):
  global CONFIG
  global bstack1l1lllll_opy_
  CONFIG = config
  bstack1l1lllll_opy_ = bstack11l11l1ll_opy_
def bstack1lll1111_opy_():
  global CONFIG
  global bstack1l1lllll_opy_
  if bstack11lll1l_opy_ (u"ࠧࡢࡲࡳ়ࠫ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1l1lll1l1_opy_)
    bstack1l1lllll_opy_ = True
    bstack1lll1l1111_opy_.bstack1lll11l1_opy_(bstack11lll1l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧঽ"), True)
def bstack1lll1l11l_opy_(config):
  bstack1l1l11ll_opy_ = bstack11lll1l_opy_ (u"ࠩࠪা")
  app = config[bstack11lll1l_opy_ (u"ࠪࡥࡵࡶࠧি")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll11lll1_opy_:
      if os.path.exists(app):
        bstack1l1l11ll_opy_ = bstack1lll11111_opy_(config, app)
      elif bstack1ll11l1l_opy_(app):
        bstack1l1l11ll_opy_ = app
      else:
        bstack1llll11l1_opy_(bstack1lll11ll1l_opy_.format(app))
    else:
      if bstack1ll11l1l_opy_(app):
        bstack1l1l11ll_opy_ = app
      elif os.path.exists(app):
        bstack1l1l11ll_opy_ = bstack1lll11111_opy_(app)
      else:
        bstack1llll11l1_opy_(bstack1ll11l11l_opy_)
  else:
    if len(app) > 2:
      bstack1llll11l1_opy_(bstack11l111l11_opy_)
    elif len(app) == 2:
      if bstack11lll1l_opy_ (u"ࠫࡵࡧࡴࡩࠩী") in app and bstack11lll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨু") in app:
        if os.path.exists(app[bstack11lll1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫূ")]):
          bstack1l1l11ll_opy_ = bstack1lll11111_opy_(config, app[bstack11lll1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬৃ")], app[bstack11lll1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫৄ")])
        else:
          bstack1llll11l1_opy_(bstack1lll11ll1l_opy_.format(app))
      else:
        bstack1llll11l1_opy_(bstack11l111l11_opy_)
    else:
      for key in app:
        if key in bstack1lll1l1l11_opy_:
          if key == bstack11lll1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৅"):
            if os.path.exists(app[key]):
              bstack1l1l11ll_opy_ = bstack1lll11111_opy_(config, app[key])
            else:
              bstack1llll11l1_opy_(bstack1lll11ll1l_opy_.format(app))
          else:
            bstack1l1l11ll_opy_ = app[key]
        else:
          bstack1llll11l1_opy_(bstack1llllll111_opy_)
  return bstack1l1l11ll_opy_
def bstack1ll11l1l_opy_(bstack1l1l11ll_opy_):
  import re
  bstack1llll11111_opy_ = re.compile(bstack11lll1l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ৆"))
  bstack1lllll1ll1_opy_ = re.compile(bstack11lll1l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣে"))
  if bstack11lll1l_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫৈ") in bstack1l1l11ll_opy_ or re.fullmatch(bstack1llll11111_opy_, bstack1l1l11ll_opy_) or re.fullmatch(bstack1lllll1ll1_opy_, bstack1l1l11ll_opy_):
    return True
  else:
    return False
def bstack1lll11111_opy_(config, path, bstack111llll11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11lll1l_opy_ (u"࠭ࡲࡣࠩ৉")).read()).hexdigest()
  bstack111ll111l_opy_ = bstack1111l1111_opy_(md5_hash)
  bstack1l1l11ll_opy_ = None
  if bstack111ll111l_opy_:
    logger.info(bstack11l1lll11_opy_.format(bstack111ll111l_opy_, md5_hash))
    return bstack111ll111l_opy_
  bstack11lll1lll_opy_ = MultipartEncoder(
    fields={
      bstack11lll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࠬ৊"): (os.path.basename(path), open(os.path.abspath(path), bstack11lll1l_opy_ (u"ࠨࡴࡥࠫো")), bstack11lll1l_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ৌ")),
      bstack11lll1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ্࠭"): bstack111llll11_opy_
    }
  )
  response = requests.post(bstack11lll1ll1_opy_, data=bstack11lll1lll_opy_,
                           headers={bstack11lll1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪৎ"): bstack11lll1lll_opy_.content_type},
                           auth=(config[bstack11lll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ৏")], config[bstack11lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৐")]))
  try:
    res = json.loads(response.text)
    bstack1l1l11ll_opy_ = res[bstack11lll1l_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ৑")]
    logger.info(bstack1ll1111l11_opy_.format(bstack1l1l11ll_opy_))
    bstack1ll1l1llll_opy_(md5_hash, bstack1l1l11ll_opy_)
  except ValueError as err:
    bstack1llll11l1_opy_(bstack1l11111l1_opy_.format(str(err)))
  return bstack1l1l11ll_opy_
def bstack1llll11lll_opy_():
  global CONFIG
  global bstack1l11111l_opy_
  bstack11l1111ll_opy_ = 0
  bstack11l1l11l_opy_ = 1
  if bstack11lll1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ৒") in CONFIG:
    bstack11l1l11l_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৓")]
  if bstack11lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৔") in CONFIG:
    bstack11l1111ll_opy_ = len(CONFIG[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৕")])
  bstack1l11111l_opy_ = int(bstack11l1l11l_opy_) * int(bstack11l1111ll_opy_)
def bstack1111l1111_opy_(md5_hash):
  bstack1ll1ll1l11_opy_ = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠬࢄࠧ৖")), bstack11lll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ৗ"), bstack11lll1l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ৘"))
  if os.path.exists(bstack1ll1ll1l11_opy_):
    bstack1lllllllll_opy_ = json.load(open(bstack1ll1ll1l11_opy_, bstack11lll1l_opy_ (u"ࠨࡴࡥࠫ৙")))
    if md5_hash in bstack1lllllllll_opy_:
      bstack1l1lllll11_opy_ = bstack1lllllllll_opy_[md5_hash]
      bstack111ll1ll1_opy_ = datetime.datetime.now()
      bstack1ll11111ll_opy_ = datetime.datetime.strptime(bstack1l1lllll11_opy_[bstack11lll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ৚")], bstack11lll1l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৛"))
      if (bstack111ll1ll1_opy_ - bstack1ll11111ll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1lllll11_opy_[bstack11lll1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩড়")]):
        return None
      return bstack1l1lllll11_opy_[bstack11lll1l_opy_ (u"ࠬ࡯ࡤࠨঢ়")]
  else:
    return None
def bstack1ll1l1llll_opy_(md5_hash, bstack1l1l11ll_opy_):
  bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"࠭ࡾࠨ৞")), bstack11lll1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧয়"))
  if not os.path.exists(bstack111ll1111_opy_):
    os.makedirs(bstack111ll1111_opy_)
  bstack1ll1ll1l11_opy_ = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠨࢀࠪৠ")), bstack11lll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩৡ"), bstack11lll1l_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫৢ"))
  bstack1l111l11_opy_ = {
    bstack11lll1l_opy_ (u"ࠫ࡮ࡪࠧৣ"): bstack1l1l11ll_opy_,
    bstack11lll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৤"): datetime.datetime.strftime(datetime.datetime.now(), bstack11lll1l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৥")),
    bstack11lll1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ০"): str(__version__)
  }
  if os.path.exists(bstack1ll1ll1l11_opy_):
    bstack1lllllllll_opy_ = json.load(open(bstack1ll1ll1l11_opy_, bstack11lll1l_opy_ (u"ࠨࡴࡥࠫ১")))
  else:
    bstack1lllllllll_opy_ = {}
  bstack1lllllllll_opy_[md5_hash] = bstack1l111l11_opy_
  with open(bstack1ll1ll1l11_opy_, bstack11lll1l_opy_ (u"ࠤࡺ࠯ࠧ২")) as outfile:
    json.dump(bstack1lllllllll_opy_, outfile)
def bstack1l1ll1l1_opy_(self):
  return
def bstack111l1111l_opy_(self):
  return
def bstack11ll11l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1llll11_opy_(self):
  global bstack11l11ll1_opy_
  global bstack11ll1ll1_opy_
  global bstack1111l111_opy_
  try:
    if bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ৩") in bstack11l11ll1_opy_ and self.session_id != None and bstack11lll111_opy_(threading.current_thread(), bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ৪"), bstack11lll1l_opy_ (u"ࠬ࠭৫")) != bstack11lll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ৬"):
      bstack111l11lll_opy_ = bstack11lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ৭") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ৮")
      bstack1lll111l11_opy_ = bstack1llll1ll_opy_(bstack11lll1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ৯"), bstack11lll1l_opy_ (u"ࠪࠫৰ"), bstack111l11lll_opy_, bstack11lll1l_opy_ (u"ࠫ࠱ࠦࠧৱ").join(
        threading.current_thread().bstackTestErrorMessages), bstack11lll1l_opy_ (u"ࠬ࠭৲"), bstack11lll1l_opy_ (u"࠭ࠧ৳"))
      if bstack111l11lll_opy_ == bstack11lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ৴"):
        bstack1ll11llll_opy_(logger)
      if self != None:
        self.execute_script(bstack1lll111l11_opy_)
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ৵") + str(e))
  bstack1111l111_opy_(self)
  self.session_id = None
def bstack1lll1lllll_opy_(self, *args, **kwargs):
  bstack1lll1l1lll_opy_ = bstack11ll11ll_opy_(self, *args, **kwargs)
  bstack111lll111_opy_.bstack1111111l1_opy_(self)
  return bstack1lll1l1lll_opy_
def bstack111lll11l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11ll1ll1_opy_
  global bstack1l11ll1ll_opy_
  global bstack11l1ll11l_opy_
  global bstack1l11llll1_opy_
  global bstack1l1111l11_opy_
  global bstack11l11ll1_opy_
  global bstack11ll11ll_opy_
  global bstack1lll111ll_opy_
  global bstack1lllllll11_opy_
  global bstack111l111l1_opy_
  CONFIG[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ৶")] = str(bstack11l11ll1_opy_) + str(__version__)
  command_executor = bstack111l11111_opy_()
  logger.debug(bstack11l1l1lll_opy_.format(command_executor))
  proxy = bstack1ll111ll1l_opy_(CONFIG, proxy)
  bstack1ll11ll11l_opy_ = 0 if bstack1l11ll1ll_opy_ < 0 else bstack1l11ll1ll_opy_
  try:
    if bstack1l11llll1_opy_ is True:
      bstack1ll11ll11l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1111l11_opy_ is True:
      bstack1ll11ll11l_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll11ll11l_opy_ = 0
  bstack1111lllll_opy_ = bstack111l1l11_opy_(CONFIG, bstack1ll11ll11l_opy_)
  logger.debug(bstack1llll111ll_opy_.format(str(bstack1111lllll_opy_)))
  if bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৷") in CONFIG and CONFIG[bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ৸")]:
    bstack111ll1l1_opy_(bstack1111lllll_opy_)
  if desired_capabilities:
    bstack1l111ll1_opy_ = bstack1llll1111l_opy_(desired_capabilities)
    bstack1l111ll1_opy_[bstack11lll1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ৹")] = bstack1l111l1l_opy_(CONFIG)
    bstack1ll11lll_opy_ = bstack111l1l11_opy_(bstack1l111ll1_opy_)
    if bstack1ll11lll_opy_:
      bstack1111lllll_opy_ = update(bstack1ll11lll_opy_, bstack1111lllll_opy_)
    desired_capabilities = None
  if options:
    bstack11111lll1_opy_(options, bstack1111lllll_opy_)
  if not options:
    options = bstack1l11l1lll_opy_(bstack1111lllll_opy_)
  bstack111l111l1_opy_ = CONFIG.get(bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৺"))[bstack1ll11ll11l_opy_]
  if bstack1111l11ll_opy_.bstack1l11111ll_opy_(CONFIG, bstack1ll11ll11l_opy_) and bstack1111l11ll_opy_.bstack1ll11ll11_opy_(bstack1111lllll_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1111l11ll_opy_.set_capabilities(bstack1111lllll_opy_, CONFIG)
  if proxy and bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ৻")):
    options.proxy(proxy)
  if options and bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧৼ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll1ll11_opy_() < version.parse(bstack11lll1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ৽")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1111lllll_opy_)
  logger.info(bstack1ll11111l_opy_)
  if bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ৾")):
    bstack11ll11ll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ৿")):
    bstack11ll11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ਀")):
    bstack11ll11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11ll11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lll1lll1_opy_ = bstack11lll1l_opy_ (u"࠭ࠧਁ")
    if bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨਂ")):
      bstack1lll1lll1_opy_ = self.caps.get(bstack11lll1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣਃ"))
    else:
      bstack1lll1lll1_opy_ = self.capabilities.get(bstack11lll1l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ਄"))
    if bstack1lll1lll1_opy_:
      bstack11llll11l_opy_(bstack1lll1lll1_opy_)
      if bstack1ll1ll11_opy_() <= version.parse(bstack11lll1l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪਅ")):
        self.command_executor._url = bstack11lll1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧਆ") + bstack1lll1l1l_opy_ + bstack11lll1l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤਇ")
      else:
        self.command_executor._url = bstack11lll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣਈ") + bstack1lll1lll1_opy_ + bstack11lll1l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣਉ")
      logger.debug(bstack1ll1l1ll1_opy_.format(bstack1lll1lll1_opy_))
    else:
      logger.debug(bstack11llll1l1_opy_.format(bstack11lll1l_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤਊ")))
  except Exception as e:
    logger.debug(bstack11llll1l1_opy_.format(e))
  if bstack11lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ਋") in bstack11l11ll1_opy_:
    bstack1l1111l1l_opy_(bstack1l11ll1ll_opy_, bstack1lllllll11_opy_)
  bstack11ll1ll1_opy_ = self.session_id
  if bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ਌") in bstack11l11ll1_opy_ or bstack11lll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ਍") in bstack11l11ll1_opy_:
    threading.current_thread().bstack11lllllll_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack111lll111_opy_.bstack1111111l1_opy_(self)
  bstack1lll111ll_opy_.append(self)
  if bstack11lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਎") in CONFIG and bstack11lll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਏ") in CONFIG[bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਐ")][bstack1ll11ll11l_opy_]:
    bstack11l1ll11l_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਑")][bstack1ll11ll11l_opy_][bstack11lll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ਒")]
  logger.debug(bstack1llll11l1l_opy_.format(bstack11ll1ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l1lll111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll111l11_opy_
      if(bstack11lll1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧਓ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠫࢃ࠭ਔ")), bstack11lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬਕ"), bstack11lll1l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨਖ")), bstack11lll1l_opy_ (u"ࠧࡸࠩਗ")) as fp:
          fp.write(bstack11lll1l_opy_ (u"ࠣࠤਘ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11lll1l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦਙ")))):
          with open(args[1], bstack11lll1l_opy_ (u"ࠪࡶࠬਚ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11lll1l_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪਛ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l111ll_opy_)
            lines.insert(1, bstack1111llll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11lll1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢਜ")), bstack11lll1l_opy_ (u"࠭ࡷࠨਝ")) as bstack1l1llll1l1_opy_:
              bstack1l1llll1l1_opy_.writelines(lines)
        CONFIG[bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਞ")] = str(bstack11l11ll1_opy_) + str(__version__)
        bstack1ll11ll11l_opy_ = 0 if bstack1l11ll1ll_opy_ < 0 else bstack1l11ll1ll_opy_
        try:
          if bstack1l11llll1_opy_ is True:
            bstack1ll11ll11l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1111l11_opy_ is True:
            bstack1ll11ll11l_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll11ll11l_opy_ = 0
        CONFIG[bstack11lll1l_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣਟ")] = False
        CONFIG[bstack11lll1l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣਠ")] = True
        bstack1111lllll_opy_ = bstack111l1l11_opy_(CONFIG, bstack1ll11ll11l_opy_)
        logger.debug(bstack1llll111ll_opy_.format(str(bstack1111lllll_opy_)))
        if CONFIG.get(bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧਡ")):
          bstack111ll1l1_opy_(bstack1111lllll_opy_)
        if bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਢ") in CONFIG and bstack11lll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਣ") in CONFIG[bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਤ")][bstack1ll11ll11l_opy_]:
          bstack11l1ll11l_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਥ")][bstack1ll11ll11l_opy_][bstack11lll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਦ")]
        args.append(os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠩࢁࠫਧ")), bstack11lll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪਨ"), bstack11lll1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭਩")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1111lllll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11lll1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢਪ"))
      bstack1ll111l11_opy_ = True
      return bstack1l1llll111_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11l11l11l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l11ll1ll_opy_
    global bstack11l1ll11l_opy_
    global bstack1l11llll1_opy_
    global bstack1l1111l11_opy_
    global bstack11l11ll1_opy_
    CONFIG[bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack11l11ll1_opy_) + str(__version__)
    bstack1ll11ll11l_opy_ = 0 if bstack1l11ll1ll_opy_ < 0 else bstack1l11ll1ll_opy_
    try:
      if bstack1l11llll1_opy_ is True:
        bstack1ll11ll11l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1111l11_opy_ is True:
        bstack1ll11ll11l_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll11ll11l_opy_ = 0
    CONFIG[bstack11lll1l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨਬ")] = True
    bstack1111lllll_opy_ = bstack111l1l11_opy_(CONFIG, bstack1ll11ll11l_opy_)
    logger.debug(bstack1llll111ll_opy_.format(str(bstack1111lllll_opy_)))
    if CONFIG.get(bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")):
      bstack111ll1l1_opy_(bstack1111lllll_opy_)
    if bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਮ") in CONFIG and bstack11lll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਯ") in CONFIG[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")][bstack1ll11ll11l_opy_]:
      bstack11l1ll11l_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack1ll11ll11l_opy_][bstack11lll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਲ")]
    import urllib
    import json
    bstack1l1111l1_opy_ = bstack11lll1l_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩਲ਼") + urllib.parse.quote(json.dumps(bstack1111lllll_opy_))
    browser = self.connect(bstack1l1111l1_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1lllll1_opy_():
    global bstack1ll111l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11l11l_opy_
        bstack1ll111l11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1lll111_opy_
      bstack1ll111l11_opy_ = True
    except Exception as e:
      pass
def bstack1l111llll_opy_(context, bstack11ll1111_opy_):
  try:
    context.page.evaluate(bstack11lll1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ਴"), bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ਵ")+ json.dumps(bstack11ll1111_opy_) + bstack11lll1l_opy_ (u"ࠥࢁࢂࠨਸ਼"))
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤ਷"), e)
def bstack11l111l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11lll1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨਸ"), bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫਹ") + json.dumps(message) + bstack11lll1l_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ਺") + json.dumps(level) + bstack11lll1l_opy_ (u"ࠨࡿࢀࠫ਻"))
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ਼ࠧ"), e)
def bstack11l1l1ll_opy_(context, status, message = bstack11lll1l_opy_ (u"ࠥࠦ਽")):
  try:
    if(status == bstack11lll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦਾ")):
      context.page.evaluate(bstack11lll1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨਿ"), bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡸࡥࡢࡵࡲࡲࠧࡀࠧੀ") + json.dumps(bstack11lll1l_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡࠤੁ") + str(message)) + bstack11lll1l_opy_ (u"ࠨ࠮ࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬੂ") + json.dumps(status) + bstack11lll1l_opy_ (u"ࠤࢀࢁࠧ੃"))
    else:
      context.page.evaluate(bstack11lll1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੄"), bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬ੅") + json.dumps(status) + bstack11lll1l_opy_ (u"ࠧࢃࡽࠣ੆"))
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥੇ"), e)
def bstack111ll11l_opy_(self, url):
  global bstack111ll1l11_opy_
  try:
    bstack11l11ll11_opy_(url)
  except Exception as err:
    logger.debug(bstack11111ll1l_opy_.format(str(err)))
  try:
    bstack111ll1l11_opy_(self, url)
  except Exception as e:
    try:
      bstack11l1ll1l1_opy_ = str(e)
      if any(err_msg in bstack11l1ll1l1_opy_ for err_msg in bstack11llll111_opy_):
        bstack11l11ll11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11111ll1l_opy_.format(str(err)))
    raise e
def bstack1lll11ll_opy_(self):
  global bstack1l1l11lll_opy_
  bstack1l1l11lll_opy_ = self
  return
def bstack1llll1ll1_opy_(self):
  global bstack1l1l1l1ll_opy_
  bstack1l1l1l1ll_opy_ = self
  return
def bstack111lll11_opy_(self, test):
  global CONFIG
  global bstack1l1l1l1ll_opy_
  global bstack1l1l11lll_opy_
  global bstack11ll1ll1_opy_
  global bstack111ll1ll_opy_
  global bstack11l1ll11l_opy_
  global bstack1lll1lll_opy_
  global bstack1l1l1ll1l_opy_
  global bstack11ll1l111_opy_
  global bstack1lll111ll_opy_
  global bstack111l111l1_opy_
  try:
    if not bstack11ll1ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠧࡿࠩੈ")), bstack11lll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ੉"), bstack11lll1l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੊"))) as f:
        bstack11ll1l1ll_opy_ = json.loads(bstack11lll1l_opy_ (u"ࠥࡿࠧੋ") + f.read().strip() + bstack11lll1l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ੌ") + bstack11lll1l_opy_ (u"ࠧࢃ੍ࠢ"))
        bstack11ll1ll1_opy_ = bstack11ll1l1ll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1lll111ll_opy_:
    for driver in bstack1lll111ll_opy_:
      if bstack11ll1ll1_opy_ == driver.session_id:
        if test:
          bstack1l1l11ll1_opy_ = str(test.data)
          if bstack11lll111_opy_(threading.current_thread(), bstack11lll1l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ੎"), None):
            logger.info(bstack11lll1l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢ੏"))
            bstack1111l11ll_opy_.bstack11lll11l1_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack11ll1ll11_opy_=bstack111l111l1_opy_)
        if not bstack1l11l111l_opy_ and bstack1l1l11ll1_opy_:
          bstack1ll1lll111_opy_ = {
            bstack11lll1l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੐"): bstack11lll1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪੑ"),
            bstack11lll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੒"): {
              bstack11lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ੓"): bstack1l1l11ll1_opy_
            }
          }
          bstack111l1l1l1_opy_ = bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ੔").format(json.dumps(bstack1ll1lll111_opy_))
          driver.execute_script(bstack111l1l1l1_opy_)
        if bstack111ll1ll_opy_:
          bstack11l1111l_opy_ = {
            bstack11lll1l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭੕"): bstack11lll1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ੖"),
            bstack11lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ੗"): {
              bstack11lll1l_opy_ (u"ࠩࡧࡥࡹࡧࠧ੘"): bstack1l1l11ll1_opy_ + bstack11lll1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬਖ਼"),
              bstack11lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪਗ਼"): bstack11lll1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪਜ਼")
            }
          }
          bstack1ll1lll111_opy_ = {
            bstack11lll1l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ੜ"): bstack11lll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ੝"),
            bstack11lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫਫ਼"): {
              bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ੟"): bstack11lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ੠")
            }
          }
          if bstack111ll1ll_opy_.status == bstack11lll1l_opy_ (u"ࠫࡕࡇࡓࡔࠩ੡"):
            bstack1llll1l11l_opy_ = bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ੢").format(json.dumps(bstack11l1111l_opy_))
            driver.execute_script(bstack1llll1l11l_opy_)
            bstack111l1l1l1_opy_ = bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ੣").format(json.dumps(bstack1ll1lll111_opy_))
            driver.execute_script(bstack111l1l1l1_opy_)
          elif bstack111ll1ll_opy_.status == bstack11lll1l_opy_ (u"ࠧࡇࡃࡌࡐࠬ੤"):
            reason = bstack11lll1l_opy_ (u"ࠣࠤ੥")
            bstack1lll11lll1_opy_ = bstack1l1l11ll1_opy_ + bstack11lll1l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪ੦")
            if bstack111ll1ll_opy_.message:
              reason = str(bstack111ll1ll_opy_.message)
              bstack1lll11lll1_opy_ = bstack1lll11lll1_opy_ + bstack11lll1l_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪ੧") + reason
            bstack11l1111l_opy_[bstack11lll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੨")] = {
              bstack11lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ੩"): bstack11lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ੪"),
              bstack11lll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬ੫"): bstack1lll11lll1_opy_
            }
            bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ੬")] = {
              bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ੭"): bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ੮"),
              bstack11lll1l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ੯"): reason
            }
            bstack1llll1l11l_opy_ = bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪੰ").format(json.dumps(bstack11l1111l_opy_))
            driver.execute_script(bstack1llll1l11l_opy_)
            bstack111l1l1l1_opy_ = bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੱ").format(json.dumps(bstack1ll1lll111_opy_))
            driver.execute_script(bstack111l1l1l1_opy_)
            bstack1ll11l111l_opy_(reason, str(bstack111ll1ll_opy_), str(bstack1l11ll1ll_opy_), logger)
  elif bstack11ll1ll1_opy_:
    try:
      data = {}
      bstack1l1l11ll1_opy_ = None
      if test:
        bstack1l1l11ll1_opy_ = str(test.data)
      if not bstack1l11l111l_opy_ and bstack1l1l11ll1_opy_:
        data[bstack11lll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬੲ")] = bstack1l1l11ll1_opy_
      if bstack111ll1ll_opy_:
        if bstack111ll1ll_opy_.status == bstack11lll1l_opy_ (u"ࠨࡒࡄࡗࡘ࠭ੳ"):
          data[bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩੴ")] = bstack11lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪੵ")
        elif bstack111ll1ll_opy_.status == bstack11lll1l_opy_ (u"ࠫࡋࡇࡉࡍࠩ੶"):
          data[bstack11lll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ੷")] = bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭੸")
          if bstack111ll1ll_opy_.message:
            data[bstack11lll1l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ੹")] = str(bstack111ll1ll_opy_.message)
      user = CONFIG[bstack11lll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ੺")]
      key = CONFIG[bstack11lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ੻")]
      url = bstack11lll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨ੼").format(user, key, bstack11ll1ll1_opy_)
      headers = {
        bstack11lll1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ੽"): bstack11lll1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ੾"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11lllll11_opy_.format(str(e)))
  if bstack1l1l1l1ll_opy_:
    bstack1l1l1ll1l_opy_(bstack1l1l1l1ll_opy_)
  if bstack1l1l11lll_opy_:
    bstack11ll1l111_opy_(bstack1l1l11lll_opy_)
  bstack1lll1lll_opy_(self, test)
def bstack1ll1ll111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll1ll1l_opy_
  global CONFIG
  global bstack1lll111ll_opy_
  global bstack11ll1ll1_opy_
  bstack1lllll1111_opy_ = None
  try:
    if bstack11lll111_opy_(threading.current_thread(), bstack11lll1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ੿"), None):
      try:
        if not bstack11ll1ll1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠧࡿࠩ઀")), bstack11lll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨઁ"), bstack11lll1l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫં"))) as f:
            bstack11ll1l1ll_opy_ = json.loads(bstack11lll1l_opy_ (u"ࠥࡿࠧઃ") + f.read().strip() + bstack11lll1l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭઄") + bstack11lll1l_opy_ (u"ࠧࢃࠢઅ"))
            bstack11ll1ll1_opy_ = bstack11ll1l1ll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1lll111ll_opy_:
        for driver in bstack1lll111ll_opy_:
          if bstack11ll1ll1_opy_ == driver.session_id:
            bstack1lllll1111_opy_ = driver
    bstack11l11ll1l_opy_ = bstack1111l11ll_opy_.bstack1lll11l1l_opy_(CONFIG, test.tags)
    if bstack1lllll1111_opy_:
      threading.current_thread().isA11yTest = bstack1111l11ll_opy_.bstack1lll1lll1l_opy_(bstack1lllll1111_opy_, bstack11l11ll1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l11ll1l_opy_
  except:
    pass
  bstack1llll1ll1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111ll1ll_opy_
  bstack111ll1ll_opy_ = self._test
def bstack1lll1l1l1_opy_():
  global bstack1l1lll1ll_opy_
  try:
    if os.path.exists(bstack1l1lll1ll_opy_):
      os.remove(bstack1l1lll1ll_opy_)
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩઆ") + str(e))
def bstack11111l11_opy_():
  global bstack1l1lll1ll_opy_
  bstack11l1l1l11_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1lll1ll_opy_):
      with open(bstack1l1lll1ll_opy_, bstack11lll1l_opy_ (u"ࠧࡸࠩઇ")):
        pass
      with open(bstack1l1lll1ll_opy_, bstack11lll1l_opy_ (u"ࠣࡹ࠮ࠦઈ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1lll1ll_opy_):
      bstack11l1l1l11_opy_ = json.load(open(bstack1l1lll1ll_opy_, bstack11lll1l_opy_ (u"ࠩࡵࡦࠬઉ")))
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬઊ") + str(e))
  finally:
    return bstack11l1l1l11_opy_
def bstack1l1111l1l_opy_(platform_index, item_index):
  global bstack1l1lll1ll_opy_
  try:
    bstack11l1l1l11_opy_ = bstack11111l11_opy_()
    bstack11l1l1l11_opy_[item_index] = platform_index
    with open(bstack1l1lll1ll_opy_, bstack11lll1l_opy_ (u"ࠦࡼ࠱ࠢઋ")) as outfile:
      json.dump(bstack11l1l1l11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪઌ") + str(e))
def bstack111lll1ll_opy_(bstack1ll1ll11l_opy_):
  global CONFIG
  bstack1lll1ll11l_opy_ = bstack11lll1l_opy_ (u"࠭ࠧઍ")
  if not bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ઎") in CONFIG:
    logger.info(bstack11lll1l_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬએ"))
  try:
    platform = CONFIG[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬઐ")][bstack1ll1ll11l_opy_]
    if bstack11lll1l_opy_ (u"ࠪࡳࡸ࠭ઑ") in platform:
      bstack1lll1ll11l_opy_ += str(platform[bstack11lll1l_opy_ (u"ࠫࡴࡹࠧ઒")]) + bstack11lll1l_opy_ (u"ࠬ࠲ࠠࠨઓ")
    if bstack11lll1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩઔ") in platform:
      bstack1lll1ll11l_opy_ += str(platform[bstack11lll1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪક")]) + bstack11lll1l_opy_ (u"ࠨ࠮ࠣࠫખ")
    if bstack11lll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ગ") in platform:
      bstack1lll1ll11l_opy_ += str(platform[bstack11lll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧઘ")]) + bstack11lll1l_opy_ (u"ࠫ࠱ࠦࠧઙ")
    if bstack11lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧચ") in platform:
      bstack1lll1ll11l_opy_ += str(platform[bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨછ")]) + bstack11lll1l_opy_ (u"ࠧ࠭ࠢࠪજ")
    if bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ઝ") in platform:
      bstack1lll1ll11l_opy_ += str(platform[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧઞ")]) + bstack11lll1l_opy_ (u"ࠪ࠰ࠥ࠭ટ")
    if bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬઠ") in platform:
      bstack1lll1ll11l_opy_ += str(platform[bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ડ")]) + bstack11lll1l_opy_ (u"࠭ࠬࠡࠩઢ")
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧણ") + str(e))
  finally:
    if bstack1lll1ll11l_opy_[len(bstack1lll1ll11l_opy_) - 2:] == bstack11lll1l_opy_ (u"ࠨ࠮ࠣࠫત"):
      bstack1lll1ll11l_opy_ = bstack1lll1ll11l_opy_[:-2]
    return bstack1lll1ll11l_opy_
def bstack1111lll11_opy_(path, bstack1lll1ll11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll1l1ll_opy_ = ET.parse(path)
    bstack1l11ll11l_opy_ = bstack1ll1l1ll_opy_.getroot()
    bstack1ll1111ll_opy_ = None
    for suite in bstack1l11ll11l_opy_.iter(bstack11lll1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨથ")):
      if bstack11lll1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪદ") in suite.attrib:
        suite.attrib[bstack11lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩધ")] += bstack11lll1l_opy_ (u"ࠬࠦࠧન") + bstack1lll1ll11l_opy_
        bstack1ll1111ll_opy_ = suite
    bstack1llll11l11_opy_ = None
    for robot in bstack1l11ll11l_opy_.iter(bstack11lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ઩")):
      bstack1llll11l11_opy_ = robot
    bstack1ll111lll_opy_ = len(bstack1llll11l11_opy_.findall(bstack11lll1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭પ")))
    if bstack1ll111lll_opy_ == 1:
      bstack1llll11l11_opy_.remove(bstack1llll11l11_opy_.findall(bstack11lll1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ"))[0])
      bstack11ll1l11l_opy_ = ET.Element(bstack11lll1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨબ"), attrib={bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨભ"): bstack11lll1l_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫમ"), bstack11lll1l_opy_ (u"ࠬ࡯ࡤࠨય"): bstack11lll1l_opy_ (u"࠭ࡳ࠱ࠩર")})
      bstack1llll11l11_opy_.insert(1, bstack11ll1l11l_opy_)
      bstack1l11ll111_opy_ = None
      for suite in bstack1llll11l11_opy_.iter(bstack11lll1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭઱")):
        bstack1l11ll111_opy_ = suite
      bstack1l11ll111_opy_.append(bstack1ll1111ll_opy_)
      bstack1lll11l111_opy_ = None
      for status in bstack1ll1111ll_opy_.iter(bstack11lll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨલ")):
        bstack1lll11l111_opy_ = status
      bstack1l11ll111_opy_.append(bstack1lll11l111_opy_)
    bstack1ll1l1ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧળ") + str(e))
def bstack1111l1lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l1ll1l_opy_
  global CONFIG
  if bstack11lll1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ઴") in options:
    del options[bstack11lll1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣવ")]
  bstack11111lll_opy_ = bstack11111l11_opy_()
  for bstack1l111111_opy_ in bstack11111lll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11lll1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬશ"), str(bstack1l111111_opy_), bstack11lll1l_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪષ"))
    bstack1111lll11_opy_(path, bstack111lll1ll_opy_(bstack11111lll_opy_[bstack1l111111_opy_]))
  bstack1lll1l1l1_opy_()
  return bstack11l1ll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll11ll1l1_opy_(self, ff_profile_dir):
  global bstack1ll1lll11l_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll1lll11l_opy_(self, ff_profile_dir)
def bstack1lll1111l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1ll11ll_opy_
  bstack1lllll111_opy_ = []
  if bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ") in CONFIG:
    bstack1lllll111_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫહ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11lll1l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥ઺")],
      pabot_args[bstack11lll1l_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦ઻")],
      argfile,
      pabot_args.get(bstack11lll1l_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ઼")),
      pabot_args[bstack11lll1l_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣઽ")],
      platform[0],
      bstack1l1ll11ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11lll1l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨા")] or [(bstack11lll1l_opy_ (u"ࠢࠣિ"), None)]
    for platform in enumerate(bstack1lllll111_opy_)
  ]
def bstack1l11l1l11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11lll1ll_opy_=bstack11lll1l_opy_ (u"ࠨࠩી")):
  global bstack1llll1l11_opy_
  self.platform_index = platform_index
  self.bstack1lll1l11l1_opy_ = bstack11lll1ll_opy_
  bstack1llll1l11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11l11l1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1l11l1l_opy_
  global bstack1l1ll1l1l_opy_
  if not bstack11lll1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫુ") in item.options:
    item.options[bstack11lll1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ")] = []
  for v in item.options[bstack11lll1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ૃ")]:
    if bstack11lll1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫૄ") in v:
      item.options[bstack11lll1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨૅ")].remove(v)
    if bstack11lll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ૆") in v:
      item.options[bstack11lll1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪે")].remove(v)
  item.options[bstack11lll1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫૈ")].insert(0, bstack11lll1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬૉ").format(item.platform_index))
  item.options[bstack11lll1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૊")].insert(0, bstack11lll1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬો").format(item.bstack1lll1l11l1_opy_))
  if bstack1l1ll1l1l_opy_:
    item.options[bstack11lll1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨૌ")].insert(0, bstack11lll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿ્ࠪ").format(bstack1l1ll1l1l_opy_))
  return bstack1ll1l11l1l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1l111l_opy_(command, item_index):
  os.environ[bstack11lll1l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ૎")] = json.dumps(CONFIG[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૏")][item_index % bstack1l1l1l111_opy_])
  global bstack1l1ll1l1l_opy_
  if bstack1l1ll1l1l_opy_:
    command[0] = command[0].replace(bstack11lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૐ"), bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ૑") + str(
      item_index) + bstack11lll1l_opy_ (u"ࠬࠦࠧ૒") + bstack1l1ll1l1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૓"),
                                    bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ૔") + str(item_index), 1)
def bstack11ll1lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11ll1111l_opy_
  bstack1l1l111l_opy_(command, item_index)
  return bstack11ll1111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11ll1111l_opy_
  bstack1l1l111l_opy_(command, item_index)
  return bstack11ll1111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1ll111ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11ll1111l_opy_
  bstack1l1l111l_opy_(command, item_index)
  return bstack11ll1111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11lll11l_opy_(self, runner, quiet=False, capture=True):
  global bstack111l1llll_opy_
  bstack1l1111ll_opy_ = bstack111l1llll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11lll1l_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨ૕")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11lll1l_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭૖")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1111ll_opy_
def bstack1ll11l1lll_opy_(self, name, context, *args):
  os.environ[bstack11lll1l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ૗")] = json.dumps(CONFIG[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૘")][int(threading.current_thread()._name) % bstack1l1l1l111_opy_])
  global bstack1lllllll1l_opy_
  if name == bstack11lll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭૙"):
    bstack1lllllll1l_opy_(self, name, context, *args)
    try:
      if not bstack1l11l111l_opy_:
        bstack1lllll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll11llll_opy_(bstack11lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ૚")) else context.browser
        bstack11ll1111_opy_ = str(self.feature.name)
        bstack1l111llll_opy_(context, bstack11ll1111_opy_)
        bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ૛") + json.dumps(bstack11ll1111_opy_) + bstack11lll1l_opy_ (u"ࠨࡿࢀࠫ૜"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11lll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ૝").format(str(e)))
  elif name == bstack11lll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૞"):
    bstack1lllllll1l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11lll1l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭૟")):
        self.driver_before_scenario = True
      if (not bstack1l11l111l_opy_):
        scenario_name = args[0].name
        feature_name = bstack11ll1111_opy_ = str(self.feature.name)
        bstack11ll1111_opy_ = feature_name + bstack11lll1l_opy_ (u"ࠬࠦ࠭ࠡࠩૠ") + scenario_name
        bstack1lllll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll11llll_opy_(bstack11lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬૡ")) else context.browser
        if self.driver_before_scenario:
          bstack1l111llll_opy_(context, bstack11ll1111_opy_)
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬૢ") + json.dumps(bstack11ll1111_opy_) + bstack11lll1l_opy_ (u"ࠨࡿࢀࠫૣ"))
    except Exception as e:
      logger.debug(bstack11lll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ૤").format(str(e)))
  elif name == bstack11lll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૥"):
    try:
      bstack11l1ll111_opy_ = args[0].status.name
      bstack1lllll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ૦") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack11l1ll111_opy_).lower() == bstack11lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ૧"):
        bstack1lll11l11_opy_ = bstack11lll1l_opy_ (u"࠭ࠧ૨")
        bstack11ll11l1l_opy_ = bstack11lll1l_opy_ (u"ࠧࠨ૩")
        bstack11l1l1l1_opy_ = bstack11lll1l_opy_ (u"ࠨࠩ૪")
        try:
          import traceback
          bstack1lll11l11_opy_ = self.exception.__class__.__name__
          bstack1ll11l11l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11ll11l1l_opy_ = bstack11lll1l_opy_ (u"ࠩࠣࠫ૫").join(bstack1ll11l11l1_opy_)
          bstack11l1l1l1_opy_ = bstack1ll11l11l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l111lll_opy_.format(str(e)))
        bstack1lll11l11_opy_ += bstack11l1l1l1_opy_
        bstack11l111l1l_opy_(context, json.dumps(str(args[0].name) + bstack11lll1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ૬") + str(bstack11ll11l1l_opy_)),
                            bstack11lll1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ૭"))
        if self.driver_before_scenario:
          bstack11l1l1ll_opy_(context, bstack11lll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ૮"), bstack1lll11l11_opy_)
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૯") + json.dumps(str(args[0].name) + bstack11lll1l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ૰") + str(bstack11ll11l1l_opy_)) + bstack11lll1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૱"))
        if self.driver_before_scenario:
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ૲") + json.dumps(bstack11lll1l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ૳") + str(bstack1lll11l11_opy_)) + bstack11lll1l_opy_ (u"ࠫࢂࢃࠧ૴"))
      else:
        bstack11l111l1l_opy_(context, bstack11lll1l_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ૵"), bstack11lll1l_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ૶"))
        if self.driver_before_scenario:
          bstack11l1l1ll_opy_(context, bstack11lll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ૷"))
        bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭૸") + json.dumps(str(args[0].name) + bstack11lll1l_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨૹ")) + bstack11lll1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩૺ"))
        if self.driver_before_scenario:
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨૻ"))
    except Exception as e:
      logger.debug(bstack11lll1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧૼ").format(str(e)))
  elif name == bstack11lll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭૽"):
    try:
      bstack1lllll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll11llll_opy_(bstack11lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૾")) else context.browser
      if context.failed is True:
        bstack1ll1111l1l_opy_ = []
        bstack111l1l11l_opy_ = []
        bstack1l1111ll1_opy_ = []
        bstack11l11l1l1_opy_ = bstack11lll1l_opy_ (u"ࠨࠩ૿")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1111l1l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll11l11l1_opy_ = traceback.format_tb(exc_tb)
            bstack1lll111l1l_opy_ = bstack11lll1l_opy_ (u"ࠩࠣࠫ଀").join(bstack1ll11l11l1_opy_)
            bstack111l1l11l_opy_.append(bstack1lll111l1l_opy_)
            bstack1l1111ll1_opy_.append(bstack1ll11l11l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l111lll_opy_.format(str(e)))
        bstack1lll11l11_opy_ = bstack11lll1l_opy_ (u"ࠪࠫଁ")
        for i in range(len(bstack1ll1111l1l_opy_)):
          bstack1lll11l11_opy_ += bstack1ll1111l1l_opy_[i] + bstack1l1111ll1_opy_[i] + bstack11lll1l_opy_ (u"ࠫࡡࡴࠧଂ")
        bstack11l11l1l1_opy_ = bstack11lll1l_opy_ (u"ࠬࠦࠧଃ").join(bstack111l1l11l_opy_)
        if not self.driver_before_scenario:
          bstack11l111l1l_opy_(context, bstack11l11l1l1_opy_, bstack11lll1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ଄"))
          bstack11l1l1ll_opy_(context, bstack11lll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢଅ"), bstack1lll11l11_opy_)
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଆ") + json.dumps(bstack11l11l1l1_opy_) + bstack11lll1l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩଇ"))
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪଈ") + json.dumps(bstack11lll1l_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤଉ") + str(bstack1lll11l11_opy_)) + bstack11lll1l_opy_ (u"ࠬࢃࡽࠨଊ"))
          bstack1ll11l111_opy_ = bstack1l1ll11l_opy_(bstack11l11l1l1_opy_, self.feature.name, logger)
          if (bstack1ll11l111_opy_ != None):
            bstack1ll111lll1_opy_.append(bstack1ll11l111_opy_)
      else:
        if not self.driver_before_scenario:
          bstack11l111l1l_opy_(context, bstack11lll1l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤଋ") + str(self.feature.name) + bstack11lll1l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤଌ"), bstack11lll1l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ଍"))
          bstack11l1l1ll_opy_(context, bstack11lll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ଎"))
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨଏ") + json.dumps(bstack11lll1l_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢଐ") + str(self.feature.name) + bstack11lll1l_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ଑")) + bstack11lll1l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ଒"))
          bstack1lllll1111_opy_.execute_script(bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡲࡤࡷࡸ࡫ࡤࠣࡿࢀࠫଓ"))
          bstack1ll11l111_opy_ = bstack1l1ll11l_opy_(bstack11l11l1l1_opy_, self.feature.name, logger)
          if (bstack1ll11l111_opy_ != None):
            bstack1ll111lll1_opy_.append(bstack1ll11l111_opy_)
    except Exception as e:
      logger.debug(bstack11lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪଔ").format(str(e)))
  else:
    bstack1lllllll1l_opy_(self, name, context, *args)
  if name in [bstack11lll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩକ"), bstack11lll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫଖ")]:
    bstack1lllllll1l_opy_(self, name, context, *args)
    if (name == bstack11lll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬଗ") and self.driver_before_scenario) or (
            name == bstack11lll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬଘ") and not self.driver_before_scenario):
      try:
        bstack1lllll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll11llll_opy_(bstack11lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬଙ")) else context.browser
        bstack1lllll1111_opy_.quit()
      except Exception:
        pass
def bstack1111ll1l_opy_(config, startdir):
  return bstack11lll1l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧଚ").format(bstack11lll1l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢଛ"))
notset = Notset()
def bstack11l1l111_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lllll111l_opy_
  if str(name).lower() == bstack11lll1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩଜ"):
    return bstack11lll1l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤଝ")
  else:
    return bstack1lllll111l_opy_(self, name, default, skip)
def bstack111llll1l_opy_(item, when):
  global bstack1ll1ll1l1_opy_
  try:
    bstack1ll1ll1l1_opy_(item, when)
  except Exception as e:
    pass
def bstack11ll11ll1_opy_():
  return
def bstack1llll1ll_opy_(type, name, status, reason, bstack11l11l11_opy_, bstack1ll1llll_opy_):
  bstack1ll1lll111_opy_ = {
    bstack11lll1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫଞ"): type,
    bstack11lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଟ"): {}
  }
  if type == bstack11lll1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨଠ"):
    bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଡ")][bstack11lll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧଢ")] = bstack11l11l11_opy_
    bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬଣ")][bstack11lll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨତ")] = json.dumps(str(bstack1ll1llll_opy_))
  if type == bstack11lll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଥ"):
    bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଦ")][bstack11lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫଧ")] = name
  if type == bstack11lll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪନ"):
    bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ଩")][bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩପ")] = status
    if status == bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪଫ"):
      bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧବ")][bstack11lll1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬଭ")] = json.dumps(str(reason))
  bstack111l1l1l1_opy_ = bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫମ").format(json.dumps(bstack1ll1lll111_opy_))
  return bstack111l1l1l1_opy_
def bstack111ll11ll_opy_(item, call, rep):
  global bstack1ll1l1l1ll_opy_
  global bstack1lll111ll_opy_
  global bstack1l11l111l_opy_
  name = bstack11lll1l_opy_ (u"ࠧࠨଯ")
  try:
    if rep.when == bstack11lll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ର"):
      bstack11ll1ll1_opy_ = threading.current_thread().bstack11lllllll_opy_
      try:
        if not bstack1l11l111l_opy_:
          name = str(rep.nodeid)
          bstack1lll111l11_opy_ = bstack1llll1ll_opy_(bstack11lll1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ଱"), name, bstack11lll1l_opy_ (u"ࠪࠫଲ"), bstack11lll1l_opy_ (u"ࠫࠬଳ"), bstack11lll1l_opy_ (u"ࠬ࠭଴"), bstack11lll1l_opy_ (u"࠭ࠧଵ"))
          threading.current_thread().bstack111l11ll1_opy_ = name
          for driver in bstack1lll111ll_opy_:
            if bstack11ll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1lll111l11_opy_)
      except Exception as e:
        logger.debug(bstack11lll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧଶ").format(str(e)))
      try:
        bstack11l11l111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11lll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩଷ"):
          status = bstack11lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩସ") if rep.outcome.lower() == bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪହ") else bstack11lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ଺")
          reason = bstack11lll1l_opy_ (u"ࠬ࠭଻")
          if status == bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ଼࠭"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11lll1l_opy_ (u"ࠧࡪࡰࡩࡳࠬଽ") if status == bstack11lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨା") else bstack11lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨି")
          data = name + bstack11lll1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬୀ") if status == bstack11lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୁ") else name + bstack11lll1l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨୂ") + reason
          bstack11111l1l1_opy_ = bstack1llll1ll_opy_(bstack11lll1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨୃ"), bstack11lll1l_opy_ (u"ࠧࠨୄ"), bstack11lll1l_opy_ (u"ࠨࠩ୅"), bstack11lll1l_opy_ (u"ࠩࠪ୆"), level, data)
          for driver in bstack1lll111ll_opy_:
            if bstack11ll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack11111l1l1_opy_)
      except Exception as e:
        logger.debug(bstack11lll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧେ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨୈ").format(str(e)))
  bstack1ll1l1l1ll_opy_(item, call, rep)
def bstack1ll1lll1ll_opy_(framework_name):
  global bstack11l11ll1_opy_
  global bstack1ll111l11_opy_
  global bstack11lll1l1l_opy_
  bstack11l11ll1_opy_ = framework_name
  logger.info(bstack11ll1lll_opy_.format(bstack11l11ll1_opy_.split(bstack11lll1l_opy_ (u"ࠬ࠳ࠧ୉"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l11ll1l_opy_:
      Service.start = bstack1l1ll1l1_opy_
      Service.stop = bstack111l1111l_opy_
      webdriver.Remote.get = bstack111ll11l_opy_
      WebDriver.close = bstack11ll11l1_opy_
      WebDriver.quit = bstack1l1llll11_opy_
      webdriver.Remote.__init__ = bstack111lll11l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1111lll1_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack11l11111_opy_ = getAccessibilityResultsSummary
    if not bstack1l11ll1l_opy_ and bstack111lll111_opy_.on():
      webdriver.Remote.__init__ = bstack1lll1lllll_opy_
    bstack1ll111l11_opy_ = True
  except Exception as e:
    pass
  bstack1ll1lllll1_opy_()
  if not bstack1ll111l11_opy_:
    bstack1l1lll1lll_opy_(bstack11lll1l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣ୊"), bstack1ll111l111_opy_)
  if bstack1lll1ll11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l11l1l1l_opy_
    except Exception as e:
      logger.error(bstack11l1l1l1l_opy_.format(str(e)))
  if bstack1lll1l11_opy_():
    bstack1lll111lll_opy_(CONFIG, logger)
  if (bstack11lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ୋ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll11ll1l1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1llll1ll1_opy_
      except Exception as e:
        logger.warn(bstack1llll111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lll11ll_opy_
      except Exception as e:
        logger.debug(bstack1ll1111lll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1llll111l_opy_)
    Output.end_test = bstack111lll11_opy_
    TestStatus.__init__ = bstack1ll1ll111_opy_
    QueueItem.__init__ = bstack1l11l1l11_opy_
    pabot._create_items = bstack1lll1111l1_opy_
    try:
      from pabot import __version__ as bstack1lll11l11l_opy_
      if version.parse(bstack1lll11l11l_opy_) >= version.parse(bstack11lll1l_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨୌ")):
        pabot._run = bstack1ll111ll11_opy_
      elif version.parse(bstack1lll11l11l_opy_) >= version.parse(bstack11lll1l_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱୍ࠩ")):
        pabot._run = bstack1ll1l111_opy_
      else:
        pabot._run = bstack11ll1lll1_opy_
    except Exception as e:
      pabot._run = bstack11ll1lll1_opy_
    pabot._create_command_for_execution = bstack11l11l1l_opy_
    pabot._report_results = bstack1111l1lll_opy_
  if bstack11lll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ୎") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1lll11111l_opy_)
    Runner.run_hook = bstack1ll11l1lll_opy_
    Step.run = bstack11lll11l_opy_
  if bstack11lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ୏") in str(framework_name).lower():
    if not bstack1l11ll1l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1111ll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11ll11ll1_opy_
      Config.getoption = bstack11l1l111_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack111ll11ll_opy_
    except Exception as e:
      pass
def bstack1l11lllll_opy_():
  global CONFIG
  if bstack11lll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ୐") in CONFIG and int(CONFIG[bstack11lll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭୑")]) > 1:
    logger.warn(bstack1l1ll111_opy_)
def bstack1111lll1l_opy_(arg, bstack1llll1l1ll_opy_, bstack11l1lll1_opy_=None):
  global CONFIG
  global bstack1lll1l1l_opy_
  global bstack1l1lllll_opy_
  global bstack1l11ll1l_opy_
  global bstack1lll1l1111_opy_
  bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ୒")
  if bstack1llll1l1ll_opy_ and isinstance(bstack1llll1l1ll_opy_, str):
    bstack1llll1l1ll_opy_ = eval(bstack1llll1l1ll_opy_)
  CONFIG = bstack1llll1l1ll_opy_[bstack11lll1l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ୓")]
  bstack1lll1l1l_opy_ = bstack1llll1l1ll_opy_[bstack11lll1l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ୔")]
  bstack1l1lllll_opy_ = bstack1llll1l1ll_opy_[bstack11lll1l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ୕")]
  bstack1l11ll1l_opy_ = bstack1llll1l1ll_opy_[bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧୖ")]
  bstack1lll1l1111_opy_.bstack1lll11l1_opy_(bstack11lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ୗ"), bstack1l11ll1l_opy_)
  os.environ[bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ୘")] = bstack1l1111lll_opy_
  os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭୙")] = json.dumps(CONFIG)
  os.environ[bstack11lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ୚")] = bstack1lll1l1l_opy_
  os.environ[bstack11lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୛")] = str(bstack1l1lllll_opy_)
  os.environ[bstack11lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩଡ଼")] = str(True)
  if bstack1ll11ll1_opy_(arg, [bstack11lll1l_opy_ (u"ࠫ࠲ࡴࠧଢ଼"), bstack11lll1l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭୞")]) != -1:
    os.environ[bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧୟ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1l1111l_opy_)
    return
  bstack111111ll_opy_()
  global bstack1l11111l_opy_
  global bstack1l11ll1ll_opy_
  global bstack1l1ll11ll_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1llll1llll_opy_
  global bstack11lll1l1l_opy_
  global bstack1l11llll1_opy_
  arg.append(bstack11lll1l_opy_ (u"ࠢ࠮࡙ࠥୠ"))
  arg.append(bstack11lll1l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦୡ"))
  arg.append(bstack11lll1l_opy_ (u"ࠤ࠰࡛ࠧୢ"))
  arg.append(bstack11lll1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤୣ"))
  global bstack11ll11ll_opy_
  global bstack1111l111_opy_
  global bstack1llll1ll1l_opy_
  global bstack1ll1lll11l_opy_
  global bstack1llll1l11_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1l1l1111_opy_
  global bstack111ll1l11_opy_
  global bstack11ll1l11_opy_
  global bstack1lllll111l_opy_
  global bstack1ll1ll1l1_opy_
  global bstack1ll1l1l1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll11ll_opy_ = webdriver.Remote.__init__
    bstack1111l111_opy_ = WebDriver.quit
    bstack1l1l1111_opy_ = WebDriver.close
    bstack111ll1l11_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1llllll1ll_opy_(CONFIG) and bstack1l1l1llll_opy_():
    if bstack1ll1ll11_opy_() < version.parse(bstack1l1lll1l_opy_):
      logger.error(bstack111l1ll11_opy_.format(bstack1ll1ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll1l11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l1l1l1l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lllll111l_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll1ll1l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l1l11l1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll1l1l1ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11lll1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ୤"))
  bstack1l1ll11ll_opy_ = CONFIG.get(bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୥"), {}).get(bstack11lll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ୦"))
  bstack1l11llll1_opy_ = True
  bstack1ll1lll1ll_opy_(bstack1l1l11111_opy_)
  os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ୧")] = CONFIG[bstack11lll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ୨")]
  os.environ[bstack11lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ୩")] = CONFIG[bstack11lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭୪")]
  os.environ[bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ୫")] = bstack1l11ll1l_opy_.__str__()
  from _pytest.config import main as bstack1ll1l111ll_opy_
  bstack1ll1l111ll_opy_(arg)
  if bstack11lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ୬") in multiprocessing.current_process().__dict__.keys():
    for bstack1ll1lllll_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack11l1lll1_opy_.append(bstack1ll1lllll_opy_)
def bstack11ll1l1l_opy_(arg):
  bstack1ll1lll1ll_opy_(bstack1l1l111ll_opy_)
  os.environ[bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ୭")] = str(bstack1l1lllll_opy_)
  from behave.__main__ import main as bstack1ll1l1ll11_opy_
  bstack1ll1l1ll11_opy_(arg)
def bstack1ll1l1l1l1_opy_():
  logger.info(bstack1lll1llll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭୮"), help=bstack11lll1l_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩ୯"))
  parser.add_argument(bstack11lll1l_opy_ (u"ࠩ࠰ࡹࠬ୰"), bstack11lll1l_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧୱ"), help=bstack11lll1l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ୲"))
  parser.add_argument(bstack11lll1l_opy_ (u"ࠬ࠳࡫ࠨ୳"), bstack11lll1l_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬ୴"), help=bstack11lll1l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨ୵"))
  parser.add_argument(bstack11lll1l_opy_ (u"ࠨ࠯ࡩࠫ୶"), bstack11lll1l_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ୷"), help=bstack11lll1l_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ୸"))
  bstack11ll1llll_opy_ = parser.parse_args()
  try:
    bstack1ll1lll1l1_opy_ = bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ୹")
    if bstack11ll1llll_opy_.framework and bstack11ll1llll_opy_.framework not in (bstack11lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ୺"), bstack11lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ୻")):
      bstack1ll1lll1l1_opy_ = bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭୼")
    bstack1l11l1l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1lll1l1_opy_)
    bstack1l1lllll1_opy_ = open(bstack1l11l1l1_opy_, bstack11lll1l_opy_ (u"ࠨࡴࠪ୽"))
    bstack111lll1l1_opy_ = bstack1l1lllll1_opy_.read()
    bstack1l1lllll1_opy_.close()
    if bstack11ll1llll_opy_.username:
      bstack111lll1l1_opy_ = bstack111lll1l1_opy_.replace(bstack11lll1l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ୾"), bstack11ll1llll_opy_.username)
    if bstack11ll1llll_opy_.key:
      bstack111lll1l1_opy_ = bstack111lll1l1_opy_.replace(bstack11lll1l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ୿"), bstack11ll1llll_opy_.key)
    if bstack11ll1llll_opy_.framework:
      bstack111lll1l1_opy_ = bstack111lll1l1_opy_.replace(bstack11lll1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ஀"), bstack11ll1llll_opy_.framework)
    file_name = bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ஁")
    file_path = os.path.abspath(file_name)
    bstack1l11l1ll1_opy_ = open(file_path, bstack11lll1l_opy_ (u"࠭ࡷࠨஂ"))
    bstack1l11l1ll1_opy_.write(bstack111lll1l1_opy_)
    bstack1l11l1ll1_opy_.close()
    logger.info(bstack1lll1llll1_opy_)
    try:
      os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩஃ")] = bstack11ll1llll_opy_.framework if bstack11ll1llll_opy_.framework != None else bstack11lll1l_opy_ (u"ࠣࠤ஄")
      config = yaml.safe_load(bstack111lll1l1_opy_)
      config[bstack11lll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩஅ")] = bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩஆ")
      bstack1lllll1ll_opy_(bstack11l11lll1_opy_, config)
    except Exception as e:
      logger.debug(bstack11l1ll1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11llllll_opy_.format(str(e)))
def bstack1lllll1ll_opy_(bstack111ll111_opy_, config, bstack1llll11ll1_opy_={}):
  global bstack1l11ll1l_opy_
  global bstack1ll1ll11ll_opy_
  if not config:
    return
  bstack1111ll11_opy_ = bstack1l11lll1l_opy_ if not bstack1l11ll1l_opy_ else (
    bstack1ll1l1lll1_opy_ if bstack11lll1l_opy_ (u"ࠫࡦࡶࡰࠨஇ") in config else bstack111llllll_opy_)
  data = {
    bstack11lll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧஈ"): config[bstack11lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨஉ")],
    bstack11lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪஊ"): config[bstack11lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஋")],
    bstack11lll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭஌"): bstack111ll111_opy_,
    bstack11lll1l_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ஍"): os.environ.get(bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭எ"), bstack1ll1ll11ll_opy_),
    bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧஏ"): bstack1ll1ll1lll_opy_,
    bstack11lll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨஐ"): bstack111l11l1l_opy_(),
    bstack11lll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ஑"): {
      bstack11lll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ஒ"): str(config[bstack11lll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩஓ")]) if bstack11lll1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪஔ") in config else bstack11lll1l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧக"),
      bstack11lll1l_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧ஖"): bstack11l1l1ll1_opy_(os.getenv(bstack11lll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣ஗"), bstack11lll1l_opy_ (u"ࠢࠣ஘"))),
      bstack11lll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪங"): bstack11lll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩச"),
      bstack11lll1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ஛"): bstack1111ll11_opy_,
      bstack11lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧஜ"): config[bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ஝")] if config[bstack11lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩஞ")] else bstack11lll1l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣட"),
      bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ஠"): str(config[bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ஡")]) if bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ஢") in config else bstack11lll1l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧண"),
      bstack11lll1l_opy_ (u"ࠬࡵࡳࠨத"): sys.platform,
      bstack11lll1l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ஥"): socket.gethostname()
    }
  }
  update(data[bstack11lll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ஦")], bstack1llll11ll1_opy_)
  try:
    response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭஧"), bstack1lllll11ll_opy_(bstack11llll1ll_opy_), data, {
      bstack11lll1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧந"): (config[bstack11lll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬன")], config[bstack11lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧப")])
    })
    if response:
      logger.debug(bstack1l1l1lll1_opy_.format(bstack111ll111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1ll1lll_opy_.format(str(e)))
def bstack11l1l1ll1_opy_(framework):
  return bstack11lll1l_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ஫").format(str(framework), __version__) if framework else bstack11lll1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ஬").format(
    __version__)
def bstack111111ll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l1lll11_opy_()
    logger.debug(bstack11llll1l_opy_.format(str(CONFIG)))
    bstack11lll1l11_opy_()
    bstack1llllllll1_opy_()
  except Exception as e:
    logger.error(bstack11lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦ஭") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll111ll_opy_
  atexit.register(bstack111l1111_opy_)
  signal.signal(signal.SIGINT, bstack1l1llll11l_opy_)
  signal.signal(signal.SIGTERM, bstack1l1llll11l_opy_)
def bstack1ll111ll_opy_(exctype, value, traceback):
  global bstack1lll111ll_opy_
  try:
    for driver in bstack1lll111ll_opy_:
      driver.execute_script(
        bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨம") + json.dumps(
          bstack11lll1l_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧய") + str(value)) + bstack11lll1l_opy_ (u"ࠪࢁࢂ࠭ர"))
  except Exception:
    pass
  bstack1111l1ll1_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1111l1ll1_opy_(message=bstack11lll1l_opy_ (u"ࠫࠬற")):
  global CONFIG
  try:
    if message:
      bstack1llll11ll1_opy_ = {
        bstack11lll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫல"): str(message)
      }
      bstack1lllll1ll_opy_(bstack1ll11l11_opy_, CONFIG, bstack1llll11ll1_opy_)
    else:
      bstack1lllll1ll_opy_(bstack1ll11l11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll11l11ll_opy_.format(str(e)))
def bstack1lll1l1l1l_opy_(bstack11111l1l_opy_, size):
  bstack1lll11lll_opy_ = []
  while len(bstack11111l1l_opy_) > size:
    bstack11111l11l_opy_ = bstack11111l1l_opy_[:size]
    bstack1lll11lll_opy_.append(bstack11111l11l_opy_)
    bstack11111l1l_opy_ = bstack11111l1l_opy_[size:]
  bstack1lll11lll_opy_.append(bstack11111l1l_opy_)
  return bstack1lll11lll_opy_
def bstack111111l1l_opy_(args):
  if bstack11lll1l_opy_ (u"࠭࠭࡮ࠩள") in args and bstack11lll1l_opy_ (u"ࠧࡱࡦࡥࠫழ") in args:
    return True
  return False
def run_on_browserstack(bstack1l11l11l_opy_=None, bstack11l1lll1_opy_=None, bstack11l1ll11_opy_=False):
  global CONFIG
  global bstack1lll1l1l_opy_
  global bstack1l1lllll_opy_
  global bstack1ll1ll11ll_opy_
  bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠨࠩவ")
  bstack11l1111l1_opy_(bstack11ll1l1l1_opy_, logger)
  if bstack1l11l11l_opy_ and isinstance(bstack1l11l11l_opy_, str):
    bstack1l11l11l_opy_ = eval(bstack1l11l11l_opy_)
  if bstack1l11l11l_opy_:
    CONFIG = bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩஶ")]
    bstack1lll1l1l_opy_ = bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫஷ")]
    bstack1l1lllll_opy_ = bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ஸ")]
    bstack1lll1l1111_opy_.bstack1lll11l1_opy_(bstack11lll1l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧஹ"), bstack1l1lllll_opy_)
    bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭஺")
  if not bstack11l1ll11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1l1111l_opy_)
      return
    if sys.argv[1] == bstack11lll1l_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ஻") or sys.argv[1] == bstack11lll1l_opy_ (u"ࠨ࠯ࡹࠫ஼"):
      logger.info(bstack11lll1l_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩ஽").format(__version__))
      return
    if sys.argv[1] == bstack11lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩா"):
      bstack1ll1l1l1l1_opy_()
      return
  args = sys.argv
  bstack111111ll_opy_()
  global bstack1l11111l_opy_
  global bstack1l1l1l111_opy_
  global bstack1l11llll1_opy_
  global bstack1l1111l11_opy_
  global bstack1l11ll1ll_opy_
  global bstack1l1ll11ll_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1ll1l11lll_opy_
  global bstack1llll1llll_opy_
  global bstack11lll1l1l_opy_
  global bstack1llllll11l_opy_
  bstack1l1l1l111_opy_ = len(CONFIG[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧி")])
  if not bstack1l1111lll_opy_:
    if args[1] == bstack11lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬீ") or args[1] == bstack11lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧு"):
      bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧூ")
      args = args[2:]
    elif args[1] == bstack11lll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௃"):
      bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௄")
      args = args[2:]
    elif args[1] == bstack11lll1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௅"):
      bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪெ")
      args = args[2:]
    elif args[1] == bstack11lll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ே"):
      bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧை")
      args = args[2:]
    elif args[1] == bstack11lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ௉"):
      bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨொ")
      args = args[2:]
    elif args[1] == bstack11lll1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩோ"):
      bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪௌ")
      args = args[2:]
    else:
      if not bstack11lll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ்ࠧ") in CONFIG or str(CONFIG[bstack11lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௎")]).lower() in [bstack11lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௏"), bstack11lll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨௐ")]:
        bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௑")
        args = args[1:]
      elif str(CONFIG[bstack11lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௒")]).lower() == bstack11lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௓"):
        bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௔")
        args = args[1:]
      elif str(CONFIG[bstack11lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௕")]).lower() == bstack11lll1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௖"):
        bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ௗ")
        args = args[1:]
      elif str(CONFIG[bstack11lll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௘")]).lower() == bstack11lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௙"):
        bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௚")
        args = args[1:]
      elif str(CONFIG[bstack11lll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ௛")]).lower() == bstack11lll1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௜"):
        bstack1l1111lll_opy_ = bstack11lll1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௝")
        args = args[1:]
      else:
        os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ௞")] = bstack1l1111lll_opy_
        bstack1llll11l1_opy_(bstack1ll1llll11_opy_)
  os.environ[bstack11lll1l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ௟")] = bstack1l1111lll_opy_
  bstack1ll1ll11ll_opy_ = bstack1l1111lll_opy_
  global bstack1l1llll111_opy_
  if bstack1l11l11l_opy_:
    try:
      os.environ[bstack11lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ௠")] = bstack1l1111lll_opy_
      bstack1lllll1ll_opy_(bstack1ll1lll1l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll11l11ll_opy_.format(str(e)))
  global bstack11ll11ll_opy_
  global bstack1111l111_opy_
  global bstack1lll1lll_opy_
  global bstack11ll1l111_opy_
  global bstack1l1l1ll1l_opy_
  global bstack1llll1ll1l_opy_
  global bstack1ll1lll11l_opy_
  global bstack11ll1111l_opy_
  global bstack1llll1l11_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1l1l1111_opy_
  global bstack1lllllll1l_opy_
  global bstack111l1llll_opy_
  global bstack111ll1l11_opy_
  global bstack11ll1l11_opy_
  global bstack1lllll111l_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11l1ll1l_opy_
  global bstack1ll1l1l1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll11ll_opy_ = webdriver.Remote.__init__
    bstack1111l111_opy_ = WebDriver.quit
    bstack1l1l1111_opy_ = WebDriver.close
    bstack111ll1l11_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1llll111_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1llllll1ll_opy_(CONFIG) and bstack1l1l1llll_opy_():
    if bstack1ll1ll11_opy_() < version.parse(bstack1l1lll1l_opy_):
      logger.error(bstack111l1ll11_opy_.format(bstack1ll1ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll1l11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l1l1l1l_opy_.format(str(e)))
  if bstack1l1111lll_opy_ != bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௡") or (bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௢") and not bstack1l11l11l_opy_):
    bstack1l111l111_opy_()
  if (bstack1l1111lll_opy_ in [bstack11lll1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௣"), bstack11lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤"), bstack11lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ௥")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll11ll1l1_opy_
        bstack1l1l1ll1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1llll111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11ll1l111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1111lll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1llll111l_opy_)
    if bstack11lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ௦") in CONFIG:
      os.environ[bstack11lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ௧")] = os.getenv(bstack11lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ௨"), json.dumps(CONFIG[bstack11lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ௩")]))
      CONFIG[bstack11lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ௪")].pop(bstack11lll1l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ௫"), None)
      CONFIG[bstack11lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ௬")].pop(bstack11lll1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭௭"), None)
    if bstack1l11ll1l_opy_ and bstack1111l11ll_opy_.bstack1ll1ll111l_opy_(CONFIG) and bstack1l1111lll_opy_ != bstack11lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௮"):
      bstack1llll1lll_opy_, bstack11l11lll_opy_ = bstack1111l11ll_opy_.bstack1ll111111_opy_(CONFIG, bstack1l1111lll_opy_, bstack1111111l_opy_.version());
      if bstack1l1111lll_opy_ != bstack11lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௯") and not bstack1llll1lll_opy_ is None:
        os.environ[bstack11lll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ௰")] = bstack1llll1lll_opy_;
        os.environ[bstack11lll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡔࡆࡕࡗࡣࡗ࡛ࡎࡠࡋࡇࠫ௱")] = str(bstack11l11lll_opy_);
    if bstack1l1111lll_opy_ != bstack11lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ௲"):
      bstack1lll1l1l1_opy_()
    bstack1lll1lll_opy_ = Output.end_test
    bstack1llll1ll1l_opy_ = TestStatus.__init__
    bstack11ll1111l_opy_ = pabot._run
    bstack1llll1l11_opy_ = QueueItem.__init__
    bstack1ll1l11l1l_opy_ = pabot._create_command_for_execution
    bstack11l1ll1l_opy_ = pabot._report_results
  if bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௳"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1lll11111l_opy_)
    bstack1lllllll1l_opy_ = Runner.run_hook
    bstack111l1llll_opy_ = Step.run
  if bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௴"):
    try:
      bstack111lll111_opy_.launch(CONFIG, {
        bstack11lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ௵"): bstack11lll1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ௶") if bstack1ll1111111_opy_() else bstack11lll1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ௷"),
        bstack11lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ௸"): bstack1111111l_opy_.version(),
        bstack11lll1l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ௹"): __version__
      })
      if bstack1l11ll1l_opy_ and bstack1111l11ll_opy_.bstack1ll1ll111l_opy_(CONFIG):
        bstack1llll1lll_opy_, bstack11l11lll_opy_ = bstack1111l11ll_opy_.bstack1ll111111_opy_(CONFIG, bstack1l1111lll_opy_, bstack1111111l_opy_.version());
        if not bstack1llll1lll_opy_ is None:
          os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ௺")] = bstack1llll1lll_opy_;
          os.environ[bstack11lll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧ௻")] = str(bstack11l11lll_opy_);
      from _pytest.config import Config
      bstack1lllll111l_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll1ll1l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1l11l1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll1l1l1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11lll1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ௼"))
  if bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௽"):
    bstack1l11llll1_opy_ = True
    if bstack1l11l11l_opy_ and bstack11l1ll11_opy_:
      bstack1l1ll11ll_opy_ = CONFIG.get(bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ௾"), {}).get(bstack11lll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௿"))
      bstack1ll1lll1ll_opy_(bstack11l111ll1_opy_)
    elif bstack1l11l11l_opy_:
      bstack1l1ll11ll_opy_ = CONFIG.get(bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪఀ"), {}).get(bstack11lll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఁ"))
      global bstack1lll111ll_opy_
      try:
        if bstack111111l1l_opy_(bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫం")]) and multiprocessing.current_process().name == bstack11lll1l_opy_ (u"ࠩ࠳ࠫః"):
          bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఄ")].remove(bstack11lll1l_opy_ (u"ࠫ࠲ࡳࠧఅ"))
          bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఆ")].remove(bstack11lll1l_opy_ (u"࠭ࡰࡥࡤࠪఇ"))
          bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఈ")] = bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఉ")][0]
          with open(bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఊ")], bstack11lll1l_opy_ (u"ࠪࡶࠬఋ")) as f:
            bstack1llll1l1l_opy_ = f.read()
          bstack1l1ll11l1_opy_ = bstack11lll1l_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣఌ").format(str(bstack1l11l11l_opy_))
          bstack111l1ll1l_opy_ = bstack1l1ll11l1_opy_ + bstack1llll1l1l_opy_
          bstack1ll1l1l111_opy_ = bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఍")] + bstack11lll1l_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨఎ")
          with open(bstack1ll1l1l111_opy_, bstack11lll1l_opy_ (u"ࠧࡸࠩఏ")):
            pass
          with open(bstack1ll1l1l111_opy_, bstack11lll1l_opy_ (u"ࠣࡹ࠮ࠦఐ")) as f:
            f.write(bstack111l1ll1l_opy_)
          import subprocess
          bstack111ll11l1_opy_ = subprocess.run([bstack11lll1l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤ఑"), bstack1ll1l1l111_opy_])
          if os.path.exists(bstack1ll1l1l111_opy_):
            os.unlink(bstack1ll1l1l111_opy_)
          os._exit(bstack111ll11l1_opy_.returncode)
        else:
          if bstack111111l1l_opy_(bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఒ")]):
            bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఓ")].remove(bstack11lll1l_opy_ (u"ࠬ࠳࡭ࠨఔ"))
            bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩక")].remove(bstack11lll1l_opy_ (u"ࠧࡱࡦࡥࠫఖ"))
            bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫగ")] = bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఘ")][0]
          bstack1ll1lll1ll_opy_(bstack11l111ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఙ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11lll1l_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭చ")] = bstack11lll1l_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧఛ")
          mod_globals[bstack11lll1l_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨజ")] = os.path.abspath(bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఝ")])
          exec(open(bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఞ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11lll1l_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩట").format(str(e)))
          for driver in bstack1lll111ll_opy_:
            bstack11l1lll1_opy_.append({
              bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨఠ"): bstack1l11l11l_opy_[bstack11lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧడ")],
              bstack11lll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫఢ"): str(e),
              bstack11lll1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬణ"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧత") + json.dumps(
                bstack11lll1l_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦథ") + str(e)) + bstack11lll1l_opy_ (u"ࠩࢀࢁࠬద"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll111ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1lllll_opy_, CONFIG, logger)
      bstack11lll111l_opy_()
      bstack1l11lllll_opy_()
      bstack1llll1l1ll_opy_ = {
        bstack11lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ధ"): args[0],
        bstack11lll1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫన"): CONFIG,
        bstack11lll1l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭఩"): bstack1lll1l1l_opy_,
        bstack11lll1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨప"): bstack1l1lllll_opy_
      }
      percy.bstack111l111l_opy_()
      if bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఫ") in CONFIG:
        bstack1lll111ll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll11l1l1l_opy_ = manager.list()
        if bstack111111l1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫబ")]):
            if index == 0:
              bstack1llll1l1ll_opy_[bstack11lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬభ")] = args
            bstack1lll111ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll1l1ll_opy_, bstack1ll11l1l1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭మ")]):
            bstack1lll111ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll1l1ll_opy_, bstack1ll11l1l1l_opy_)))
        for t in bstack1lll111ll1_opy_:
          t.start()
        for t in bstack1lll111ll1_opy_:
          t.join()
        bstack1ll1l11lll_opy_ = list(bstack1ll11l1l1l_opy_)
      else:
        if bstack111111l1l_opy_(args):
          bstack1llll1l1ll_opy_[bstack11lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧయ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1llll1l1ll_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1lll1ll_opy_(bstack11l111ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11lll1l_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧర")] = bstack11lll1l_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨఱ")
          mod_globals[bstack11lll1l_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩల")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧళ") or bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨఴ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1llll111l_opy_)
    bstack11lll111l_opy_()
    bstack1ll1lll1ll_opy_(bstack1ll1l1l1l_opy_)
    if bstack11lll1l_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨవ") in args:
      i = args.index(bstack11lll1l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩశ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l11111l_opy_))
    args.insert(0, str(bstack11lll1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪష")))
    pabot.main(args)
  elif bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧస"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1llll111l_opy_)
    for a in args:
      if bstack11lll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭హ") in a:
        bstack1l11ll1ll_opy_ = int(a.split(bstack11lll1l_opy_ (u"ࠨ࠼ࠪ఺"))[1])
      if bstack11lll1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭఻") in a:
        bstack1l1ll11ll_opy_ = str(a.split(bstack11lll1l_opy_ (u"ࠪ࠾఼ࠬ"))[1])
      if bstack11lll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫఽ") in a:
        bstack1l1ll1l1l_opy_ = str(a.split(bstack11lll1l_opy_ (u"ࠬࡀࠧా"))[1])
    bstack11111l111_opy_ = None
    if bstack11lll1l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬి") in args:
      i = args.index(bstack11lll1l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ీ"))
      args.pop(i)
      bstack11111l111_opy_ = args.pop(i)
    if bstack11111l111_opy_ is not None:
      global bstack1lllllll11_opy_
      bstack1lllllll11_opy_ = bstack11111l111_opy_
    bstack1ll1lll1ll_opy_(bstack1ll1l1l1l_opy_)
    run_cli(args)
    if bstack11lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬు") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1lllll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11l1lll1_opy_.append(bstack1ll1lllll_opy_)
  elif bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩూ"):
    bstack1ll11lllll_opy_ = bstack1111111l_opy_(args, logger, CONFIG, bstack1l11ll1l_opy_)
    bstack1ll11lllll_opy_.bstack1lll111l1_opy_()
    bstack11lll111l_opy_()
    bstack1l1111l11_opy_ = True
    bstack11lll1l1l_opy_ = bstack1ll11lllll_opy_.bstack1111l11l_opy_()
    bstack1ll11lllll_opy_.bstack1llll1l1ll_opy_(bstack1l11l111l_opy_)
    bstack1llll1llll_opy_ = bstack1ll11lllll_opy_.bstack1ll111ll1_opy_(bstack1111lll1l_opy_, {
      bstack11lll1l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫృ"): bstack1lll1l1l_opy_,
      bstack11lll1l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ౄ"): bstack1l1lllll_opy_,
      bstack11lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ౅"): bstack1l11ll1l_opy_
    })
    bstack1llllll11l_opy_ = 1 if len(bstack1llll1llll_opy_) > 0 else 0
  elif bstack1l1111lll_opy_ == bstack11lll1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ె"):
    try:
      from behave.__main__ import main as bstack1ll1l1ll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1lll1lll_opy_(e, bstack1lll11111l_opy_)
    bstack11lll111l_opy_()
    bstack1l1111l11_opy_ = True
    bstack11111ll11_opy_ = 1
    if bstack11lll1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧే") in CONFIG:
      bstack11111ll11_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨై")]
    bstack111ll1l1l_opy_ = int(bstack11111ll11_opy_) * int(len(CONFIG[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౉")]))
    config = Configuration(args)
    bstack1ll1l11ll1_opy_ = config.paths
    if len(bstack1ll1l11ll1_opy_) == 0:
      import glob
      pattern = bstack11lll1l_opy_ (u"ࠪ࠮࠯࠵ࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠩొ")
      bstack11l11llll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11l11llll_opy_)
      config = Configuration(args)
      bstack1ll1l11ll1_opy_ = config.paths
    bstack1ll1l111l_opy_ = [os.path.normpath(item) for item in bstack1ll1l11ll1_opy_]
    bstack1ll111l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1ll1ll_opy_ = [item for item in bstack1ll111l1_opy_ if item not in bstack1ll1l111l_opy_]
    import platform as pf
    if pf.system().lower() == bstack11lll1l_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬో"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1l111l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111ll111_opy_)))
                    for bstack1111ll111_opy_ in bstack1ll1l111l_opy_]
    bstack111111111_opy_ = []
    for spec in bstack1ll1l111l_opy_:
      bstack1lllll1l1_opy_ = []
      bstack1lllll1l1_opy_ += bstack1l1ll1ll_opy_
      bstack1lllll1l1_opy_.append(spec)
      bstack111111111_opy_.append(bstack1lllll1l1_opy_)
    execution_items = []
    for bstack1lllll1l1_opy_ in bstack111111111_opy_:
      for index, _ in enumerate(CONFIG[bstack11lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౌ")]):
        item = {}
        item[bstack11lll1l_opy_ (u"࠭ࡡࡳࡩ్ࠪ")] = bstack11lll1l_opy_ (u"ࠧࠡࠩ౎").join(bstack1lllll1l1_opy_)
        item[bstack11lll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ౏")] = index
        execution_items.append(item)
    bstack1lll1ll1ll_opy_ = bstack1lll1l1l1l_opy_(execution_items, bstack111ll1l1l_opy_)
    for execution_item in bstack1lll1ll1ll_opy_:
      bstack1lll111ll1_opy_ = []
      for item in execution_item:
        bstack1lll111ll1_opy_.append(bstack1lll1l111l_opy_(name=str(item[bstack11lll1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ౐")]),
                                             target=bstack11ll1l1l_opy_,
                                             args=(item[bstack11lll1l_opy_ (u"ࠪࡥࡷ࡭ࠧ౑")],)))
      for t in bstack1lll111ll1_opy_:
        t.start()
      for t in bstack1lll111ll1_opy_:
        t.join()
  else:
    bstack1llll11l1_opy_(bstack1ll1llll11_opy_)
  if not bstack1l11l11l_opy_:
    bstack1llll111_opy_()
def browserstack_initialize(bstack1ll11ll1l_opy_=None):
  run_on_browserstack(bstack1ll11ll1l_opy_, None, True)
def bstack1llll111_opy_():
  global CONFIG
  global bstack1ll1ll11ll_opy_
  global bstack1llllll11l_opy_
  bstack111lll111_opy_.stop()
  bstack111lll111_opy_.bstack1l1ll1111_opy_()
  if bstack1111l11ll_opy_.bstack1ll1ll111l_opy_(CONFIG):
    bstack1111l11ll_opy_.bstack1111l1l1_opy_()
  [bstack111lllll1_opy_, bstack111l1l1ll_opy_] = bstack1ll1ll1111_opy_()
  if bstack111lllll1_opy_ is not None and bstack1l11lll1_opy_() != -1:
    sessions = bstack1l11ll11_opy_(bstack111lllll1_opy_)
    bstack1l111111l_opy_(sessions, bstack111l1l1ll_opy_)
  if bstack1ll1ll11ll_opy_ == bstack11lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ౒") and bstack1llllll11l_opy_ != 0:
    sys.exit(bstack1llllll11l_opy_)
def bstack1l1ll1l11_opy_(bstack111l11ll_opy_):
  if bstack111l11ll_opy_:
    return bstack111l11ll_opy_.capitalize()
  else:
    return bstack111l11ll_opy_
def bstack1ll1llll1_opy_(bstack1l1l1l11_opy_):
  if bstack11lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౓") in bstack1l1l1l11_opy_ and bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౔")] != bstack11lll1l_opy_ (u"ࠧࠨౕ"):
    return bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠨࡰࡤࡱࡪౖ࠭")]
  else:
    bstack1l1l11ll1_opy_ = bstack11lll1l_opy_ (u"ࠤࠥ౗")
    if bstack11lll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪౘ") in bstack1l1l1l11_opy_ and bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫౙ")] != None:
      bstack1l1l11ll1_opy_ += bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬౚ")] + bstack11lll1l_opy_ (u"ࠨࠬࠡࠤ౛")
      if bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠧࡰࡵࠪ౜")] == bstack11lll1l_opy_ (u"ࠣ࡫ࡲࡷࠧౝ"):
        bstack1l1l11ll1_opy_ += bstack11lll1l_opy_ (u"ࠤ࡬ࡓࡘࠦࠢ౞")
      bstack1l1l11ll1_opy_ += (bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ౟")] or bstack11lll1l_opy_ (u"ࠫࠬౠ"))
      return bstack1l1l11ll1_opy_
    else:
      bstack1l1l11ll1_opy_ += bstack1l1ll1l11_opy_(bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ౡ")]) + bstack11lll1l_opy_ (u"ࠨࠠࠣౢ") + (
              bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩౣ")] or bstack11lll1l_opy_ (u"ࠨࠩ౤")) + bstack11lll1l_opy_ (u"ࠤ࠯ࠤࠧ౥")
      if bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"ࠪࡳࡸ࠭౦")] == bstack11lll1l_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧ౧"):
        bstack1l1l11ll1_opy_ += bstack11lll1l_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥ౨")
      bstack1l1l11ll1_opy_ += bstack1l1l1l11_opy_[bstack11lll1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ౩")] or bstack11lll1l_opy_ (u"ࠧࠨ౪")
      return bstack1l1l11ll1_opy_
def bstack11ll11l11_opy_(bstack1l1llll1ll_opy_):
  if bstack1l1llll1ll_opy_ == bstack11lll1l_opy_ (u"ࠣࡦࡲࡲࡪࠨ౫"):
    return bstack11lll1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౬")
  elif bstack1l1llll1ll_opy_ == bstack11lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ౭"):
    return bstack11lll1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ౮")
  elif bstack1l1llll1ll_opy_ == bstack11lll1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ౯"):
    return bstack11lll1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౰")
  elif bstack1l1llll1ll_opy_ == bstack11lll1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ౱"):
    return bstack11lll1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ౲")
  elif bstack1l1llll1ll_opy_ == bstack11lll1l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ౳"):
    return bstack11lll1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ౴")
  elif bstack1l1llll1ll_opy_ == bstack11lll1l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧ౵"):
    return bstack11lll1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౶")
  else:
    return bstack11lll1l_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪ౷") + bstack1l1ll1l11_opy_(
      bstack1l1llll1ll_opy_) + bstack11lll1l_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౸")
def bstack111l1l111_opy_(session):
  return bstack11lll1l_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨ౹").format(
    session[bstack11lll1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭౺")], bstack1ll1llll1_opy_(session), bstack11ll11l11_opy_(session[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩ౻")]),
    bstack11ll11l11_opy_(session[bstack11lll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ౼")]),
    bstack1l1ll1l11_opy_(session[bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭౽")] or session[bstack11lll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭౾")] or bstack11lll1l_opy_ (u"ࠧࠨ౿")) + bstack11lll1l_opy_ (u"ࠣࠢࠥಀ") + (session[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫಁ")] or bstack11lll1l_opy_ (u"ࠪࠫಂ")),
    session[bstack11lll1l_opy_ (u"ࠫࡴࡹࠧಃ")] + bstack11lll1l_opy_ (u"ࠧࠦࠢ಄") + session[bstack11lll1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪಅ")], session[bstack11lll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩಆ")] or bstack11lll1l_opy_ (u"ࠨࠩಇ"),
    session[bstack11lll1l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ಈ")] if session[bstack11lll1l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧಉ")] else bstack11lll1l_opy_ (u"ࠫࠬಊ"))
def bstack1l111111l_opy_(sessions, bstack111l1l1ll_opy_):
  try:
    bstack11111ll1_opy_ = bstack11lll1l_opy_ (u"ࠧࠨಋ")
    if not os.path.exists(bstack1l1l1l11l_opy_):
      os.mkdir(bstack1l1l1l11l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lll1l_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫಌ")), bstack11lll1l_opy_ (u"ࠧࡳࠩ಍")) as f:
      bstack11111ll1_opy_ = f.read()
    bstack11111ll1_opy_ = bstack11111ll1_opy_.replace(bstack11lll1l_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬಎ"), str(len(sessions)))
    bstack11111ll1_opy_ = bstack11111ll1_opy_.replace(bstack11lll1l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩಏ"), bstack111l1l1ll_opy_)
    bstack11111ll1_opy_ = bstack11111ll1_opy_.replace(bstack11lll1l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫಐ"),
                                              sessions[0].get(bstack11lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨ಑")) if sessions[0] else bstack11lll1l_opy_ (u"ࠬ࠭ಒ"))
    with open(os.path.join(bstack1l1l1l11l_opy_, bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪಓ")), bstack11lll1l_opy_ (u"ࠧࡸࠩಔ")) as stream:
      stream.write(bstack11111ll1_opy_.split(bstack11lll1l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬಕ"))[0])
      for session in sessions:
        stream.write(bstack111l1l111_opy_(session))
      stream.write(bstack11111ll1_opy_.split(bstack11lll1l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ಖ"))[1])
    logger.info(bstack11lll1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭ಗ").format(bstack1l1l1l11l_opy_));
  except Exception as e:
    logger.debug(bstack1ll111llll_opy_.format(str(e)))
def bstack1l11ll11_opy_(bstack111lllll1_opy_):
  global CONFIG
  try:
    host = bstack11lll1l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧಘ") if bstack11lll1l_opy_ (u"ࠬࡧࡰࡱࠩಙ") in CONFIG else bstack11lll1l_opy_ (u"࠭ࡡࡱ࡫ࠪಚ")
    user = CONFIG[bstack11lll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩಛ")]
    key = CONFIG[bstack11lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಜ")]
    bstack1llll1ll11_opy_ = bstack11lll1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨಝ") if bstack11lll1l_opy_ (u"ࠪࡥࡵࡶࠧಞ") in CONFIG else bstack11lll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ಟ")
    url = bstack11lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪಠ").format(user, key, host, bstack1llll1ll11_opy_,
                                                                                bstack111lllll1_opy_)
    headers = {
      bstack11lll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬಡ"): bstack11lll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪಢ"),
    }
    proxies = bstack11lll1111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11lll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ಣ")], response.json()))
  except Exception as e:
    logger.debug(bstack11l111111_opy_.format(str(e)))
def bstack1ll1ll1111_opy_():
  global CONFIG
  global bstack1ll1ll1lll_opy_
  try:
    if bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬತ") in CONFIG:
      host = bstack11lll1l_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ಥ") if bstack11lll1l_opy_ (u"ࠫࡦࡶࡰࠨದ") in CONFIG else bstack11lll1l_opy_ (u"ࠬࡧࡰࡪࠩಧ")
      user = CONFIG[bstack11lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨನ")]
      key = CONFIG[bstack11lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ಩")]
      bstack1llll1ll11_opy_ = bstack11lll1l_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧಪ") if bstack11lll1l_opy_ (u"ࠩࡤࡴࡵ࠭ಫ") in CONFIG else bstack11lll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬಬ")
      url = bstack11lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫಭ").format(user, key, host, bstack1llll1ll11_opy_)
      headers = {
        bstack11lll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫಮ"): bstack11lll1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩಯ"),
      }
      if bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩರ") in CONFIG:
        params = {bstack11lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಱ"): CONFIG[bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬಲ")], bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ಳ"): CONFIG[bstack11lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭಴")]}
      else:
        params = {bstack11lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪವ"): CONFIG[bstack11lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩಶ")]}
      proxies = bstack11lll1111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11111111_opy_ = response.json()[0][bstack11lll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪಷ")]
        if bstack11111111_opy_:
          bstack111l1l1ll_opy_ = bstack11111111_opy_[bstack11lll1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬಸ")].split(bstack11lll1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨಹ"))[0] + bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫ಺") + bstack11111111_opy_[
            bstack11lll1l_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ಻")]
          logger.info(bstack1lll1ll1l_opy_.format(bstack111l1l1ll_opy_))
          bstack1ll1ll1lll_opy_ = bstack11111111_opy_[bstack11lll1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ಼")]
          bstack1ll11lll1l_opy_ = CONFIG[bstack11lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩಽ")]
          if bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩಾ") in CONFIG:
            bstack1ll11lll1l_opy_ += bstack11lll1l_opy_ (u"ࠨࠢࠪಿ") + CONFIG[bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫೀ")]
          if bstack1ll11lll1l_opy_ != bstack11111111_opy_[bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨು")]:
            logger.debug(bstack1l1111111_opy_.format(bstack11111111_opy_[bstack11lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩೂ")], bstack1ll11lll1l_opy_))
          return [bstack11111111_opy_[bstack11lll1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨೃ")], bstack111l1l1ll_opy_]
    else:
      logger.warn(bstack11l1l11ll_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l1111_opy_.format(str(e)))
  return [None, None]
def bstack11l11ll11_opy_(url, bstack1l111ll1l_opy_=False):
  global CONFIG
  global bstack1ll1lll11_opy_
  if not bstack1ll1lll11_opy_:
    hostname = bstack1ll1111ll1_opy_(url)
    is_private = bstack111lllll_opy_(hostname)
    if (bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪೄ") in CONFIG and not CONFIG[bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ೅")]) and (is_private or bstack1l111ll1l_opy_):
      bstack1ll1lll11_opy_ = hostname
def bstack1ll1111ll1_opy_(url):
  return urlparse(url).hostname
def bstack111lllll_opy_(hostname):
  for bstack1ll111l1ll_opy_ in bstack1111ll1l1_opy_:
    regex = re.compile(bstack1ll111l1ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1lll11llll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l11ll1ll_opy_
  if not bstack1111l11ll_opy_.bstack1l11111ll_opy_(CONFIG, bstack1l11ll1ll_opy_):
    logger.warning(bstack11lll1l_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦೆ"))
    return {}
  try:
    results = driver.execute_script(bstack11lll1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡀࠤࡳ࡫ࡷࠡࡅࡸࡷࡹࡵ࡭ࡆࡸࡨࡲࡹ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡊࡉ࡙ࡥࡒࡆࡕࡘࡐ࡙࡙ࠧࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡴࠠ࠾ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࡫ࡶࡦࡰࡷ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡲࡦ࡯ࡲࡺࡪࡋࡶࡦࡰࡷࡐ࡮ࡹࡴࡦࡰࡨࡶ࠭࠭ࡁ࠲࠳࡜ࡣࡗࡋࡓࡖࡎࡗࡗࡤࡘࡅࡔࡒࡒࡒࡘࡋࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡵࡲࡰࡻ࡫ࠨࡦࡸࡨࡲࡹ࠴ࡤࡦࡶࡤ࡭ࡱ࠴ࡤࡢࡶࡤ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡡࡥࡦࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࡷࡧࡱࡸ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠠࡤࡣࡷࡧ࡭ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡰࡥࡤࡶࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠤࠥࠦೇ"))
    return results
  except Exception:
    logger.error(bstack11lll1l_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧೈ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l11ll1ll_opy_
  if not bstack1111l11ll_opy_.bstack1l11111ll_opy_(CONFIG, bstack1l11ll1ll_opy_):
    logger.warning(bstack11lll1l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣ೉"))
    return {}
  try:
    bstack1ll11ll1ll_opy_ = driver.execute_script(bstack11lll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࡷࡧࡱࡸࠥࡃࠠ࡯ࡧࡺࠤࡈࡻࡳࡵࡱࡰࡉࡻ࡫࡮ࡵࠪࠪࡅ࠶࠷࡙ࡠࡖࡄࡔࡤࡍࡅࡕࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡗ࡚ࡓࡍࡂࡔ࡜ࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡨࡱࠤࡂࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪࡨࡺࡪࡴࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡶࡪࡳ࡯ࡷࡧࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡰ࡮ࡹࡩ࠭࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠲ࡸࡻ࡭࡮ࡣࡵࡽ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡢࡦࡧࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡗ࡚ࡓࡍࡂࡔ࡜ࡣࡗࡋࡓࡑࡑࡑࡗࡊ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࡹࡩࡳࡺࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠢࡦࡥࡹࡩࡨࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥ࡫ࡧࡦࡸ࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠦࠧࠨೊ"))
    return bstack1ll11ll1ll_opy_
  except Exception:
    logger.error(bstack11lll1l_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢೋ"))
    return {}