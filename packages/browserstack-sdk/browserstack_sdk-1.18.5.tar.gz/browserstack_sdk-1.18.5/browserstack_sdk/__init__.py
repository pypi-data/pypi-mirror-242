# coding: UTF-8
import sys
bstack1111l_opy_ = sys.version_info [0] == 2
bstack1ll11ll_opy_ = 2048
bstack1lll_opy_ = 7
def bstack1111_opy_ (bstack11l111l_opy_):
    global bstack1l1l11l_opy_
    bstack1lll1l1_opy_ = ord (bstack11l111l_opy_ [-1])
    bstack1ll1ll_opy_ = bstack11l111l_opy_ [:-1]
    bstack111111l_opy_ = bstack1lll1l1_opy_ % len (bstack1ll1ll_opy_)
    bstack11l111_opy_ = bstack1ll1ll_opy_ [:bstack111111l_opy_] + bstack1ll1ll_opy_ [bstack111111l_opy_:]
    if bstack1111l_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11ll_opy_ - (bstack1l1l1ll_opy_ + bstack1lll1l1_opy_) % bstack1lll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11l111_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11ll_opy_ - (bstack1l1l1ll_opy_ + bstack1lll1l1_opy_) % bstack1lll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11l111_opy_)])
    return eval (bstack1l_opy_)
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
def bstack1lll111l_opy_():
  global CONFIG
  headers = {
        bstack1111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡵ"): bstack1111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡶ"),
      }
  proxies = bstack1l1llll11_opy_(CONFIG, bstack1ll111l1l1_opy_)
  try:
    response = requests.get(bstack1ll111l1l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1lllll11_opy_ = response.json()[bstack1111_opy_ (u"ࠫ࡭ࡻࡢࡴࠩࡷ")]
      logger.debug(bstack1ll11l111l_opy_.format(response.json()))
      return bstack1l1lllll11_opy_
    else:
      logger.debug(bstack1llllllll_opy_.format(bstack1111_opy_ (u"ࠧࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡋࡕࡒࡒࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴࠣࠦࡸ")))
  except Exception as e:
    logger.debug(bstack1llllllll_opy_.format(e))
def bstack1llllllll1_opy_(hub_url):
  global CONFIG
  url = bstack1111_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣࡹ")+  hub_url + bstack1111_opy_ (u"ࠢ࠰ࡥ࡫ࡩࡨࡱࠢࡺ")
  headers = {
        bstack1111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧࡻ"): bstack1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬࡼ"),
      }
  proxies = bstack1l1llll11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1111llll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1l11ll_opy_.format(hub_url, e))
def bstack111lll11l_opy_():
  try:
    global bstack11l11l11l_opy_
    bstack1l1lllll11_opy_ = bstack1lll111l_opy_()
    bstack1l1ll1ll_opy_ = []
    results = []
    for bstack1l11111l_opy_ in bstack1l1lllll11_opy_:
      bstack1l1ll1ll_opy_.append(bstack1ll111111l_opy_(target=bstack1llllllll1_opy_,args=(bstack1l11111l_opy_,)))
    for t in bstack1l1ll1ll_opy_:
      t.start()
    for t in bstack1l1ll1ll_opy_:
      results.append(t.join())
    bstack1lll1ll111_opy_ = {}
    for item in results:
      hub_url = item[bstack1111_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫࡽ")]
      latency = item[bstack1111_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬࡾ")]
      bstack1lll1ll111_opy_[hub_url] = latency
    bstack1l111l1l1_opy_ = min(bstack1lll1ll111_opy_, key= lambda x: bstack1lll1ll111_opy_[x])
    bstack11l11l11l_opy_ = bstack1l111l1l1_opy_
    logger.debug(bstack1111lll1_opy_.format(bstack1l111l1l1_opy_))
  except Exception as e:
    logger.debug(bstack1lll1l11l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1ll1111l_opy_, bstack1ll11l11_opy_, bstack1ll111l111_opy_, bstack1l111lll1_opy_, Notset, bstack1lll11l1_opy_, \
  bstack1ll111l1l_opy_, bstack111ll11ll_opy_, bstack1ll1l1l11_opy_, bstack1111lll11_opy_, bstack111l1ll11_opy_, bstack1111ll111_opy_, bstack1l11llll_opy_, \
  bstack11l1l111_opy_, bstack1llll1l1_opy_, bstack1l11ll111_opy_, bstack1l111l11l_opy_, bstack11l1ll11l_opy_, bstack1l11l111_opy_
from bstack_utils.bstack11l11ll1_opy_ import bstack1l1lll11l_opy_
from bstack_utils.proxy import bstack111llllll_opy_, bstack1l1llll11_opy_, bstack111ll1111_opy_, bstack1l1l11ll1_opy_
import bstack_utils.bstack1l1ll1l1_opy_ as bstack111ll1l1l_opy_
from browserstack_sdk.bstack1l1l1l1ll_opy_ import *
from browserstack_sdk.bstack1l1l1lll1_opy_ import *
from bstack_utils.bstack1l1llllll1_opy_ import bstack111l11ll1_opy_
bstack111lll1l_opy_ = bstack1111_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬࡿ")
bstack11ll11l1l_opy_ = bstack1111_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࢀ")
from ._version import __version__
bstack1lllllll1_opy_ = None
CONFIG = {}
bstack1lll111l11_opy_ = {}
bstack1ll11lll1l_opy_ = {}
bstack1lll1ll1_opy_ = None
bstack11l111111_opy_ = None
bstack1ll111lll_opy_ = None
bstack1llll11111_opy_ = -1
bstack1ll11lll1_opy_ = 0
bstack1lll11l11_opy_ = bstack11l111l1l_opy_
bstack1lll11111l_opy_ = 1
bstack1lll1l1l1_opy_ = False
bstack11ll11111_opy_ = False
bstack1lll1l1ll_opy_ = bstack1111_opy_ (u"ࠧࠨࢁ")
bstack1ll1ll1l11_opy_ = bstack1111_opy_ (u"ࠨࠩࢂ")
bstack11llll11_opy_ = False
bstack11111llll_opy_ = True
bstack1l111l11_opy_ = bstack1111_opy_ (u"ࠩࠪࢃ")
bstack11lll1111_opy_ = []
bstack11l11l11l_opy_ = bstack1111_opy_ (u"ࠪࠫࢄ")
bstack1lll111l1l_opy_ = False
bstack1l1l1lll_opy_ = None
bstack1ll1111111_opy_ = None
bstack1llll1lll_opy_ = -1
bstack11lll111l_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠫࢃ࠭ࢅ")), bstack1111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࢆ"), bstack1111_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫࢇ"))
bstack1ll1lll1l_opy_ = 0
bstack1ll1ll1ll_opy_ = []
bstack1ll1llllll_opy_ = []
bstack1l11ll1l_opy_ = []
bstack111ll1lll_opy_ = []
bstack1lllllllll_opy_ = bstack1111_opy_ (u"ࠧࠨ࢈")
bstack1l1ll111l_opy_ = bstack1111_opy_ (u"ࠨࠩࢉ")
bstack1ll1lll11_opy_ = False
bstack1l1ll111_opy_ = False
bstack1l1ll1l11_opy_ = None
bstack1ll1l1l1l_opy_ = None
bstack1ll11l1l_opy_ = None
bstack11l111l11_opy_ = None
bstack1l1l1ll11_opy_ = None
bstack1lll11lll_opy_ = None
bstack1ll11ll111_opy_ = None
bstack11lll11l1_opy_ = None
bstack11llll1l1_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack1ll11l1ll_opy_ = None
bstack11l1111l1_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack1l1l1111_opy_ = None
bstack1111l11l_opy_ = None
bstack111llll11_opy_ = None
bstack1l1l11l11_opy_ = None
bstack11111l11_opy_ = None
bstack111l1lll_opy_ = bstack1111_opy_ (u"ࠤࠥࢊ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lll11l11_opy_,
                    format=bstack1111_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨࢋ"),
                    datefmt=bstack1111_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ࢌ"),
                    stream=sys.stdout)
bstack1llll1l1ll_opy_ = Config.get_instance()
percy = bstack1llll111ll_opy_()
def bstack111l111ll_opy_():
  global CONFIG
  global bstack1lll11l11_opy_
  if bstack1111_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࢍ") in CONFIG:
    bstack1lll11l11_opy_ = bstack1ll1l1l11l_opy_[CONFIG[bstack1111_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ")]]
    logging.getLogger().setLevel(bstack1lll11l11_opy_)
def bstack1111l1111_opy_():
  global CONFIG
  global bstack1ll1lll11_opy_
  bstack1ll1lll1ll_opy_ = bstack1l1lll1lll_opy_(CONFIG)
  if (bstack1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ࢏") in bstack1ll1lll1ll_opy_ and str(bstack1ll1lll1ll_opy_[bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐")]).lower() == bstack1111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ࢑")):
    bstack1ll1lll11_opy_ = True
def bstack11l1l1lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1llll1ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1111lllll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1111_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡧࡴࡴࡦࡪࡩࡩ࡭ࡱ࡫ࠢ࢒") == args[i].lower() or bstack1111_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡨ࡬࡫ࠧ࢓") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l111l11_opy_
      bstack1l111l11_opy_ += bstack1111_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࡋ࡯࡬ࡦࠢࠪ࢔") + path
      return path
  return None
bstack1ll1lllll_opy_ = re.compile(bstack1111_opy_ (u"ࡸࠢ࠯ࠬࡂࡠࠩࢁࠨ࠯ࠬࡂ࠭ࢂ࠴ࠪࡀࠤ࢕"))
def bstack1lll111111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll1lllll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1111_opy_ (u"ࠢࠥࡽࠥ࢖") + group + bstack1111_opy_ (u"ࠣࡿࠥࢗ"), os.environ.get(group))
  return value
def bstack11111ll1l_opy_():
  bstack1lll1llll1_opy_ = bstack1111lllll_opy_()
  if bstack1lll1llll1_opy_ and os.path.exists(os.path.abspath(bstack1lll1llll1_opy_)):
    fileName = bstack1lll1llll1_opy_
  if bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭࢘") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")])) and not bstack1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    fileName = os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")]
  if bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    bstack1l11l_opy_ = os.path.abspath(fileName)
  else:
    bstack1l11l_opy_ = bstack1111_opy_ (u"ࠧࠨ࢝")
  bstack11lllll11_opy_ = os.getcwd()
  bstack1ll111ll_opy_ = bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ࢞")
  bstack11111lll1_opy_ = bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭࢟")
  while (not os.path.exists(bstack1l11l_opy_)) and bstack11lllll11_opy_ != bstack1111_opy_ (u"ࠥࠦࢠ"):
    bstack1l11l_opy_ = os.path.join(bstack11lllll11_opy_, bstack1ll111ll_opy_)
    if not os.path.exists(bstack1l11l_opy_):
      bstack1l11l_opy_ = os.path.join(bstack11lllll11_opy_, bstack11111lll1_opy_)
    if bstack11lllll11_opy_ != os.path.dirname(bstack11lllll11_opy_):
      bstack11lllll11_opy_ = os.path.dirname(bstack11lllll11_opy_)
    else:
      bstack11lllll11_opy_ = bstack1111_opy_ (u"ࠦࠧࢡ")
  if not os.path.exists(bstack1l11l_opy_):
    bstack11llll111_opy_(
      bstack11lll1l1_opy_.format(os.getcwd()))
  try:
    with open(bstack1l11l_opy_, bstack1111_opy_ (u"ࠬࡸࠧࢢ")) as stream:
      yaml.add_implicit_resolver(bstack1111_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࢣ"), bstack1ll1lllll_opy_)
      yaml.add_constructor(bstack1111_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣࢤ"), bstack1lll111111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l11l_opy_, bstack1111_opy_ (u"ࠨࡴࠪࢥ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11llll111_opy_(bstack11ll1llll_opy_.format(str(exc)))
def bstack111ll11l_opy_(config):
  bstack11l1lll11_opy_ = bstack1l1llll11l_opy_(config)
  for option in list(bstack11l1lll11_opy_):
    if option.lower() in bstack1l111l1l_opy_ and option != bstack1l111l1l_opy_[option.lower()]:
      bstack11l1lll11_opy_[bstack1l111l1l_opy_[option.lower()]] = bstack11l1lll11_opy_[option]
      del bstack11l1lll11_opy_[option]
  return config
def bstack1ll1l11ll1_opy_():
  global bstack1ll11lll1l_opy_
  for key, bstack1llllll11l_opy_ in bstack1ll11l11l1_opy_.items():
    if isinstance(bstack1llllll11l_opy_, list):
      for var in bstack1llllll11l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll11lll1l_opy_[key] = os.environ[var]
          break
    elif bstack1llllll11l_opy_ in os.environ and os.environ[bstack1llllll11l_opy_] and str(os.environ[bstack1llllll11l_opy_]).strip():
      bstack1ll11lll1l_opy_[key] = os.environ[bstack1llllll11l_opy_]
  if bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫࢦ") in os.environ:
    bstack1ll11lll1l_opy_[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢧ")] = {}
    bstack1ll11lll1l_opy_[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢨ")][bstack1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢩ")] = os.environ[bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨࢪ")]
def bstack1lll1lllll_opy_():
  global bstack1lll111l11_opy_
  global bstack1l111l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1111_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢫ").lower() == val.lower():
      bstack1lll111l11_opy_[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢬ")] = {}
      bstack1lll111l11_opy_[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢭ")][bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢮ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l1llll1ll_opy_ in bstack11ll1111l_opy_.items():
    if isinstance(bstack1l1llll1ll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1llll1ll_opy_:
          if idx < len(sys.argv) and bstack1111_opy_ (u"ࠫ࠲࠳ࠧࢯ") + var.lower() == val.lower() and not key in bstack1lll111l11_opy_:
            bstack1lll111l11_opy_[key] = sys.argv[idx + 1]
            bstack1l111l11_opy_ += bstack1111_opy_ (u"ࠬࠦ࠭࠮ࠩࢰ") + var + bstack1111_opy_ (u"࠭ࠠࠨࢱ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1111_opy_ (u"ࠧ࠮࠯ࠪࢲ") + bstack1l1llll1ll_opy_.lower() == val.lower() and not key in bstack1lll111l11_opy_:
          bstack1lll111l11_opy_[key] = sys.argv[idx + 1]
          bstack1l111l11_opy_ += bstack1111_opy_ (u"ࠨࠢ࠰࠱ࠬࢳ") + bstack1l1llll1ll_opy_ + bstack1111_opy_ (u"ࠩࠣࠫࢴ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11lllll1_opy_(config):
  bstack111111l11_opy_ = config.keys()
  for bstack1ll1l11l1_opy_, bstack1lll11ll1_opy_ in bstack1ll11ll1l_opy_.items():
    if bstack1lll11ll1_opy_ in bstack111111l11_opy_:
      config[bstack1ll1l11l1_opy_] = config[bstack1lll11ll1_opy_]
      del config[bstack1lll11ll1_opy_]
  for bstack1ll1l11l1_opy_, bstack1lll11ll1_opy_ in bstack1lll1ll1ll_opy_.items():
    if isinstance(bstack1lll11ll1_opy_, list):
      for bstack11l111ll_opy_ in bstack1lll11ll1_opy_:
        if bstack11l111ll_opy_ in bstack111111l11_opy_:
          config[bstack1ll1l11l1_opy_] = config[bstack11l111ll_opy_]
          del config[bstack11l111ll_opy_]
          break
    elif bstack1lll11ll1_opy_ in bstack111111l11_opy_:
      config[bstack1ll1l11l1_opy_] = config[bstack1lll11ll1_opy_]
      del config[bstack1lll11ll1_opy_]
  for bstack11l111ll_opy_ in list(config):
    for bstack1l1111l11_opy_ in bstack1l11ll11l_opy_:
      if bstack11l111ll_opy_.lower() == bstack1l1111l11_opy_.lower() and bstack11l111ll_opy_ != bstack1l1111l11_opy_:
        config[bstack1l1111l11_opy_] = config[bstack11l111ll_opy_]
        del config[bstack11l111ll_opy_]
  bstack1ll11l11l_opy_ = []
  if bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ") in config:
    bstack1ll11l11l_opy_ = config[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࢶ")]
  for platform in bstack1ll11l11l_opy_:
    for bstack11l111ll_opy_ in list(platform):
      for bstack1l1111l11_opy_ in bstack1l11ll11l_opy_:
        if bstack11l111ll_opy_.lower() == bstack1l1111l11_opy_.lower() and bstack11l111ll_opy_ != bstack1l1111l11_opy_:
          platform[bstack1l1111l11_opy_] = platform[bstack11l111ll_opy_]
          del platform[bstack11l111ll_opy_]
  for bstack1ll1l11l1_opy_, bstack1lll11ll1_opy_ in bstack1lll1ll1ll_opy_.items():
    for platform in bstack1ll11l11l_opy_:
      if isinstance(bstack1lll11ll1_opy_, list):
        for bstack11l111ll_opy_ in bstack1lll11ll1_opy_:
          if bstack11l111ll_opy_ in platform:
            platform[bstack1ll1l11l1_opy_] = platform[bstack11l111ll_opy_]
            del platform[bstack11l111ll_opy_]
            break
      elif bstack1lll11ll1_opy_ in platform:
        platform[bstack1ll1l11l1_opy_] = platform[bstack1lll11ll1_opy_]
        del platform[bstack1lll11ll1_opy_]
  for bstack1llll1llll_opy_ in bstack1lll1l1l_opy_:
    if bstack1llll1llll_opy_ in config:
      if not bstack1lll1l1l_opy_[bstack1llll1llll_opy_] in config:
        config[bstack1lll1l1l_opy_[bstack1llll1llll_opy_]] = {}
      config[bstack1lll1l1l_opy_[bstack1llll1llll_opy_]].update(config[bstack1llll1llll_opy_])
      del config[bstack1llll1llll_opy_]
  for platform in bstack1ll11l11l_opy_:
    for bstack1llll1llll_opy_ in bstack1lll1l1l_opy_:
      if bstack1llll1llll_opy_ in list(platform):
        if not bstack1lll1l1l_opy_[bstack1llll1llll_opy_] in platform:
          platform[bstack1lll1l1l_opy_[bstack1llll1llll_opy_]] = {}
        platform[bstack1lll1l1l_opy_[bstack1llll1llll_opy_]].update(platform[bstack1llll1llll_opy_])
        del platform[bstack1llll1llll_opy_]
  config = bstack111ll11l_opy_(config)
  return config
def bstack11l111l1_opy_(config):
  global bstack1ll1ll1l11_opy_
  if bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ") in config and str(config[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࢸ")]).lower() != bstack1111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࢹ"):
    if not bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ") in config:
      config[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")] = {}
    if not bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢼ") in config[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")]:
      bstack1111111l1_opy_ = datetime.datetime.now()
      bstack11l1l1111_opy_ = bstack1111111l1_opy_.strftime(bstack1111_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩࢾ"))
      hostname = socket.gethostname()
      bstack1111lll1l_opy_ = bstack1111_opy_ (u"࠭ࠧࢿ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1111_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩࣀ").format(bstack11l1l1111_opy_, hostname, bstack1111lll1l_opy_)
      config[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack1111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")] = identifier
    bstack1ll1ll1l11_opy_ = config[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")]
  return config
def bstack1111ll1l1_opy_():
  bstack11l11l1l1_opy_ =  bstack1111lll11_opy_()[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠫࣅ")]
  return bstack11l11l1l1_opy_ if bstack11l11l1l1_opy_ else -1
def bstack1ll1111ll1_opy_(bstack11l11l1l1_opy_):
  global CONFIG
  if not bstack1111_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨࣆ") in CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")]:
    return
  CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")] = CONFIG[bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")].replace(
    bstack1111_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ࣊"),
    str(bstack11l11l1l1_opy_)
  )
def bstack1l111lll_opy_():
  global CONFIG
  if not bstack1111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ࣋") in CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")]:
    return
  bstack1111111l1_opy_ = datetime.datetime.now()
  bstack11l1l1111_opy_ = bstack1111111l1_opy_.strftime(bstack1111_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫ࣍"))
  CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")] = CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")].replace(
    bstack1111_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ࣐"),
    bstack11l1l1111_opy_
  )
def bstack1l111l1ll_opy_():
  global CONFIG
  if bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ") in CONFIG and not bool(CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭")]):
    del CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]
    return
  if not bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ") in CONFIG:
    CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")] = bstack1111_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫࣖ")
  if bstack1111_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣗ") in CONFIG[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]:
    bstack1l111lll_opy_()
    os.environ[bstack1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨࣙ")] = CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]
  if not bstack1111_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨࣛ") in CONFIG[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]:
    return
  bstack11l11l1l1_opy_ = bstack1111_opy_ (u"ࠨࠩࣝ")
  bstack1ll1l1l1l1_opy_ = bstack1111ll1l1_opy_()
  if bstack1ll1l1l1l1_opy_ != -1:
    bstack11l11l1l1_opy_ = bstack1111_opy_ (u"ࠩࡆࡍࠥ࠭ࣞ") + str(bstack1ll1l1l1l1_opy_)
  if bstack11l11l1l1_opy_ == bstack1111_opy_ (u"ࠪࠫࣟ"):
    bstack1lll1lll11_opy_ = bstack1l1lll11_opy_(CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ࣠")])
    if bstack1lll1lll11_opy_ != -1:
      bstack11l11l1l1_opy_ = str(bstack1lll1lll11_opy_)
  if bstack11l11l1l1_opy_:
    bstack1ll1111ll1_opy_(bstack11l11l1l1_opy_)
    os.environ[bstack1111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ࣡")] = CONFIG[bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣢")]
def bstack1ll1l1lll1_opy_(bstack1l11lll1l_opy_, bstack1ll1ll11ll_opy_, path):
  bstack1111l11l1_opy_ = {
    bstack1111_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࣣࠫ"): bstack1ll1ll11ll_opy_
  }
  if os.path.exists(path):
    bstack11llll1l_opy_ = json.load(open(path, bstack1111_opy_ (u"ࠨࡴࡥࠫࣤ")))
  else:
    bstack11llll1l_opy_ = {}
  bstack11llll1l_opy_[bstack1l11lll1l_opy_] = bstack1111l11l1_opy_
  with open(path, bstack1111_opy_ (u"ࠤࡺ࠯ࠧࣥ")) as outfile:
    json.dump(bstack11llll1l_opy_, outfile)
def bstack1l1lll11_opy_(bstack1l11lll1l_opy_):
  bstack1l11lll1l_opy_ = str(bstack1l11lll1l_opy_)
  bstack11ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠪࢂࣦࠬ")), bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"))
  try:
    if not os.path.exists(bstack11ll1ll1_opy_):
      os.makedirs(bstack11ll1ll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠬࢄࠧࣨ")), bstack1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"), bstack1111_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩ࣪"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1111_opy_ (u"ࠨࡹࠪ࣫")):
        pass
      with open(file_path, bstack1111_opy_ (u"ࠤࡺ࠯ࠧ࣬")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1111_opy_ (u"ࠪࡶ࣭ࠬ")) as bstack11ll1l1l1_opy_:
      bstack1ll1ll1l1l_opy_ = json.load(bstack11ll1l1l1_opy_)
    if bstack1l11lll1l_opy_ in bstack1ll1ll1l1l_opy_:
      bstack1ll111l1ll_opy_ = bstack1ll1ll1l1l_opy_[bstack1l11lll1l_opy_][bstack1111_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣮")]
      bstack1ll11l1l1l_opy_ = int(bstack1ll111l1ll_opy_) + 1
      bstack1ll1l1lll1_opy_(bstack1l11lll1l_opy_, bstack1ll11l1l1l_opy_, file_path)
      return bstack1ll11l1l1l_opy_
    else:
      bstack1ll1l1lll1_opy_(bstack1l11lll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lllll1lll_opy_.format(str(e)))
    return -1
def bstack111ll11l1_opy_(config):
  if not config[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫࣯ࠧ")] or not config[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࣰࠩ")]:
    return True
  else:
    return False
def bstack1l1l111l_opy_(config, index=0):
  global bstack11llll11_opy_
  bstack11ll11l11_opy_ = {}
  caps = bstack1111111ll_opy_ + bstack1ll11lll_opy_
  if bstack11llll11_opy_:
    caps += bstack111l1llll_opy_
  for key in config:
    if key in caps + [bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]:
      continue
    bstack11ll11l11_opy_[key] = config[key]
  if bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ") in config:
    for bstack11ll111l1_opy_ in config[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")][index]:
      if bstack11ll111l1_opy_ in caps + [bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣴ"), bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࣵ")]:
        continue
      bstack11ll11l11_opy_[bstack11ll111l1_opy_] = config[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣶ")][index][bstack11ll111l1_opy_]
  bstack11ll11l11_opy_[bstack1111_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨࣷ")] = socket.gethostname()
  if bstack1111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ") in bstack11ll11l11_opy_:
    del (bstack11ll11l11_opy_[bstack1111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࣹࠩ")])
  return bstack11ll11l11_opy_
def bstack11ll1l1ll_opy_(config):
  global bstack11llll11_opy_
  bstack11llll11l_opy_ = {}
  caps = bstack1ll11lll_opy_
  if bstack11llll11_opy_:
    caps += bstack111l1llll_opy_
  for key in caps:
    if key in config:
      bstack11llll11l_opy_[key] = config[key]
  return bstack11llll11l_opy_
def bstack1llll11l1l_opy_(bstack11ll11l11_opy_, bstack11llll11l_opy_):
  bstack1l111ll11_opy_ = {}
  for key in bstack11ll11l11_opy_.keys():
    if key in bstack1ll11ll1l_opy_:
      bstack1l111ll11_opy_[bstack1ll11ll1l_opy_[key]] = bstack11ll11l11_opy_[key]
    else:
      bstack1l111ll11_opy_[key] = bstack11ll11l11_opy_[key]
  for key in bstack11llll11l_opy_:
    if key in bstack1ll11ll1l_opy_:
      bstack1l111ll11_opy_[bstack1ll11ll1l_opy_[key]] = bstack11llll11l_opy_[key]
    else:
      bstack1l111ll11_opy_[key] = bstack11llll11l_opy_[key]
  return bstack1l111ll11_opy_
def bstack1ll1ll1lll_opy_(config, index=0):
  global bstack11llll11_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack11llll11l_opy_ = bstack11ll1l1ll_opy_(config)
  bstack1l1l1l11l_opy_ = bstack1ll11lll_opy_
  bstack1l1l1l11l_opy_ += bstack11ll1l11_opy_
  if bstack11llll11_opy_:
    bstack1l1l1l11l_opy_ += bstack111l1llll_opy_
  if bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ") in config:
    if bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ") in config[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index]:
      caps[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")] = config[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index][bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")]
    if bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ") in config[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index]:
      caps[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")] = str(config[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index][bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")])
    bstack1ll11ll11_opy_ = {}
    for bstack1llll11l_opy_ in bstack1l1l1l11l_opy_:
      if bstack1llll11l_opy_ in config[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1llll11l_opy_ == bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack1ll11ll11_opy_[bstack1llll11l_opy_] = str(config[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1llll11l_opy_] * 1.0)
          except:
            bstack1ll11ll11_opy_[bstack1llll11l_opy_] = str(config[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1llll11l_opy_])
        else:
          bstack1ll11ll11_opy_[bstack1llll11l_opy_] = config[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1llll11l_opy_]
        del (config[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1llll11l_opy_])
    bstack11llll11l_opy_ = update(bstack11llll11l_opy_, bstack1ll11ll11_opy_)
  bstack11ll11l11_opy_ = bstack1l1l111l_opy_(config, index)
  for bstack11l111ll_opy_ in bstack1ll11lll_opy_ + [bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऋ"), bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧऌ")]:
    if bstack11l111ll_opy_ in bstack11ll11l11_opy_:
      bstack11llll11l_opy_[bstack11l111ll_opy_] = bstack11ll11l11_opy_[bstack11l111ll_opy_]
      del (bstack11ll11l11_opy_[bstack11l111ll_opy_])
  if bstack1lll11l1_opy_(config):
    bstack11ll11l11_opy_[bstack1111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = True
    caps.update(bstack11llll11l_opy_)
    caps[bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩऎ")] = bstack11ll11l11_opy_
  else:
    bstack11ll11l11_opy_[bstack1111_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = False
    caps.update(bstack1llll11l1l_opy_(bstack11ll11l11_opy_, bstack11llll11l_opy_))
    if bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ") in caps:
      caps[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬऑ")] = caps[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ")]
      del (caps[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫओ")])
    if bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ") in caps:
      caps[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪक")] = caps[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख")]
      del (caps[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫग")])
  return caps
def bstack1l1111ll_opy_():
  global bstack11l11l11l_opy_
  if bstack1llll1ll1_opy_() <= version.parse(bstack1111_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫघ")):
    if bstack11l11l11l_opy_ != bstack1111_opy_ (u"ࠬ࠭ङ"):
      return bstack1111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢच") + bstack11l11l11l_opy_ + bstack1111_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦछ")
    return bstack111lll111_opy_
  if bstack11l11l11l_opy_ != bstack1111_opy_ (u"ࠨࠩज"):
    return bstack1111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦझ") + bstack11l11l11l_opy_ + bstack1111_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦञ")
  return bstack1lll1ll11l_opy_
def bstack1lllll1ll_opy_(options):
  return hasattr(options, bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬट"))
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
def bstack11ll1l111_opy_(options, bstack1ll11ll1ll_opy_):
  for bstack11l1l1ll1_opy_ in bstack1ll11ll1ll_opy_:
    if bstack11l1l1ll1_opy_ in [bstack1111_opy_ (u"ࠬࡧࡲࡨࡵࠪठ"), bstack1111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪड")]:
      continue
    if bstack11l1l1ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack11l1l1ll1_opy_] = update(options._experimental_options[bstack11l1l1ll1_opy_],
                                                         bstack1ll11ll1ll_opy_[bstack11l1l1ll1_opy_])
    else:
      options.add_experimental_option(bstack11l1l1ll1_opy_, bstack1ll11ll1ll_opy_[bstack11l1l1ll1_opy_])
  if bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬढ") in bstack1ll11ll1ll_opy_:
    for arg in bstack1ll11ll1ll_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ण")]:
      options.add_argument(arg)
    del (bstack1ll11ll1ll_opy_[bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत")])
  if bstack1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ") in bstack1ll11ll1ll_opy_:
    for ext in bstack1ll11ll1ll_opy_[bstack1111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨद")]:
      options.add_extension(ext)
    del (bstack1ll11ll1ll_opy_[bstack1111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध")])
def bstack1l11l1ll_opy_(options, bstack1ll1l1llll_opy_):
  if bstack1111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन") in bstack1ll1l1llll_opy_:
    for bstack11ll11ll_opy_ in bstack1ll1l1llll_opy_[bstack1111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")]:
      if bstack11ll11ll_opy_ in options._preferences:
        options._preferences[bstack11ll11ll_opy_] = update(options._preferences[bstack11ll11ll_opy_], bstack1ll1l1llll_opy_[bstack1111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप")][bstack11ll11ll_opy_])
      else:
        options.set_preference(bstack11ll11ll_opy_, bstack1ll1l1llll_opy_[bstack1111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")][bstack11ll11ll_opy_])
  if bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨब") in bstack1ll1l1llll_opy_:
    for arg in bstack1ll1l1llll_opy_[bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩभ")]:
      options.add_argument(arg)
def bstack1ll11lllll_opy_(options, bstack1ll1ll1ll1_opy_):
  if bstack1111_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭म") in bstack1ll1ll1ll1_opy_:
    options.use_webview(bool(bstack1ll1ll1ll1_opy_[bstack1111_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧय")]))
  bstack11ll1l111_opy_(options, bstack1ll1ll1ll1_opy_)
def bstack1lll1lll1_opy_(options, bstack1ll1ll1l_opy_):
  for bstack1llll1111l_opy_ in bstack1ll1ll1l_opy_:
    if bstack1llll1111l_opy_ in [bstack1111_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫर"), bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      continue
    options.set_capability(bstack1llll1111l_opy_, bstack1ll1ll1l_opy_[bstack1llll1111l_opy_])
  if bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧल") in bstack1ll1ll1l_opy_:
    for arg in bstack1ll1ll1l_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      options.add_argument(arg)
  if bstack1111_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨऴ") in bstack1ll1ll1l_opy_:
    options.bstack1l11l11l1_opy_(bool(bstack1ll1ll1l_opy_[bstack1111_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩव")]))
def bstack1l111ll1l_opy_(options, bstack1lllll11ll_opy_):
  for bstack1ll11ll11l_opy_ in bstack1lllll11ll_opy_:
    if bstack1ll11ll11l_opy_ in [bstack1111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश"), bstack1111_opy_ (u"ࠧࡢࡴࡪࡷࠬष")]:
      continue
    options._options[bstack1ll11ll11l_opy_] = bstack1lllll11ll_opy_[bstack1ll11ll11l_opy_]
  if bstack1111_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस") in bstack1lllll11ll_opy_:
    for bstack11l11lll_opy_ in bstack1lllll11ll_opy_[bstack1111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ह")]:
      options.bstack1lll11l1l_opy_(
        bstack11l11lll_opy_, bstack1lllll11ll_opy_[bstack1111_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ")][bstack11l11lll_opy_])
  if bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩऻ") in bstack1lllll11ll_opy_:
    for arg in bstack1lllll11ll_opy_[bstack1111_opy_ (u"ࠬࡧࡲࡨࡵ़ࠪ")]:
      options.add_argument(arg)
def bstack1l11111ll_opy_(options, caps):
  if not hasattr(options, bstack1111_opy_ (u"࠭ࡋࡆ࡛ࠪऽ")):
    return
  if options.KEY == bstack1111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack11ll1l111_opy_(options, caps[bstack1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1111_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1l11l1ll_opy_(options, caps[bstack1111_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack1111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1lll1lll1_opy_(options, caps[bstack1111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1111_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack1ll11lllll_opy_(options, caps[bstack1111_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack1111_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॆ") and options.KEY in caps:
    bstack1l111ll1l_opy_(options, caps[bstack1111_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨे")])
def bstack111l1lll1_opy_(caps):
  global bstack11llll11_opy_
  if isinstance(os.environ.get(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫै")), str):
    bstack11llll11_opy_ = eval(os.getenv(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬॉ")))
  if bstack11llll11_opy_:
    if bstack11l1l1lll_opy_() < version.parse(bstack1111_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫॊ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ो")
    if bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ") in caps:
      browser = caps[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    elif bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॎ") in caps:
      browser = caps[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫॏ")]
    browser = str(browser).lower()
    if browser == bstack1111_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫॐ") or browser == bstack1111_opy_ (u"ࠬ࡯ࡰࡢࡦࠪ॑"):
      browser = bstack1111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮॒࠭")
    if browser == bstack1111_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨ॓"):
      browser = bstack1111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ॔")
    if browser not in [bstack1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩॕ"), bstack1111_opy_ (u"ࠪࡩࡩ࡭ࡥࠨॖ"), bstack1111_opy_ (u"ࠫ࡮࡫ࠧॗ"), bstack1111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬक़"), bstack1111_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧख़")]:
      return None
    try:
      package = bstack1111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩग़").format(browser)
      name = bstack1111_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩज़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lllll1ll_opy_(options):
        return None
      for bstack11l111ll_opy_ in caps.keys():
        options.set_capability(bstack11l111ll_opy_, caps[bstack11l111ll_opy_])
      bstack1l11111ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1111lll_opy_(options, bstack1ll11llll_opy_):
  if not bstack1lllll1ll_opy_(options):
    return
  for bstack11l111ll_opy_ in bstack1ll11llll_opy_.keys():
    if bstack11l111ll_opy_ in bstack11ll1l11_opy_:
      continue
    if bstack11l111ll_opy_ in options._caps and type(options._caps[bstack11l111ll_opy_]) in [dict, list]:
      options._caps[bstack11l111ll_opy_] = update(options._caps[bstack11l111ll_opy_], bstack1ll11llll_opy_[bstack11l111ll_opy_])
    else:
      options.set_capability(bstack11l111ll_opy_, bstack1ll11llll_opy_[bstack11l111ll_opy_])
  bstack1l11111ll_opy_(options, bstack1ll11llll_opy_)
  if bstack1111_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨड़") in options._caps:
    if options._caps[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")] and options._caps[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़")].lower() != bstack1111_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭य़"):
      del options._caps[bstack1111_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬॠ")]
def bstack11ll11l1_opy_(proxy_config):
  if bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ") in proxy_config:
    proxy_config[bstack1111_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪॢ")] = proxy_config[bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ")]
    del (proxy_config[bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ।")])
  if bstack1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ॥") in proxy_config and proxy_config[bstack1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")].lower() != bstack1111_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭१"):
    proxy_config[bstack1111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")] = bstack1111_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨ३")
  if bstack1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧ४") in proxy_config:
    proxy_config[bstack1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭५")] = bstack1111_opy_ (u"ࠫࡵࡧࡣࠨ६")
  return proxy_config
def bstack1ll1llll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७") in config:
    return proxy
  config[bstack1111_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")] = bstack11ll11l1_opy_(config[bstack1111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९")])
  if proxy == None:
    proxy = Proxy(config[bstack1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")])
  return proxy
def bstack111l11l1_opy_(self):
  global CONFIG
  global bstack1ll11l1ll_opy_
  try:
    proxy = bstack111ll1111_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1111_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॱ")):
        proxies = bstack111llllll_opy_(proxy, bstack1l1111ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11lll11_opy_ = proxies.popitem()
          if bstack1111_opy_ (u"ࠥ࠾࠴࠵ࠢॲ") in bstack1ll11lll11_opy_:
            return bstack1ll11lll11_opy_
          else:
            return bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧॳ") + bstack1ll11lll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤॴ").format(str(e)))
  return bstack1ll11l1ll_opy_(self)
def bstack1lllll11_opy_():
  global CONFIG
  return bstack1l1l11ll1_opy_(CONFIG) and bstack1111ll111_opy_() and bstack1llll1ll1_opy_() >= version.parse(bstack111111111_opy_)
def bstack111lllll1_opy_():
  global CONFIG
  return (bstack1111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩॵ") in CONFIG or bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॶ") in CONFIG) and bstack1l11llll_opy_()
def bstack1l1llll11l_opy_(config):
  bstack11l1lll11_opy_ = {}
  if bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॷ") in config:
    bstack11l1lll11_opy_ = config[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॸ")]
  if bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॹ") in config:
    bstack11l1lll11_opy_ = config[bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॺ")]
  proxy = bstack111ll1111_opy_(config)
  if proxy:
    if proxy.endswith(bstack1111_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")) and os.path.isfile(proxy):
      bstack11l1lll11_opy_[bstack1111_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩॼ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1111_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")):
        proxies = bstack1l1llll11_opy_(config, bstack1l1111ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11lll11_opy_ = proxies.popitem()
          if bstack1111_opy_ (u"ࠣ࠼࠲࠳ࠧॾ") in bstack1ll11lll11_opy_:
            parsed_url = urlparse(bstack1ll11lll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1111_opy_ (u"ࠤ࠽࠳࠴ࠨॿ") + bstack1ll11lll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11l1lll11_opy_[bstack1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ঀ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11l1lll11_opy_[bstack1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧঁ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11l1lll11_opy_[bstack1111_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨং")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11l1lll11_opy_[bstack1111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩঃ")] = str(parsed_url.password)
  return bstack11l1lll11_opy_
def bstack1l1lll1lll_opy_(config):
  if bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ঄") in config:
    return config[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭অ")]
  return {}
def bstack1lll1l1111_opy_(caps):
  global bstack1ll1ll1l11_opy_
  if bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪআ") in caps:
    caps[bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪঈ")] = True
    if bstack1ll1ll1l11_opy_:
      caps[bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨঊ")] = bstack1ll1ll1l11_opy_
  else:
    caps[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬঋ")] = True
    if bstack1ll1ll1l11_opy_:
      caps[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩঌ")] = bstack1ll1ll1l11_opy_
def bstack1111l111l_opy_():
  global CONFIG
  if bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭঍") in CONFIG and CONFIG[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ঎")]:
    bstack11l1lll11_opy_ = bstack1l1llll11l_opy_(CONFIG)
    bstack1ll1l1ll_opy_(CONFIG[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧএ")], bstack11l1lll11_opy_)
def bstack1ll1l1ll_opy_(key, bstack11l1lll11_opy_):
  global bstack1lllllll1_opy_
  logger.info(bstack1ll11ll1_opy_)
  try:
    bstack1lllllll1_opy_ = Local()
    bstack11l1111l_opy_ = {bstack1111_opy_ (u"ࠬࡱࡥࡺࠩঐ"): key}
    bstack11l1111l_opy_.update(bstack11l1lll11_opy_)
    logger.debug(bstack1ll1llll11_opy_.format(str(bstack11l1111l_opy_)))
    bstack1lllllll1_opy_.start(**bstack11l1111l_opy_)
    if bstack1lllllll1_opy_.isRunning():
      logger.info(bstack111l11l11_opy_)
  except Exception as e:
    bstack11llll111_opy_(bstack1llllll1l1_opy_.format(str(e)))
def bstack1ll1llll1_opy_():
  global bstack1lllllll1_opy_
  if bstack1lllllll1_opy_.isRunning():
    logger.info(bstack1l1l111ll_opy_)
    bstack1lllllll1_opy_.stop()
  bstack1lllllll1_opy_ = None
def bstack1llllll1ll_opy_(bstack1l11l1lll_opy_=[]):
  global CONFIG
  bstack111ll1l11_opy_ = []
  bstack1llll111l_opy_ = [bstack1111_opy_ (u"࠭࡯ࡴࠩ঑"), bstack1111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ঒"), bstack1111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬও"), bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫঔ"), bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨক"), bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬখ")]
  try:
    for err in bstack1l11l1lll_opy_:
      bstack111111ll_opy_ = {}
      for k in bstack1llll111l_opy_:
        val = CONFIG[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨগ")][int(err[bstack1111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬঘ")])].get(k)
        if val:
          bstack111111ll_opy_[k] = val
      bstack111111ll_opy_[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭ঙ")] = {
        err[bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭চ")]: err[bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")]
      }
      bstack111ll1l11_opy_.append(bstack111111ll_opy_)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬজ") + str(e))
  finally:
    return bstack111ll1l11_opy_
def bstack1ll1lll111_opy_(file_name):
  bstack1111l1l1_opy_ = []
  try:
    bstack1ll11l1l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll11l1l1_opy_):
      with open(bstack1ll11l1l1_opy_) as f:
        bstack1llll11ll1_opy_ = json.load(f)
        bstack1111l1l1_opy_ = bstack1llll11ll1_opy_
      os.remove(bstack1ll11l1l1_opy_)
    return bstack1111l1l1_opy_
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ঝ") + str(e))
def bstack1llllll111_opy_():
  global bstack111l1lll_opy_
  global bstack11lll1111_opy_
  global bstack1ll1ll1ll_opy_
  global bstack1ll1llllll_opy_
  global bstack1l11ll1l_opy_
  global bstack1l1ll111l_opy_
  percy.shutdown()
  bstack1ll1l1ll11_opy_ = os.environ.get(bstack1111_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ঞ"))
  if bstack1ll1l1ll11_opy_ in [bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬট"), bstack1111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ঠ")]:
    bstack11llll1ll_opy_()
  if bstack111l1lll_opy_:
    logger.warning(bstack1lllll11l1_opy_.format(str(bstack111l1lll_opy_)))
  else:
    try:
      bstack11llll1l_opy_ = bstack1ll111l1l_opy_(bstack1111_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧড"), logger)
      if bstack11llll1l_opy_.get(bstack1111_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧঢ")) and bstack11llll1l_opy_.get(bstack1111_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")).get(bstack1111_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ত")):
        logger.warning(bstack1lllll11l1_opy_.format(str(bstack11llll1l_opy_[bstack1111_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪথ")][bstack1111_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨদ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1llll1l1l_opy_)
  global bstack1lllllll1_opy_
  if bstack1lllllll1_opy_:
    bstack1ll1llll1_opy_()
  try:
    for driver in bstack11lll1111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lll1l111_opy_)
  if bstack1l1ll111l_opy_ == bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ধ"):
    bstack1l11ll1l_opy_ = bstack1ll1lll111_opy_(bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩন"))
  if bstack1l1ll111l_opy_ == bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ঩") and len(bstack1ll1llllll_opy_) == 0:
    bstack1ll1llllll_opy_ = bstack1ll1lll111_opy_(bstack1111_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨপ"))
    if len(bstack1ll1llllll_opy_) == 0:
      bstack1ll1llllll_opy_ = bstack1ll1lll111_opy_(bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪফ"))
  bstack1l111ll1_opy_ = bstack1111_opy_ (u"ࠬ࠭ব")
  if len(bstack1ll1ll1ll_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1llllll1ll_opy_(bstack1ll1ll1ll_opy_)
  elif len(bstack1ll1llllll_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1llllll1ll_opy_(bstack1ll1llllll_opy_)
  elif len(bstack1l11ll1l_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1llllll1ll_opy_(bstack1l11ll1l_opy_)
  elif len(bstack111ll1lll_opy_) > 0:
    bstack1l111ll1_opy_ = bstack1llllll1ll_opy_(bstack111ll1lll_opy_)
  if bool(bstack1l111ll1_opy_):
    bstack1lllll11l_opy_(bstack1l111ll1_opy_)
  else:
    bstack1lllll11l_opy_()
  bstack111ll11ll_opy_(bstack1ll11111l_opy_, logger)
def bstack111l1l1ll_opy_(self, *args):
  logger.error(bstack11l11ll11_opy_)
  bstack1llllll111_opy_()
  sys.exit(1)
def bstack11llll111_opy_(err):
  logger.critical(bstack1ll1ll11_opy_.format(str(err)))
  bstack1lllll11l_opy_(bstack1ll1ll11_opy_.format(str(err)))
  atexit.unregister(bstack1llllll111_opy_)
  bstack11llll1ll_opy_()
  sys.exit(1)
def bstack1ll1l1l111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lllll11l_opy_(message)
  atexit.unregister(bstack1llllll111_opy_)
  bstack11llll1ll_opy_()
  sys.exit(1)
def bstack1l1l1ll1_opy_():
  global CONFIG
  global bstack1lll111l11_opy_
  global bstack1ll11lll1l_opy_
  global bstack11111llll_opy_
  CONFIG = bstack11111ll1l_opy_()
  bstack1ll1l11ll1_opy_()
  bstack1lll1lllll_opy_()
  CONFIG = bstack11lllll1_opy_(CONFIG)
  update(CONFIG, bstack1ll11lll1l_opy_)
  update(CONFIG, bstack1lll111l11_opy_)
  CONFIG = bstack11l111l1_opy_(CONFIG)
  bstack11111llll_opy_ = bstack1l111lll1_opy_(CONFIG)
  bstack1llll1l1ll_opy_.bstack111l1111_opy_(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧভ"), bstack11111llll_opy_)
  if (bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪম") in CONFIG and bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫয") in bstack1lll111l11_opy_) or (
          bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in CONFIG and bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") not in bstack1ll11lll1l_opy_):
    if os.getenv(bstack1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨল")):
      CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঳")] = os.getenv(bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ঴"))
    else:
      bstack1l111l1ll_opy_()
  elif (bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in CONFIG and bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪশ") in CONFIG) or (
          bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬষ") in bstack1ll11lll1l_opy_ and bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭স") not in bstack1lll111l11_opy_):
    del (CONFIG[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭হ")])
  if bstack111ll11l1_opy_(CONFIG):
    bstack11llll111_opy_(bstack1ll11l1ll1_opy_)
  bstack11l1l11l_opy_()
  bstack11lllll1l_opy_()
  if bstack11llll11_opy_:
    CONFIG[bstack1111_opy_ (u"ࠬࡧࡰࡱࠩ঺")] = bstack1l111llll_opy_(CONFIG)
    logger.info(bstack1lll1l1l1l_opy_.format(CONFIG[bstack1111_opy_ (u"࠭ࡡࡱࡲࠪ঻")]))
def bstack11l1lllll_opy_(config, bstack1l1ll11l1_opy_):
  global CONFIG
  global bstack11llll11_opy_
  CONFIG = config
  bstack11llll11_opy_ = bstack1l1ll11l1_opy_
def bstack11lllll1l_opy_():
  global CONFIG
  global bstack11llll11_opy_
  if bstack1111_opy_ (u"ࠧࡢࡲࡳ়ࠫ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1l1l1111l_opy_)
    bstack11llll11_opy_ = True
    bstack1llll1l1ll_opy_.bstack111l1111_opy_(bstack1111_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧঽ"), True)
def bstack1l111llll_opy_(config):
  bstack1lll1111l_opy_ = bstack1111_opy_ (u"ࠩࠪা")
  app = config[bstack1111_opy_ (u"ࠪࡥࡵࡶࠧি")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111ll1l1_opy_:
      if os.path.exists(app):
        bstack1lll1111l_opy_ = bstack11l1llll_opy_(config, app)
      elif bstack1lll1l11_opy_(app):
        bstack1lll1111l_opy_ = app
      else:
        bstack11llll111_opy_(bstack1l11l1l1l_opy_.format(app))
    else:
      if bstack1lll1l11_opy_(app):
        bstack1lll1111l_opy_ = app
      elif os.path.exists(app):
        bstack1lll1111l_opy_ = bstack11l1llll_opy_(app)
      else:
        bstack11llll111_opy_(bstack1llll1ll11_opy_)
  else:
    if len(app) > 2:
      bstack11llll111_opy_(bstack11111l1l1_opy_)
    elif len(app) == 2:
      if bstack1111_opy_ (u"ࠫࡵࡧࡴࡩࠩী") in app and bstack1111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨু") in app:
        if os.path.exists(app[bstack1111_opy_ (u"࠭ࡰࡢࡶ࡫ࠫূ")]):
          bstack1lll1111l_opy_ = bstack11l1llll_opy_(config, app[bstack1111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬৃ")], app[bstack1111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫৄ")])
        else:
          bstack11llll111_opy_(bstack1l11l1l1l_opy_.format(app))
      else:
        bstack11llll111_opy_(bstack11111l1l1_opy_)
    else:
      for key in app:
        if key in bstack1111llll_opy_:
          if key == bstack1111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৅"):
            if os.path.exists(app[key]):
              bstack1lll1111l_opy_ = bstack11l1llll_opy_(config, app[key])
            else:
              bstack11llll111_opy_(bstack1l11l1l1l_opy_.format(app))
          else:
            bstack1lll1111l_opy_ = app[key]
        else:
          bstack11llll111_opy_(bstack1111ll11_opy_)
  return bstack1lll1111l_opy_
def bstack1lll1l11_opy_(bstack1lll1111l_opy_):
  import re
  bstack1l11l111l_opy_ = re.compile(bstack1111_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ৆"))
  bstack111l11lll_opy_ = re.compile(bstack1111_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣে"))
  if bstack1111_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫৈ") in bstack1lll1111l_opy_ or re.fullmatch(bstack1l11l111l_opy_, bstack1lll1111l_opy_) or re.fullmatch(bstack111l11lll_opy_, bstack1lll1111l_opy_):
    return True
  else:
    return False
def bstack11l1llll_opy_(config, path, bstack11llllll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1111_opy_ (u"࠭ࡲࡣࠩ৉")).read()).hexdigest()
  bstack1llll1ll_opy_ = bstack11l1l1l1_opy_(md5_hash)
  bstack1lll1111l_opy_ = None
  if bstack1llll1ll_opy_:
    logger.info(bstack1l1ll1111_opy_.format(bstack1llll1ll_opy_, md5_hash))
    return bstack1llll1ll_opy_
  bstack1ll1l1111_opy_ = MultipartEncoder(
    fields={
      bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࠬ৊"): (os.path.basename(path), open(os.path.abspath(path), bstack1111_opy_ (u"ࠨࡴࡥࠫো")), bstack1111_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ৌ")),
      bstack1111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ্࠭"): bstack11llllll_opy_
    }
  )
  response = requests.post(bstack1111l1lll_opy_, data=bstack1ll1l1111_opy_,
                           headers={bstack1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪৎ"): bstack1ll1l1111_opy_.content_type},
                           auth=(config[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ৏")], config[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৐")]))
  try:
    res = json.loads(response.text)
    bstack1lll1111l_opy_ = res[bstack1111_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨ৑")]
    logger.info(bstack1ll111111_opy_.format(bstack1lll1111l_opy_))
    bstack1lllll1111_opy_(md5_hash, bstack1lll1111l_opy_)
  except ValueError as err:
    bstack11llll111_opy_(bstack1ll11l1111_opy_.format(str(err)))
  return bstack1lll1111l_opy_
def bstack11l1l11l_opy_():
  global CONFIG
  global bstack1lll11111l_opy_
  bstack1ll1l11l11_opy_ = 0
  bstack1l1l1l111_opy_ = 1
  if bstack1111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ৒") in CONFIG:
    bstack1l1l1l111_opy_ = CONFIG[bstack1111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৓")]
  if bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৔") in CONFIG:
    bstack1ll1l11l11_opy_ = len(CONFIG[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৕")])
  bstack1lll11111l_opy_ = int(bstack1l1l1l111_opy_) * int(bstack1ll1l11l11_opy_)
def bstack11l1l1l1_opy_(md5_hash):
  bstack1ll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠬࢄࠧ৖")), bstack1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ৗ"), bstack1111_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ৘"))
  if os.path.exists(bstack1ll1l1l1_opy_):
    bstack1ll1111l1l_opy_ = json.load(open(bstack1ll1l1l1_opy_, bstack1111_opy_ (u"ࠨࡴࡥࠫ৙")))
    if md5_hash in bstack1ll1111l1l_opy_:
      bstack1llll1l11l_opy_ = bstack1ll1111l1l_opy_[md5_hash]
      bstack1lll1111ll_opy_ = datetime.datetime.now()
      bstack1ll1ll11l1_opy_ = datetime.datetime.strptime(bstack1llll1l11l_opy_[bstack1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ৚")], bstack1111_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৛"))
      if (bstack1lll1111ll_opy_ - bstack1ll1ll11l1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1llll1l11l_opy_[bstack1111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩড়")]):
        return None
      return bstack1llll1l11l_opy_[bstack1111_opy_ (u"ࠬ࡯ࡤࠨঢ়")]
  else:
    return None
def bstack1lllll1111_opy_(md5_hash, bstack1lll1111l_opy_):
  bstack11ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"࠭ࡾࠨ৞")), bstack1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧয়"))
  if not os.path.exists(bstack11ll1ll1_opy_):
    os.makedirs(bstack11ll1ll1_opy_)
  bstack1ll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠨࢀࠪৠ")), bstack1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩৡ"), bstack1111_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫৢ"))
  bstack11ll1lll1_opy_ = {
    bstack1111_opy_ (u"ࠫ࡮ࡪࠧৣ"): bstack1lll1111l_opy_,
    bstack1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৤"): datetime.datetime.strftime(datetime.datetime.now(), bstack1111_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৥")),
    bstack1111_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ০"): str(__version__)
  }
  if os.path.exists(bstack1ll1l1l1_opy_):
    bstack1ll1111l1l_opy_ = json.load(open(bstack1ll1l1l1_opy_, bstack1111_opy_ (u"ࠨࡴࡥࠫ১")))
  else:
    bstack1ll1111l1l_opy_ = {}
  bstack1ll1111l1l_opy_[md5_hash] = bstack11ll1lll1_opy_
  with open(bstack1ll1l1l1_opy_, bstack1111_opy_ (u"ࠤࡺ࠯ࠧ২")) as outfile:
    json.dump(bstack1ll1111l1l_opy_, outfile)
def bstack11l1ll11_opy_(self):
  return
def bstack11l11111l_opy_(self):
  return
def bstack1l1l111l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1ll11ll_opy_(self):
  global bstack1lll1l1ll_opy_
  global bstack1lll1ll1_opy_
  global bstack1ll1l1l1l_opy_
  try:
    if bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ৩") in bstack1lll1l1ll_opy_ and self.session_id != None and bstack1ll111l111_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ৪"), bstack1111_opy_ (u"ࠬ࠭৫")) != bstack1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ৬"):
      bstack111111ll1_opy_ = bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ৭") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ৮")
      bstack11l11l11_opy_ = bstack1llll1lll1_opy_(bstack1111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ৯"), bstack1111_opy_ (u"ࠪࠫৰ"), bstack111111ll1_opy_, bstack1111_opy_ (u"ࠫ࠱ࠦࠧৱ").join(
        threading.current_thread().bstackTestErrorMessages), bstack1111_opy_ (u"ࠬ࠭৲"), bstack1111_opy_ (u"࠭ࠧ৳"))
      if bstack111111ll1_opy_ == bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ৴"):
        bstack11l1ll11l_opy_(logger)
      if self != None:
        self.execute_script(bstack11l11l11_opy_)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ৵") + str(e))
  bstack1ll1l1l1l_opy_(self)
  self.session_id = None
def bstack1l1l11l1l_opy_(self, *args, **kwargs):
  bstack11l1ll1l_opy_ = bstack1l1ll1l11_opy_(self, *args, **kwargs)
  bstack1l1lll11l_opy_.bstack1ll11l111_opy_(self)
  return bstack11l1ll1l_opy_
def bstack11111l11l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1lll1ll1_opy_
  global bstack1llll11111_opy_
  global bstack1ll111lll_opy_
  global bstack1lll1l1l1_opy_
  global bstack11ll11111_opy_
  global bstack1lll1l1ll_opy_
  global bstack1l1ll1l11_opy_
  global bstack11lll1111_opy_
  global bstack1llll1lll_opy_
  CONFIG[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ৶")] = str(bstack1lll1l1ll_opy_) + str(__version__)
  command_executor = bstack1l1111ll_opy_()
  logger.debug(bstack111l1111l_opy_.format(command_executor))
  proxy = bstack1ll1llll_opy_(CONFIG, proxy)
  bstack1ll111ll1_opy_ = 0 if bstack1llll11111_opy_ < 0 else bstack1llll11111_opy_
  try:
    if bstack1lll1l1l1_opy_ is True:
      bstack1ll111ll1_opy_ = int(multiprocessing.current_process().name)
    elif bstack11ll11111_opy_ is True:
      bstack1ll111ll1_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll111ll1_opy_ = 0
  bstack1ll11llll_opy_ = bstack1ll1ll1lll_opy_(CONFIG, bstack1ll111ll1_opy_)
  logger.debug(bstack111l1ll1_opy_.format(str(bstack1ll11llll_opy_)))
  if bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৷") in CONFIG and CONFIG[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ৸")]:
    bstack1lll1l1111_opy_(bstack1ll11llll_opy_)
  if desired_capabilities:
    bstack1ll1l11111_opy_ = bstack11lllll1_opy_(desired_capabilities)
    bstack1ll1l11111_opy_[bstack1111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ৹")] = bstack1lll11l1_opy_(CONFIG)
    bstack1111l1ll_opy_ = bstack1ll1ll1lll_opy_(bstack1ll1l11111_opy_)
    if bstack1111l1ll_opy_:
      bstack1ll11llll_opy_ = update(bstack1111l1ll_opy_, bstack1ll11llll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1111lll_opy_(options, bstack1ll11llll_opy_)
  if not options:
    options = bstack111l1lll1_opy_(bstack1ll11llll_opy_)
  if bstack111ll1l1l_opy_.bstack1llll11l11_opy_(CONFIG, bstack1ll111ll1_opy_) and bstack111ll1l1l_opy_.bstack1lll11l111_opy_(bstack1ll11llll_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack111ll1l1l_opy_.set_capabilities(bstack1ll11llll_opy_, CONFIG)
  if proxy and bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭৺")):
    options.proxy(proxy)
  if options and bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭৻")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1llll1ll1_opy_() < version.parse(bstack1111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧৼ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll11llll_opy_)
  logger.info(bstack1l1l1ll1l_opy_)
  if bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ৽")):
    bstack1l1ll1l11_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ৾")):
    bstack1l1ll1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ৿")):
    bstack1l1ll1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1ll1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11l1l111l_opy_ = bstack1111_opy_ (u"ࠬ࠭਀")
    if bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧਁ")):
      bstack11l1l111l_opy_ = self.caps.get(bstack1111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢਂ"))
    else:
      bstack11l1l111l_opy_ = self.capabilities.get(bstack1111_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣਃ"))
    if bstack11l1l111l_opy_:
      bstack1l11ll111_opy_(bstack11l1l111l_opy_)
      if bstack1llll1ll1_opy_() <= version.parse(bstack1111_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ਄")):
        self.command_executor._url = bstack1111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦਅ") + bstack11l11l11l_opy_ + bstack1111_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣਆ")
      else:
        self.command_executor._url = bstack1111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢਇ") + bstack11l1l111l_opy_ + bstack1111_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢਈ")
      logger.debug(bstack111ll1ll1_opy_.format(bstack11l1l111l_opy_))
    else:
      logger.debug(bstack1ll1l1lll_opy_.format(bstack1111_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣਉ")))
  except Exception as e:
    logger.debug(bstack1ll1l1lll_opy_.format(e))
  if bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧਊ") in bstack1lll1l1ll_opy_:
    bstack1111ll1ll_opy_(bstack1llll11111_opy_, bstack1llll1lll_opy_)
  bstack1lll1ll1_opy_ = self.session_id
  if bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ਋") in bstack1lll1l1ll_opy_ or bstack1111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ਌") in bstack1lll1l1ll_opy_:
    threading.current_thread().bstack1ll1l11l1l_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l1lll11l_opy_.bstack1ll11l111_opy_(self)
  bstack11lll1111_opy_.append(self)
  if bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ਍") in CONFIG and bstack1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ਎") in CONFIG[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਏ")][bstack1ll111ll1_opy_]:
    bstack1ll111lll_opy_ = CONFIG[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਐ")][bstack1ll111ll1_opy_][bstack1111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭਑")]
  logger.debug(bstack1ll1lllll1_opy_.format(bstack1lll1ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1lllll1ll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lll111l1l_opy_
      if(bstack1111_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦ਒") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠪࢂࠬਓ")), bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਔ"), bstack1111_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਕ")), bstack1111_opy_ (u"࠭ࡷࠨਖ")) as fp:
          fp.write(bstack1111_opy_ (u"ࠢࠣਗ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1111_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥਘ")))):
          with open(args[1], bstack1111_opy_ (u"ࠩࡵࠫਙ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1111_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩਚ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111lll1l_opy_)
            lines.insert(1, bstack11ll11l1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1111_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨਛ")), bstack1111_opy_ (u"ࠬࡽࠧਜ")) as bstack1l1llllll_opy_:
              bstack1l1llllll_opy_.writelines(lines)
        CONFIG[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਝ")] = str(bstack1lll1l1ll_opy_) + str(__version__)
        bstack1ll111ll1_opy_ = 0 if bstack1llll11111_opy_ < 0 else bstack1llll11111_opy_
        try:
          if bstack1lll1l1l1_opy_ is True:
            bstack1ll111ll1_opy_ = int(multiprocessing.current_process().name)
          elif bstack11ll11111_opy_ is True:
            bstack1ll111ll1_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll111ll1_opy_ = 0
        CONFIG[bstack1111_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢਞ")] = False
        CONFIG[bstack1111_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢਟ")] = True
        bstack1ll11llll_opy_ = bstack1ll1ll1lll_opy_(CONFIG, bstack1ll111ll1_opy_)
        logger.debug(bstack111l1ll1_opy_.format(str(bstack1ll11llll_opy_)))
        if CONFIG.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਠ")):
          bstack1lll1l1111_opy_(bstack1ll11llll_opy_)
        if bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਡ") in CONFIG and bstack1111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਢ") in CONFIG[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਣ")][bstack1ll111ll1_opy_]:
          bstack1ll111lll_opy_ = CONFIG[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਤ")][bstack1ll111ll1_opy_][bstack1111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਥ")]
        args.append(os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠨࢀࠪਦ")), bstack1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਧ"), bstack1111_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਨ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11llll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1111_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਩"))
      bstack1lll111l1l_opy_ = True
      return bstack1l1l1111_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack11lll111_opy_(self,
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
    global bstack1llll11111_opy_
    global bstack1ll111lll_opy_
    global bstack1lll1l1l1_opy_
    global bstack11ll11111_opy_
    global bstack1lll1l1ll_opy_
    CONFIG[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਪ")] = str(bstack1lll1l1ll_opy_) + str(__version__)
    bstack1ll111ll1_opy_ = 0 if bstack1llll11111_opy_ < 0 else bstack1llll11111_opy_
    try:
      if bstack1lll1l1l1_opy_ is True:
        bstack1ll111ll1_opy_ = int(multiprocessing.current_process().name)
      elif bstack11ll11111_opy_ is True:
        bstack1ll111ll1_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll111ll1_opy_ = 0
    CONFIG[bstack1111_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਫ")] = True
    bstack1ll11llll_opy_ = bstack1ll1ll1lll_opy_(CONFIG, bstack1ll111ll1_opy_)
    logger.debug(bstack111l1ll1_opy_.format(str(bstack1ll11llll_opy_)))
    if CONFIG.get(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ")):
      bstack1lll1l1111_opy_(bstack1ll11llll_opy_)
    if bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਭ") in CONFIG and bstack1111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਮ") in CONFIG[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ")][bstack1ll111ll1_opy_]:
      bstack1ll111lll_opy_ = CONFIG[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")][bstack1ll111ll1_opy_][bstack1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ਱")]
    import urllib
    import json
    bstack111111lll_opy_ = bstack1111_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨਲ") + urllib.parse.quote(json.dumps(bstack1ll11llll_opy_))
    browser = self.connect(bstack111111lll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1llll111_opy_():
    global bstack1lll111l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11lll111_opy_
        bstack1lll111l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lllll1ll1_opy_
      bstack1lll111l1l_opy_ = True
    except Exception as e:
      pass
def bstack111ll111l_opy_(context, bstack11111l111_opy_):
  try:
    context.page.evaluate(bstack1111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣਲ਼"), bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ਴")+ json.dumps(bstack11111l111_opy_) + bstack1111_opy_ (u"ࠤࢀࢁࠧਵ"))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣਸ਼"), e)
def bstack1l1lll1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ਷"), bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪਸ") + json.dumps(message) + bstack1111_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩਹ") + json.dumps(level) + bstack1111_opy_ (u"ࠧࡾࡿࠪ਺"))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ਻"), e)
def bstack1l1ll1lll_opy_(context, status, message = bstack1111_opy_ (u"ࠤ਼ࠥ")):
  try:
    if(status == bstack1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ਽")):
      context.page.evaluate(bstack1111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧਾ"), bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿࠭ਿ") + json.dumps(bstack1111_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠࠣੀ") + str(message)) + bstack1111_opy_ (u"ࠧ࠭ࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠫੁ") + json.dumps(status) + bstack1111_opy_ (u"ࠣࡿࢀࠦੂ"))
    else:
      context.page.evaluate(bstack1111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ੃"), bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠫ੄") + json.dumps(status) + bstack1111_opy_ (u"ࠦࢂࢃࠢ੅"))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤ੆"), e)
def bstack111111l1l_opy_(self, url):
  global bstack1ll1ll1111_opy_
  try:
    bstack1ll111lll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1l111l111_opy_.format(str(err)))
  try:
    bstack1ll1ll1111_opy_(self, url)
  except Exception as e:
    try:
      bstack1l11ll1l1_opy_ = str(e)
      if any(err_msg in bstack1l11ll1l1_opy_ for err_msg in bstack1ll111l11_opy_):
        bstack1ll111lll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l111l111_opy_.format(str(err)))
    raise e
def bstack11l1111ll_opy_(self):
  global bstack1ll1111111_opy_
  bstack1ll1111111_opy_ = self
  return
def bstack11ll1l1l_opy_(self):
  global bstack1l1l1lll_opy_
  bstack1l1l1lll_opy_ = self
  return
def bstack1ll11l1l11_opy_(self, test):
  global CONFIG
  global bstack1l1l1lll_opy_
  global bstack1ll1111111_opy_
  global bstack1lll1ll1_opy_
  global bstack11l111111_opy_
  global bstack1ll111lll_opy_
  global bstack1ll11l1l_opy_
  global bstack11l111l11_opy_
  global bstack1l1l1ll11_opy_
  global bstack11lll1111_opy_
  try:
    if not bstack1lll1ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack1111_opy_ (u"࠭ࡾࠨੇ")), bstack1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧੈ"), bstack1111_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ੉"))) as f:
        bstack1lll111ll1_opy_ = json.loads(bstack1111_opy_ (u"ࠤࡾࠦ੊") + f.read().strip() + bstack1111_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬੋ") + bstack1111_opy_ (u"ࠦࢂࠨੌ"))
        bstack1lll1ll1_opy_ = bstack1lll111ll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11lll1111_opy_:
    for driver in bstack11lll1111_opy_:
      if bstack1lll1ll1_opy_ == driver.session_id:
        if test:
          bstack11l11llll_opy_ = str(test.data)
          if bstack1ll111l111_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵ੍ࠩ"), None):
            logger.info(bstack1111_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨ੎"))
            bstack111ll1l1l_opy_.bstack1ll1llll1l_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack111l1l1l_opy_={})
        if not bstack1ll1lll11_opy_ and bstack11l11llll_opy_:
          bstack1l1lll1ll_opy_ = {
            bstack1111_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ੏"): bstack1111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੐"),
            bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬੑ"): {
              bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ੒"): bstack11l11llll_opy_
            }
          }
          bstack1lll1l11ll_opy_ = bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੓").format(json.dumps(bstack1l1lll1ll_opy_))
          driver.execute_script(bstack1lll1l11ll_opy_)
        if bstack11l111111_opy_:
          bstack1ll11llll1_opy_ = {
            bstack1111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ੔"): bstack1111_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ੕"),
            bstack1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੖"): {
              bstack1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭੗"): bstack11l11llll_opy_ + bstack1111_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ੘"),
              bstack1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩਖ਼"): bstack1111_opy_ (u"ࠫ࡮ࡴࡦࡰࠩਗ਼")
            }
          }
          bstack1l1lll1ll_opy_ = {
            bstack1111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬਜ਼"): bstack1111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩੜ"),
            bstack1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੝"): {
              bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨਫ਼"): bstack1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੟")
            }
          }
          if bstack11l111111_opy_.status == bstack1111_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ੠"):
            bstack1ll111l1_opy_ = bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੡").format(json.dumps(bstack1ll11llll1_opy_))
            driver.execute_script(bstack1ll111l1_opy_)
            bstack1lll1l11ll_opy_ = bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ੢").format(json.dumps(bstack1l1lll1ll_opy_))
            driver.execute_script(bstack1lll1l11ll_opy_)
          elif bstack11l111111_opy_.status == bstack1111_opy_ (u"࠭ࡆࡂࡋࡏࠫ੣"):
            reason = bstack1111_opy_ (u"ࠢࠣ੤")
            bstack1l1lll111_opy_ = bstack11l11llll_opy_ + bstack1111_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩ੥")
            if bstack11l111111_opy_.message:
              reason = str(bstack11l111111_opy_.message)
              bstack1l1lll111_opy_ = bstack1l1lll111_opy_ + bstack1111_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ੦") + reason
            bstack1ll11llll1_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੧")] = {
              bstack1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ੨"): bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ੩"),
              bstack1111_opy_ (u"࠭ࡤࡢࡶࡤࠫ੪"): bstack1l1lll111_opy_
            }
            bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੫")] = {
              bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੬"): bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ੭"),
              bstack1111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ੮"): reason
            }
            bstack1ll111l1_opy_ = bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੯").format(json.dumps(bstack1ll11llll1_opy_))
            driver.execute_script(bstack1ll111l1_opy_)
            bstack1lll1l11ll_opy_ = bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪੰ").format(json.dumps(bstack1l1lll1ll_opy_))
            driver.execute_script(bstack1lll1l11ll_opy_)
            bstack1l11l111_opy_(reason, str(bstack11l111111_opy_), str(bstack1llll11111_opy_), logger)
  elif bstack1lll1ll1_opy_:
    try:
      data = {}
      bstack11l11llll_opy_ = None
      if test:
        bstack11l11llll_opy_ = str(test.data)
      if not bstack1ll1lll11_opy_ and bstack11l11llll_opy_:
        data[bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫੱ")] = bstack11l11llll_opy_
      if bstack11l111111_opy_:
        if bstack11l111111_opy_.status == bstack1111_opy_ (u"ࠧࡑࡃࡖࡗࠬੲ"):
          data[bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨੳ")] = bstack1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩੴ")
        elif bstack11l111111_opy_.status == bstack1111_opy_ (u"ࠪࡊࡆࡏࡌࠨੵ"):
          data[bstack1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੶")] = bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੷")
          if bstack11l111111_opy_.message:
            data[bstack1111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭੸")] = str(bstack11l111111_opy_.message)
      user = CONFIG[bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ੹")]
      key = CONFIG[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ੺")]
      url = bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ੻").format(user, key, bstack1lll1ll1_opy_)
      headers = {
        bstack1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ੼"): bstack1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ੽"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11lll11ll_opy_.format(str(e)))
  if bstack1l1l1lll_opy_:
    bstack11l111l11_opy_(bstack1l1l1lll_opy_)
  if bstack1ll1111111_opy_:
    bstack1l1l1ll11_opy_(bstack1ll1111111_opy_)
  bstack1ll11l1l_opy_(self, test)
def bstack1l11ll11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll11lll_opy_
  global CONFIG
  global bstack11lll1111_opy_
  global bstack1lll1ll1_opy_
  bstack1lllll1l11_opy_ = None
  try:
    if bstack1ll111l111_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ੾"), None):
      try:
        if not bstack1lll1ll1_opy_:
          with open(os.path.join(os.path.expanduser(bstack1111_opy_ (u"࠭ࡾࠨ੿")), bstack1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઀"), bstack1111_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪઁ"))) as f:
            bstack1lll111ll1_opy_ = json.loads(bstack1111_opy_ (u"ࠤࡾࠦં") + f.read().strip() + bstack1111_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬઃ") + bstack1111_opy_ (u"ࠦࢂࠨ઄"))
            bstack1lll1ll1_opy_ = bstack1lll111ll1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11lll1111_opy_:
        for driver in bstack11lll1111_opy_:
          if bstack1lll1ll1_opy_ == driver.session_id:
            bstack1lllll1l11_opy_ = driver
    bstack1lll11l1ll_opy_ = bstack111ll1l1l_opy_.bstack11lll11l_opy_(CONFIG, test.tags)
    if bstack1lllll1l11_opy_:
      threading.current_thread().isA11yTest = bstack111ll1l1l_opy_.bstack111lll1l1_opy_(bstack1lllll1l11_opy_, bstack1lll11l1ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lll11l1ll_opy_
  except:
    pass
  bstack1lll11lll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l111111_opy_
  bstack11l111111_opy_ = self._test
def bstack1ll1lll11l_opy_():
  global bstack11lll111l_opy_
  try:
    if os.path.exists(bstack11lll111l_opy_):
      os.remove(bstack11lll111l_opy_)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨઅ") + str(e))
def bstack1l11lll11_opy_():
  global bstack11lll111l_opy_
  bstack11llll1l_opy_ = {}
  try:
    if not os.path.isfile(bstack11lll111l_opy_):
      with open(bstack11lll111l_opy_, bstack1111_opy_ (u"࠭ࡷࠨઆ")):
        pass
      with open(bstack11lll111l_opy_, bstack1111_opy_ (u"ࠢࡸ࠭ࠥઇ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11lll111l_opy_):
      bstack11llll1l_opy_ = json.load(open(bstack11lll111l_opy_, bstack1111_opy_ (u"ࠨࡴࡥࠫઈ")))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઉ") + str(e))
  finally:
    return bstack11llll1l_opy_
def bstack1111ll1ll_opy_(platform_index, item_index):
  global bstack11lll111l_opy_
  try:
    bstack11llll1l_opy_ = bstack1l11lll11_opy_()
    bstack11llll1l_opy_[item_index] = platform_index
    with open(bstack11lll111l_opy_, bstack1111_opy_ (u"ࠥࡻ࠰ࠨઊ")) as outfile:
      json.dump(bstack11llll1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩઋ") + str(e))
def bstack11lll1lll_opy_(bstack111llll1l_opy_):
  global CONFIG
  bstack1111ll1l_opy_ = bstack1111_opy_ (u"ࠬ࠭ઌ")
  if not bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩઍ") in CONFIG:
    logger.info(bstack1111_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫ઎"))
  try:
    platform = CONFIG[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫએ")][bstack111llll1l_opy_]
    if bstack1111_opy_ (u"ࠩࡲࡷࠬઐ") in platform:
      bstack1111ll1l_opy_ += str(platform[bstack1111_opy_ (u"ࠪࡳࡸ࠭ઑ")]) + bstack1111_opy_ (u"ࠫ࠱ࠦࠧ઒")
    if bstack1111_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઓ") in platform:
      bstack1111ll1l_opy_ += str(platform[bstack1111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩઔ")]) + bstack1111_opy_ (u"ࠧ࠭ࠢࠪક")
    if bstack1111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬખ") in platform:
      bstack1111ll1l_opy_ += str(platform[bstack1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ગ")]) + bstack1111_opy_ (u"ࠪ࠰ࠥ࠭ઘ")
    if bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ઙ") in platform:
      bstack1111ll1l_opy_ += str(platform[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧચ")]) + bstack1111_opy_ (u"࠭ࠬࠡࠩછ")
    if bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬજ") in platform:
      bstack1111ll1l_opy_ += str(platform[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ઝ")]) + bstack1111_opy_ (u"ࠩ࠯ࠤࠬઞ")
    if bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫટ") in platform:
      bstack1111ll1l_opy_ += str(platform[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬઠ")]) + bstack1111_opy_ (u"ࠬ࠲ࠠࠨડ")
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ઢ") + str(e))
  finally:
    if bstack1111ll1l_opy_[len(bstack1111ll1l_opy_) - 2:] == bstack1111_opy_ (u"ࠧ࠭ࠢࠪણ"):
      bstack1111ll1l_opy_ = bstack1111ll1l_opy_[:-2]
    return bstack1111ll1l_opy_
def bstack1ll1l11l_opy_(path, bstack1111ll1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l11llll1_opy_ = ET.parse(path)
    bstack1lllll111l_opy_ = bstack1l11llll1_opy_.getroot()
    bstack1111l1l1l_opy_ = None
    for suite in bstack1lllll111l_opy_.iter(bstack1111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧત")):
      if bstack1111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩથ") in suite.attrib:
        suite.attrib[bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨદ")] += bstack1111_opy_ (u"ࠫࠥ࠭ધ") + bstack1111ll1l_opy_
        bstack1111l1l1l_opy_ = suite
    bstack1ll1l111l_opy_ = None
    for robot in bstack1lllll111l_opy_.iter(bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫન")):
      bstack1ll1l111l_opy_ = robot
    bstack1lll1ll1l1_opy_ = len(bstack1ll1l111l_opy_.findall(bstack1111_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ઩")))
    if bstack1lll1ll1l1_opy_ == 1:
      bstack1ll1l111l_opy_.remove(bstack1ll1l111l_opy_.findall(bstack1111_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭પ"))[0])
      bstack1l11l1111_opy_ = ET.Element(bstack1111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ"), attrib={bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧબ"): bstack1111_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪભ"), bstack1111_opy_ (u"ࠫ࡮ࡪࠧમ"): bstack1111_opy_ (u"ࠬࡹ࠰ࠨય")})
      bstack1ll1l111l_opy_.insert(1, bstack1l11l1111_opy_)
      bstack1lll1llll_opy_ = None
      for suite in bstack1ll1l111l_opy_.iter(bstack1111_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬર")):
        bstack1lll1llll_opy_ = suite
      bstack1lll1llll_opy_.append(bstack1111l1l1l_opy_)
      bstack111llll1_opy_ = None
      for status in bstack1111l1l1l_opy_.iter(bstack1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ઱")):
        bstack111llll1_opy_ = status
      bstack1lll1llll_opy_.append(bstack111llll1_opy_)
    bstack1l11llll1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭લ") + str(e))
def bstack1llll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l11l11_opy_
  global CONFIG
  if bstack1111_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨળ") in options:
    del options[bstack1111_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ઴")]
  bstack1111l11l1_opy_ = bstack1l11lll11_opy_()
  for bstack1llll1111_opy_ in bstack1111l11l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1111_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫવ"), str(bstack1llll1111_opy_), bstack1111_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩશ"))
    bstack1ll1l11l_opy_(path, bstack11lll1lll_opy_(bstack1111l11l1_opy_[bstack1llll1111_opy_]))
  bstack1ll1lll11l_opy_()
  return bstack1l1l11l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111l11l1l_opy_(self, ff_profile_dir):
  global bstack1ll11ll111_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll11ll111_opy_(self, ff_profile_dir)
def bstack1lll11ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll1ll1l11_opy_
  bstack111l11ll_opy_ = []
  if bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩષ") in CONFIG:
    bstack111l11ll_opy_ = CONFIG[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤહ")],
      pabot_args[bstack1111_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥ઺")],
      argfile,
      pabot_args.get(bstack1111_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ઻")),
      pabot_args[bstack1111_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹ઼ࠢ")],
      platform[0],
      bstack1ll1ll1l11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1111_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧઽ")] or [(bstack1111_opy_ (u"ࠨࠢા"), None)]
    for platform in enumerate(bstack111l11ll_opy_)
  ]
def bstack11l1lll1l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l11ll1ll_opy_=bstack1111_opy_ (u"ࠧࠨિ")):
  global bstack11llll1l1_opy_
  self.platform_index = platform_index
  self.bstack111l1l11l_opy_ = bstack1l11ll1ll_opy_
  bstack11llll1l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1llll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1ll1l1_opy_
  global bstack1l111l11_opy_
  if not bstack1111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪી") in item.options:
    item.options[bstack1111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫુ")] = []
  for v in item.options[bstack1111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ")]:
    if bstack1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪૃ") in v:
      item.options[bstack1111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")].remove(v)
    if bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ૅ") in v:
      item.options[bstack1111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")].remove(v)
  item.options[bstack1111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪે")].insert(0, bstack1111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫૈ").format(item.platform_index))
  item.options[bstack1111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૉ")].insert(0, bstack1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ૊").format(item.bstack111l1l11l_opy_))
  if bstack1l111l11_opy_:
    item.options[bstack1111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧો")].insert(0, bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩૌ").format(bstack1l111l11_opy_))
  return bstack1ll1ll1l1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11l11l111_opy_(command, item_index):
  os.environ[bstack1111_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ્")] = json.dumps(CONFIG[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૎")][item_index % bstack1ll11lll1_opy_])
  global bstack1l111l11_opy_
  if bstack1l111l11_opy_:
    command[0] = command[0].replace(bstack1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૏"), bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧૐ") + str(
      item_index) + bstack1111_opy_ (u"ࠫࠥ࠭૑") + bstack1l111l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૒"),
                                    bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ૓") + str(item_index), 1)
def bstack1lll1111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11lll11l1_opy_
  bstack11l11l111_opy_(command, item_index)
  return bstack11lll11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1llll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11lll11l1_opy_
  bstack11l11l111_opy_(command, item_index)
  return bstack11lll11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11lll11l1_opy_
  bstack11l11l111_opy_(command, item_index)
  return bstack11lll11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1lll11l1l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1l1ll1_opy_
  bstack11l1ll1l1_opy_ = bstack1ll1l1ll1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1111_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ૔")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1111_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ૕")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11l1ll1l1_opy_
def bstack11ll11ll1_opy_(self, name, context, *args):
  os.environ[bstack1111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૖")] = json.dumps(CONFIG[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૗")][int(threading.current_thread()._name) % bstack1ll11lll1_opy_])
  global bstack1l111111_opy_
  if name == bstack1111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૘"):
    bstack1l111111_opy_(self, name, context, *args)
    try:
      if not bstack1ll1lll11_opy_:
        bstack1lllll1l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1ll1_opy_(bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૙")) else context.browser
        bstack11111l111_opy_ = str(self.feature.name)
        bstack111ll111l_opy_(context, bstack11111l111_opy_)
        bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૚") + json.dumps(bstack11111l111_opy_) + bstack1111_opy_ (u"ࠧࡾࡿࠪ૛"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ૜").format(str(e)))
  elif name == bstack1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૝"):
    bstack1l111111_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૞")):
        self.driver_before_scenario = True
      if (not bstack1ll1lll11_opy_):
        scenario_name = args[0].name
        feature_name = bstack11111l111_opy_ = str(self.feature.name)
        bstack11111l111_opy_ = feature_name + bstack1111_opy_ (u"ࠫࠥ࠳ࠠࠨ૟") + scenario_name
        bstack1lllll1l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1ll1_opy_(bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫૠ")) else context.browser
        if self.driver_before_scenario:
          bstack111ll111l_opy_(context, bstack11111l111_opy_)
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫૡ") + json.dumps(bstack11111l111_opy_) + bstack1111_opy_ (u"ࠧࡾࡿࠪૢ"))
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩૣ").format(str(e)))
  elif name == bstack1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૤"):
    try:
      bstack1lllll111_opy_ = args[0].status.name
      bstack1lllll1l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૥") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1lllll111_opy_).lower() == bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૦"):
        bstack11l111ll1_opy_ = bstack1111_opy_ (u"ࠬ࠭૧")
        bstack1111l1ll1_opy_ = bstack1111_opy_ (u"࠭ࠧ૨")
        bstack1llll1l11_opy_ = bstack1111_opy_ (u"ࠧࠨ૩")
        try:
          import traceback
          bstack11l111ll1_opy_ = self.exception.__class__.__name__
          bstack1l1lllll1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1111l1ll1_opy_ = bstack1111_opy_ (u"ࠨࠢࠪ૪").join(bstack1l1lllll1l_opy_)
          bstack1llll1l11_opy_ = bstack1l1lllll1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll1111ll_opy_.format(str(e)))
        bstack11l111ll1_opy_ += bstack1llll1l11_opy_
        bstack1l1lll1l_opy_(context, json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૫") + str(bstack1111l1ll1_opy_)),
                            bstack1111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ૬"))
        if self.driver_before_scenario:
          bstack1l1ll1lll_opy_(context, bstack1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ૭"), bstack11l111ll1_opy_)
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ૮") + json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ૯") + str(bstack1111l1ll1_opy_)) + bstack1111_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ૰"))
        if self.driver_before_scenario:
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨ૱") + json.dumps(bstack1111_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ૲") + str(bstack11l111ll1_opy_)) + bstack1111_opy_ (u"ࠪࢁࢂ࠭૳"))
      else:
        bstack1l1lll1l_opy_(context, bstack1111_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧ૴"), bstack1111_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ૵"))
        if self.driver_before_scenario:
          bstack1l1ll1lll_opy_(context, bstack1111_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ૶"))
        bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ૷") + json.dumps(str(args[0].name) + bstack1111_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ૸")) + bstack1111_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨૹ"))
        if self.driver_before_scenario:
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦࡵࡧࡳࡴࡧࡧࠦࢂࢃࠧૺ"))
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ૻ").format(str(e)))
  elif name == bstack1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬૼ"):
    try:
      bstack1lllll1l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1ll1_opy_(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ૽")) else context.browser
      if context.failed is True:
        bstack1lll1l11l1_opy_ = []
        bstack1llll11lll_opy_ = []
        bstack111l1ll1l_opy_ = []
        bstack1l1l1l1l1_opy_ = bstack1111_opy_ (u"ࠧࠨ૾")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1lll1l11l1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l1lllll1l_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1l1ll1l_opy_ = bstack1111_opy_ (u"ࠨࠢࠪ૿").join(bstack1l1lllll1l_opy_)
            bstack1llll11lll_opy_.append(bstack1ll1l1ll1l_opy_)
            bstack111l1ll1l_opy_.append(bstack1l1lllll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1111ll_opy_.format(str(e)))
        bstack11l111ll1_opy_ = bstack1111_opy_ (u"ࠩࠪ଀")
        for i in range(len(bstack1lll1l11l1_opy_)):
          bstack11l111ll1_opy_ += bstack1lll1l11l1_opy_[i] + bstack111l1ll1l_opy_[i] + bstack1111_opy_ (u"ࠪࡠࡳ࠭ଁ")
        bstack1l1l1l1l1_opy_ = bstack1111_opy_ (u"ࠫࠥ࠭ଂ").join(bstack1llll11lll_opy_)
        if not self.driver_before_scenario:
          bstack1l1lll1l_opy_(context, bstack1l1l1l1l1_opy_, bstack1111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦଃ"))
          bstack1l1ll1lll_opy_(context, bstack1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ଄"), bstack11l111ll1_opy_)
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଅ") + json.dumps(bstack1l1l1l1l1_opy_) + bstack1111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨଆ"))
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩଇ") + json.dumps(bstack1111_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣଈ") + str(bstack11l111ll1_opy_)) + bstack1111_opy_ (u"ࠫࢂࢃࠧଉ"))
          bstack1llllll11_opy_ = bstack1l111l11l_opy_(bstack1l1l1l1l1_opy_, self.feature.name, logger)
          if (bstack1llllll11_opy_ != None):
            bstack111ll1lll_opy_.append(bstack1llllll11_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1l1lll1l_opy_(context, bstack1111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣଊ") + str(self.feature.name) + bstack1111_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣଋ"), bstack1111_opy_ (u"ࠢࡪࡰࡩࡳࠧଌ"))
          bstack1l1ll1lll_opy_(context, bstack1111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ଍"))
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ଎") + json.dumps(bstack1111_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨଏ") + str(self.feature.name) + bstack1111_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨଐ")) + bstack1111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ଑"))
          bstack1lllll1l11_opy_.execute_script(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ଒"))
          bstack1llllll11_opy_ = bstack1l111l11l_opy_(bstack1l1l1l1l1_opy_, self.feature.name, logger)
          if (bstack1llllll11_opy_ != None):
            bstack111ll1lll_opy_.append(bstack1llllll11_opy_)
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩଓ").format(str(e)))
  else:
    bstack1l111111_opy_(self, name, context, *args)
  if name in [bstack1111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨଔ"), bstack1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪକ")]:
    bstack1l111111_opy_(self, name, context, *args)
    if (name == bstack1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫଖ") and self.driver_before_scenario) or (
            name == bstack1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଗ") and not self.driver_before_scenario):
      try:
        bstack1lllll1l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1ll1ll1_opy_(bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଘ")) else context.browser
        bstack1lllll1l11_opy_.quit()
      except Exception:
        pass
def bstack1ll11111ll_opy_(config, startdir):
  return bstack1111_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦଙ").format(bstack1111_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨଚ"))
notset = Notset()
def bstack111lll11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1111l11l_opy_
  if str(name).lower() == bstack1111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨଛ"):
    return bstack1111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣଜ")
  else:
    return bstack1111l11l_opy_(self, name, default, skip)
def bstack1llll11ll_opy_(item, when):
  global bstack111llll11_opy_
  try:
    bstack111llll11_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll1l11lll_opy_():
  return
def bstack1llll1lll1_opy_(type, name, status, reason, bstack111l1l1l1_opy_, bstack1lll1ll11_opy_):
  bstack1l1lll1ll_opy_ = {
    bstack1111_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪଝ"): type,
    bstack1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଞ"): {}
  }
  if type == bstack1111_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧଟ"):
    bstack1l1lll1ll_opy_[bstack1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଠ")][bstack1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଡ")] = bstack111l1l1l1_opy_
    bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଢ")][bstack1111_opy_ (u"ࠩࡧࡥࡹࡧࠧଣ")] = json.dumps(str(bstack1lll1ll11_opy_))
  if type == bstack1111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫତ"):
    bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଥ")][bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪଦ")] = name
  if type == bstack1111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩଧ"):
    bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪନ")][bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ଩")] = status
    if status == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩପ"):
      bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଫ")][bstack1111_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫବ")] = json.dumps(str(reason))
  bstack1lll1l11ll_opy_ = bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪଭ").format(json.dumps(bstack1l1lll1ll_opy_))
  return bstack1lll1l11ll_opy_
def bstack1l11l1l11_opy_(item, call, rep):
  global bstack11111l11_opy_
  global bstack11lll1111_opy_
  global bstack1ll1lll11_opy_
  name = bstack1111_opy_ (u"࠭ࠧମ")
  try:
    if rep.when == bstack1111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬଯ"):
      bstack1lll1ll1_opy_ = threading.current_thread().bstack1ll1l11l1l_opy_
      try:
        if not bstack1ll1lll11_opy_:
          name = str(rep.nodeid)
          bstack11l11l11_opy_ = bstack1llll1lll1_opy_(bstack1111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩର"), name, bstack1111_opy_ (u"ࠩࠪ଱"), bstack1111_opy_ (u"ࠪࠫଲ"), bstack1111_opy_ (u"ࠫࠬଳ"), bstack1111_opy_ (u"ࠬ࠭଴"))
          threading.current_thread().bstack1111111l_opy_ = name
          for driver in bstack11lll1111_opy_:
            if bstack1lll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack11l11l11_opy_)
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ଵ").format(str(e)))
      try:
        bstack111l11ll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨଶ"):
          status = bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଷ") if rep.outcome.lower() == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩସ") else bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪହ")
          reason = bstack1111_opy_ (u"ࠫࠬ଺")
          if status == bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ଻"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1111_opy_ (u"࠭ࡩ࡯ࡨࡲ଼ࠫ") if status == bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଽ") else bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧା")
          data = name + bstack1111_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫି") if status == bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪୀ") else name + bstack1111_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧୁ") + reason
          bstack1l11lll1_opy_ = bstack1llll1lll1_opy_(bstack1111_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧୂ"), bstack1111_opy_ (u"࠭ࠧୃ"), bstack1111_opy_ (u"ࠧࠨୄ"), bstack1111_opy_ (u"ࠨࠩ୅"), level, data)
          for driver in bstack11lll1111_opy_:
            if bstack1lll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1l11lll1_opy_)
      except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭୆").format(str(e)))
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧେ").format(str(e)))
  bstack11111l11_opy_(item, call, rep)
def bstack1ll1lll1l1_opy_(framework_name):
  global bstack1lll1l1ll_opy_
  global bstack1lll111l1l_opy_
  global bstack1l1ll111_opy_
  bstack1lll1l1ll_opy_ = framework_name
  logger.info(bstack11lll1l11_opy_.format(bstack1lll1l1ll_opy_.split(bstack1111_opy_ (u"ࠫ࠲࠭ୈ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11111llll_opy_:
      Service.start = bstack11l1ll11_opy_
      Service.stop = bstack11l11111l_opy_
      webdriver.Remote.get = bstack111111l1l_opy_
      WebDriver.close = bstack1l1l111l1_opy_
      WebDriver.quit = bstack1l1ll11ll_opy_
      webdriver.Remote.__init__ = bstack11111l11l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1lll111ll_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1l1l11111_opy_ = getAccessibilityResultsSummary
    if not bstack11111llll_opy_ and bstack1l1lll11l_opy_.on():
      webdriver.Remote.__init__ = bstack1l1l11l1l_opy_
    bstack1lll111l1l_opy_ = True
  except Exception as e:
    pass
  bstack1l1llll111_opy_()
  if not bstack1lll111l1l_opy_:
    bstack1ll1l1l111_opy_(bstack1111_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ୉"), bstack1l1llll1l_opy_)
  if bstack1lllll11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111l11l1_opy_
    except Exception as e:
      logger.error(bstack1ll111ll11_opy_.format(str(e)))
  if bstack111lllll1_opy_():
    bstack11l1l111_opy_(CONFIG, logger)
  if (bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ୊") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack111l11l1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11ll1l1l_opy_
      except Exception as e:
        logger.warn(bstack1ll11ll1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11l1111ll_opy_
      except Exception as e:
        logger.debug(bstack1lllllll11_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll11ll1l1_opy_)
    Output.end_test = bstack1ll11l1l11_opy_
    TestStatus.__init__ = bstack1l11ll11_opy_
    QueueItem.__init__ = bstack11l1lll1l_opy_
    pabot._create_items = bstack1lll11ll_opy_
    try:
      from pabot import __version__ as bstack11111ll11_opy_
      if version.parse(bstack11111ll11_opy_) >= version.parse(bstack1111_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧୋ")):
        pabot._run = bstack1llll1l111_opy_
      elif version.parse(bstack11111ll11_opy_) >= version.parse(bstack1111_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨୌ")):
        pabot._run = bstack1llll1ll1l_opy_
      else:
        pabot._run = bstack1lll1111l1_opy_
    except Exception as e:
      pabot._run = bstack1lll1111l1_opy_
    pabot._create_command_for_execution = bstack1l1llll1_opy_
    pabot._report_results = bstack1llll11l1_opy_
  if bstack1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ୍ࠩ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll1111lll_opy_)
    Runner.run_hook = bstack11ll11ll1_opy_
    Step.run = bstack1lll11l1l1_opy_
  if bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ୎") in str(framework_name).lower():
    if not bstack11111llll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll11111ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll1l11lll_opy_
      Config.getoption = bstack111lll11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l11l1l11_opy_
    except Exception as e:
      pass
def bstack11l11111_opy_():
  global CONFIG
  if bstack1111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ୏") in CONFIG and int(CONFIG[bstack1111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ୐")]) > 1:
    logger.warn(bstack1lll1111_opy_)
def bstack1ll11l1lll_opy_(arg, bstack11111111l_opy_, bstack1111l1l1_opy_=None):
  global CONFIG
  global bstack11l11l11l_opy_
  global bstack11llll11_opy_
  global bstack11111llll_opy_
  global bstack1llll1l1ll_opy_
  bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭୑")
  if bstack11111111l_opy_ and isinstance(bstack11111111l_opy_, str):
    bstack11111111l_opy_ = eval(bstack11111111l_opy_)
  CONFIG = bstack11111111l_opy_[bstack1111_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ୒")]
  bstack11l11l11l_opy_ = bstack11111111l_opy_[bstack1111_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ୓")]
  bstack11llll11_opy_ = bstack11111111l_opy_[bstack1111_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ୔")]
  bstack11111llll_opy_ = bstack11111111l_opy_[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭୕")]
  bstack1llll1l1ll_opy_.bstack111l1111_opy_(bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬୖ"), bstack11111llll_opy_)
  os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧୗ")] = bstack1ll1l1ll11_opy_
  os.environ[bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ୘")] = json.dumps(CONFIG)
  os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ୙")] = bstack11l11l11l_opy_
  os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ୚")] = str(bstack11llll11_opy_)
  os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨ୛")] = str(True)
  if bstack1ll1l1l11_opy_(arg, [bstack1111_opy_ (u"ࠪ࠱ࡳ࠭ଡ଼"), bstack1111_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬଢ଼")]) != -1:
    os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭୞")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111l111l_opy_)
    return
  bstack11lllllll_opy_()
  global bstack1lll11111l_opy_
  global bstack1llll11111_opy_
  global bstack1ll1ll1l11_opy_
  global bstack1l111l11_opy_
  global bstack1ll1llllll_opy_
  global bstack1l1ll111_opy_
  global bstack1lll1l1l1_opy_
  arg.append(bstack1111_opy_ (u"ࠨ࠭ࡘࠤୟ"))
  arg.append(bstack1111_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥୠ"))
  arg.append(bstack1111_opy_ (u"ࠣ࠯࡚ࠦୡ"))
  arg.append(bstack1111_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣୢ"))
  global bstack1l1ll1l11_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1lll11lll_opy_
  global bstack1ll11ll111_opy_
  global bstack11llll1l1_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11l1111l1_opy_
  global bstack1ll1ll1111_opy_
  global bstack1ll11l1ll_opy_
  global bstack1111l11l_opy_
  global bstack111llll11_opy_
  global bstack11111l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1ll1l11_opy_ = webdriver.Remote.__init__
    bstack1ll1l1l1l_opy_ = WebDriver.quit
    bstack11l1111l1_opy_ = WebDriver.close
    bstack1ll1ll1111_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1l1l11ll1_opy_(CONFIG) and bstack1111ll111_opy_():
    if bstack1llll1ll1_opy_() < version.parse(bstack111111111_opy_):
      logger.error(bstack1l1ll1l1l_opy_.format(bstack1llll1ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll11l1ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll111ll11_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1111l11l_opy_ = Config.getoption
    from _pytest import runner
    bstack111llll11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack111lllll_opy_)
  try:
    from pytest_bdd import reporting
    bstack11111l11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1111_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫୣ"))
  bstack1ll1ll1l11_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ୤"), {}).get(bstack1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ୥"))
  bstack1lll1l1l1_opy_ = True
  bstack1ll1lll1l1_opy_(bstack1l11l11ll_opy_)
  os.environ[bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ୦")] = CONFIG[bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ୧")]
  os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ୨")] = CONFIG[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ୩")]
  os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭୪")] = bstack11111llll_opy_.__str__()
  from _pytest.config import main as bstack1ll1ll111_opy_
  bstack1ll1ll111_opy_(arg)
  if bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ୫") in multiprocessing.current_process().__dict__.keys():
    for bstack11lll1l1l_opy_ in multiprocessing.current_process().bstack1l1lll1l1_opy_:
      bstack1111l1l1_opy_.append(bstack11lll1l1l_opy_)
def bstack1l1111ll1_opy_(arg):
  bstack1ll1lll1l1_opy_(bstack11ll111l_opy_)
  os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭୬")] = str(bstack11llll11_opy_)
  from behave.__main__ import main as bstack1ll1l111_opy_
  bstack1ll1l111_opy_(arg)
def bstack1lll111lll_opy_():
  logger.info(bstack1lll1l1l11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ୭"), help=bstack1111_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨ୮"))
  parser.add_argument(bstack1111_opy_ (u"ࠨ࠯ࡸࠫ୯"), bstack1111_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭୰"), help=bstack1111_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩୱ"))
  parser.add_argument(bstack1111_opy_ (u"ࠫ࠲ࡱࠧ୲"), bstack1111_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫ୳"), help=bstack1111_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧ୴"))
  parser.add_argument(bstack1111_opy_ (u"ࠧ࠮ࡨࠪ୵"), bstack1111_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭୶"), help=bstack1111_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ୷"))
  bstack11l1ll111_opy_ = parser.parse_args()
  try:
    bstack1l11l1l1_opy_ = bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ୸")
    if bstack11l1ll111_opy_.framework and bstack11l1ll111_opy_.framework not in (bstack1111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ୹"), bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭୺")):
      bstack1l11l1l1_opy_ = bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬ୻")
    bstack11ll11lll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11l1l1_opy_)
    bstack1l1111l1l_opy_ = open(bstack11ll11lll_opy_, bstack1111_opy_ (u"ࠧࡳࠩ୼"))
    bstack11l1lll1_opy_ = bstack1l1111l1l_opy_.read()
    bstack1l1111l1l_opy_.close()
    if bstack11l1ll111_opy_.username:
      bstack11l1lll1_opy_ = bstack11l1lll1_opy_.replace(bstack1111_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ୽"), bstack11l1ll111_opy_.username)
    if bstack11l1ll111_opy_.key:
      bstack11l1lll1_opy_ = bstack11l1lll1_opy_.replace(bstack1111_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ୾"), bstack11l1ll111_opy_.key)
    if bstack11l1ll111_opy_.framework:
      bstack11l1lll1_opy_ = bstack11l1lll1_opy_.replace(bstack1111_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ୿"), bstack11l1ll111_opy_.framework)
    file_name = bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧ஀")
    file_path = os.path.abspath(file_name)
    bstack1l111111l_opy_ = open(file_path, bstack1111_opy_ (u"ࠬࡽࠧ஁"))
    bstack1l111111l_opy_.write(bstack11l1lll1_opy_)
    bstack1l111111l_opy_.close()
    logger.info(bstack1ll11l11ll_opy_)
    try:
      os.environ[bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨஂ")] = bstack11l1ll111_opy_.framework if bstack11l1ll111_opy_.framework != None else bstack1111_opy_ (u"ࠢࠣஃ")
      config = yaml.safe_load(bstack11l1lll1_opy_)
      config[bstack1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ஄")] = bstack1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨஅ")
      bstack1l1ll11l_opy_(bstack11lll1ll_opy_, config)
    except Exception as e:
      logger.debug(bstack11l1llll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll1l1lll_opy_.format(str(e)))
def bstack1l1ll11l_opy_(bstack1ll1l1111l_opy_, config, bstack1ll1111l1_opy_={}):
  global bstack11111llll_opy_
  global bstack1l1ll111l_opy_
  if not config:
    return
  bstack1ll11111_opy_ = bstack1lllll1l1_opy_ if not bstack11111llll_opy_ else (
    bstack1l1lllllll_opy_ if bstack1111_opy_ (u"ࠪࡥࡵࡶࠧஆ") in config else bstack11l11l1l_opy_)
  data = {
    bstack1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭இ"): config[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧஈ")],
    bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩஉ"): config[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪஊ")],
    bstack1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ஋"): bstack1ll1l1111l_opy_,
    bstack1111_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭஌"): os.environ.get(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ஍"), bstack1l1ll111l_opy_),
    bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭எ"): bstack1lllllllll_opy_,
    bstack1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧஏ"): bstack1llll1l1_opy_(),
    bstack1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩஐ"): {
      bstack1111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ஑"): str(config[bstack1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨஒ")]) if bstack1111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩஓ") in config else bstack1111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦஔ"),
      bstack1111_opy_ (u"ࠫࡷ࡫ࡦࡦࡴࡵࡩࡷ࠭க"): bstack1lll11111_opy_(os.getenv(bstack1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢ஖"), bstack1111_opy_ (u"ࠨࠢ஗"))),
      bstack1111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ஘"): bstack1111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨங"),
      bstack1111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪச"): bstack1ll11111_opy_,
      bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭஛"): config[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧஜ")] if config[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ஝")] else bstack1111_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢஞ"),
      bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩட"): str(config[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ஠")]) if bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ஡") in config else bstack1111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ஢"),
      bstack1111_opy_ (u"ࠫࡴࡹࠧண"): sys.platform,
      bstack1111_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧத"): socket.gethostname()
    }
  }
  update(data[bstack1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ஥")], bstack1ll1111l1_opy_)
  try:
    response = bstack1ll1111l_opy_(bstack1111_opy_ (u"ࠧࡑࡑࡖࡘࠬ஦"), bstack1ll11l11_opy_(bstack1lll1l111l_opy_), data, {
      bstack1111_opy_ (u"ࠨࡣࡸࡸ࡭࠭஧"): (config[bstack1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫந")], config[bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ன")])
    })
    if response:
      logger.debug(bstack1l1l11l1_opy_.format(bstack1ll1l1111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111l1l111_opy_.format(str(e)))
def bstack1lll11111_opy_(framework):
  return bstack1111_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣப").format(str(framework), __version__) if framework else bstack1111_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ஫").format(
    __version__)
def bstack11lllllll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l1l1ll1_opy_()
    logger.debug(bstack1l1111l1_opy_.format(str(CONFIG)))
    bstack111l111ll_opy_()
    bstack1111l1111_opy_()
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ஬") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11l1l1l1l_opy_
  atexit.register(bstack1llllll111_opy_)
  signal.signal(signal.SIGINT, bstack111l1l1ll_opy_)
  signal.signal(signal.SIGTERM, bstack111l1l1ll_opy_)
def bstack11l1l1l1l_opy_(exctype, value, traceback):
  global bstack11lll1111_opy_
  try:
    for driver in bstack11lll1111_opy_:
      driver.execute_script(
        bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧ஭") + json.dumps(
          bstack1111_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦம") + str(value)) + bstack1111_opy_ (u"ࠩࢀࢁࠬய"))
  except Exception:
    pass
  bstack1lllll11l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lllll11l_opy_(message=bstack1111_opy_ (u"ࠪࠫர")):
  global CONFIG
  try:
    if message:
      bstack1ll1111l1_opy_ = {
        bstack1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪற"): str(message)
      }
      bstack1l1ll11l_opy_(bstack1llll111l1_opy_, CONFIG, bstack1ll1111l1_opy_)
    else:
      bstack1l1ll11l_opy_(bstack1llll111l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l11111l1_opy_.format(str(e)))
def bstack1l1lll1ll1_opy_(bstack1lll11lll1_opy_, size):
  bstack1llll1l1l1_opy_ = []
  while len(bstack1lll11lll1_opy_) > size:
    bstack11l1l1ll_opy_ = bstack1lll11lll1_opy_[:size]
    bstack1llll1l1l1_opy_.append(bstack11l1l1ll_opy_)
    bstack1lll11lll1_opy_ = bstack1lll11lll1_opy_[size:]
  bstack1llll1l1l1_opy_.append(bstack1lll11lll1_opy_)
  return bstack1llll1l1l1_opy_
def bstack1lll11llll_opy_(args):
  if bstack1111_opy_ (u"ࠬ࠳࡭ࠨல") in args and bstack1111_opy_ (u"࠭ࡰࡥࡤࠪள") in args:
    return True
  return False
def run_on_browserstack(bstack1lll1lll1l_opy_=None, bstack1111l1l1_opy_=None, bstack1llll111_opy_=False):
  global CONFIG
  global bstack11l11l11l_opy_
  global bstack11llll11_opy_
  global bstack1l1ll111l_opy_
  bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠧࠨழ")
  bstack111ll11ll_opy_(bstack1ll11111l_opy_, logger)
  if bstack1lll1lll1l_opy_ and isinstance(bstack1lll1lll1l_opy_, str):
    bstack1lll1lll1l_opy_ = eval(bstack1lll1lll1l_opy_)
  if bstack1lll1lll1l_opy_:
    CONFIG = bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨவ")]
    bstack11l11l11l_opy_ = bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪஶ")]
    bstack11llll11_opy_ = bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬஷ")]
    bstack1llll1l1ll_opy_.bstack111l1111_opy_(bstack1111_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ஸ"), bstack11llll11_opy_)
    bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬஹ")
  if not bstack1llll111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111l111l_opy_)
      return
    if sys.argv[1] == bstack1111_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩ஺") or sys.argv[1] == bstack1111_opy_ (u"ࠧ࠮ࡸࠪ஻"):
      logger.info(bstack1111_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨ஼").format(__version__))
      return
    if sys.argv[1] == bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ஽"):
      bstack1lll111lll_opy_()
      return
  args = sys.argv
  bstack11lllllll_opy_()
  global bstack1lll11111l_opy_
  global bstack1ll11lll1_opy_
  global bstack1lll1l1l1_opy_
  global bstack11ll11111_opy_
  global bstack1llll11111_opy_
  global bstack1ll1ll1l11_opy_
  global bstack1l111l11_opy_
  global bstack1ll1ll1ll_opy_
  global bstack1ll1llllll_opy_
  global bstack1l1ll111_opy_
  global bstack1ll1lll1l_opy_
  bstack1ll11lll1_opy_ = len(CONFIG[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ா")])
  if not bstack1ll1l1ll11_opy_:
    if args[1] == bstack1111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫி") or args[1] == bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ீ"):
      bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ு")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ூ"):
      bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௃")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௄"):
      bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௅")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬெ"):
      bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ே")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ை"):
      bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ௉")
      args = args[2:]
    elif args[1] == bstack1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨொ"):
      bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩோ")
      args = args[2:]
    else:
      if not bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ௌ") in CONFIG or str(CONFIG[bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ்ࠧ")]).lower() in [bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௎"), bstack1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ௏")]:
        bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧௐ")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௑")]).lower() == bstack1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௒"):
        bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௓")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ௔")]).lower() == bstack1111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௕"):
        bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௖")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪௗ")]).lower() == bstack1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௘"):
        bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௙")
        args = args[1:]
      elif str(CONFIG[bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௚")]).lower() == bstack1111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௛"):
        bstack1ll1l1ll11_opy_ = bstack1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௜")
        args = args[1:]
      else:
        os.environ[bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ௝")] = bstack1ll1l1ll11_opy_
        bstack11llll111_opy_(bstack11llllll1_opy_)
  os.environ[bstack1111_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨ௞")] = bstack1ll1l1ll11_opy_
  bstack1l1ll111l_opy_ = bstack1ll1l1ll11_opy_
  global bstack1l1l1111_opy_
  if bstack1lll1lll1l_opy_:
    try:
      os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ௟")] = bstack1ll1l1ll11_opy_
      bstack1l1ll11l_opy_(bstack1l11l11l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l11111l1_opy_.format(str(e)))
  global bstack1l1ll1l11_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1ll11l1l_opy_
  global bstack1l1l1ll11_opy_
  global bstack11l111l11_opy_
  global bstack1lll11lll_opy_
  global bstack1ll11ll111_opy_
  global bstack11lll11l1_opy_
  global bstack11llll1l1_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11l1111l1_opy_
  global bstack1l111111_opy_
  global bstack1ll1l1ll1_opy_
  global bstack1ll1ll1111_opy_
  global bstack1ll11l1ll_opy_
  global bstack1111l11l_opy_
  global bstack111llll11_opy_
  global bstack1l1l11l11_opy_
  global bstack11111l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1ll1l11_opy_ = webdriver.Remote.__init__
    bstack1ll1l1l1l_opy_ = WebDriver.quit
    bstack11l1111l1_opy_ = WebDriver.close
    bstack1ll1ll1111_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1l1111_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l1l11ll1_opy_(CONFIG) and bstack1111ll111_opy_():
    if bstack1llll1ll1_opy_() < version.parse(bstack111111111_opy_):
      logger.error(bstack1l1ll1l1l_opy_.format(bstack1llll1ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll11l1ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll111ll11_opy_.format(str(e)))
  if bstack1ll1l1ll11_opy_ != bstack1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௠") or (bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௡") and not bstack1lll1lll1l_opy_):
    bstack111lll11l_opy_()
  if (bstack1ll1l1ll11_opy_ in [bstack1111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௢"), bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௣"), bstack1111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ௤")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack111l11l1l_opy_
        bstack11l111l11_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll11ll1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1l1ll11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1lllllll11_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll11ll1l1_opy_)
    if bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ௥") in CONFIG:
      os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ௦")] = os.getenv(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ௧"), json.dumps(CONFIG[bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ௨")]))
      CONFIG[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ௩")].pop(bstack1111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ௪"), None)
      CONFIG[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭௫")].pop(bstack1111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ௬"), None)
    if bstack11111llll_opy_ and bstack111ll1l1l_opy_.bstack11111l1l_opy_(CONFIG) and bstack1ll1l1ll11_opy_ != bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௭"):
      bstack11l11lll1_opy_, bstack11111111_opy_ = bstack111ll1l1l_opy_.bstack1l1l1llll_opy_(CONFIG, bstack1ll1l1ll11_opy_, bstack1ll111ll1l_opy_.version());
    if bstack1ll1l1ll11_opy_ != bstack1111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௮") and not bstack11l11lll1_opy_ is None:
      os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ௯")] = bstack11l11lll1_opy_;
      os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆࠪ௰")] = str(bstack11111111_opy_);
    if bstack1ll1l1ll11_opy_ != bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭௱"):
      bstack1ll1lll11l_opy_()
    bstack1ll11l1l_opy_ = Output.end_test
    bstack1lll11lll_opy_ = TestStatus.__init__
    bstack11lll11l1_opy_ = pabot._run
    bstack11llll1l1_opy_ = QueueItem.__init__
    bstack1ll1ll1l1_opy_ = pabot._create_command_for_execution
    bstack1l1l11l11_opy_ = pabot._report_results
  if bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௲"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll1111lll_opy_)
    bstack1l111111_opy_ = Runner.run_hook
    bstack1ll1l1ll1_opy_ = Step.run
  if bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ௳"):
    try:
      bstack1l1lll11l_opy_.launch(CONFIG, {
        bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ௴"): bstack1111_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ௵") if bstack111l1ll11_opy_() else bstack1111_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ௶"),
        bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ௷"): bstack1ll111ll1l_opy_.version(),
        bstack1111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ௸"): __version__
      })
      if bstack11111llll_opy_ and bstack111ll1l1l_opy_.bstack11111l1l_opy_(CONFIG):
        bstack11l11lll1_opy_, bstack11111111_opy_ = bstack111ll1l1l_opy_.bstack1l1l1llll_opy_(CONFIG, bstack1ll1l1ll11_opy_, bstack1ll111ll1l_opy_.version());
        if not bstack11l11lll1_opy_ is None:
          os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ௹")] = bstack11l11lll1_opy_;
          os.environ[bstack1111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡖࡈࡗ࡙ࡥࡒࡖࡐࡢࡍࡉ࠭௺")] = str(bstack11111111_opy_);
      from _pytest.config import Config
      bstack1111l11l_opy_ = Config.getoption
      from _pytest import runner
      bstack111llll11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack111lllll_opy_)
    try:
      from pytest_bdd import reporting
      bstack11111l11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1111_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ௻"))
  if bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௼"):
    bstack1lll1l1l1_opy_ = True
    if bstack1lll1lll1l_opy_ and bstack1llll111_opy_:
      bstack1ll1ll1l11_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ௽"), {}).get(bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௾"))
      bstack1ll1lll1l1_opy_(bstack1ll1l1l1ll_opy_)
    elif bstack1lll1lll1l_opy_:
      bstack1ll1ll1l11_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ௿"), {}).get(bstack1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨఀ"))
      global bstack11lll1111_opy_
      try:
        if bstack1lll11llll_opy_(bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఁ")]) and multiprocessing.current_process().name == bstack1111_opy_ (u"ࠨ࠲ࠪం"):
          bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬః")].remove(bstack1111_opy_ (u"ࠪ࠱ࡲ࠭ఄ"))
          bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఅ")].remove(bstack1111_opy_ (u"ࠬࡶࡤࡣࠩఆ"))
          bstack1lll1lll1l_opy_[bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఇ")] = bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఈ")][0]
          with open(bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఉ")], bstack1111_opy_ (u"ࠩࡵࠫఊ")) as f:
            bstack1111l11ll_opy_ = f.read()
          bstack1l1l1l11_opy_ = bstack1111_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࡪࡥࡧࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯࠭ࡹࡥ࡭ࡨ࠯ࠤࡦࡸࡧ࠭ࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡃࠠ࠱ࠫ࠽ࠎࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࡣࡵ࡫ࠥࡃࠠࡴࡶࡵࠬ࡮ࡴࡴࠩࡣࡵ࡫࠮࠱࠱࠱ࠫࠍࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫ࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢఋ").format(str(bstack1lll1lll1l_opy_))
          bstack111l1l11_opy_ = bstack1l1l1l11_opy_ + bstack1111l11ll_opy_
          bstack1lllll1l1l_opy_ = bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఌ")] + bstack1111_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ఍")
          with open(bstack1lllll1l1l_opy_, bstack1111_opy_ (u"࠭ࡷࠨఎ")):
            pass
          with open(bstack1lllll1l1l_opy_, bstack1111_opy_ (u"ࠢࡸ࠭ࠥఏ")) as f:
            f.write(bstack111l1l11_opy_)
          import subprocess
          bstack11ll1ll11_opy_ = subprocess.run([bstack1111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣఐ"), bstack1lllll1l1l_opy_])
          if os.path.exists(bstack1lllll1l1l_opy_):
            os.unlink(bstack1lllll1l1l_opy_)
          os._exit(bstack11ll1ll11_opy_.returncode)
        else:
          if bstack1lll11llll_opy_(bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ఑")]):
            bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఒ")].remove(bstack1111_opy_ (u"ࠫ࠲ࡳࠧఓ"))
            bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఔ")].remove(bstack1111_opy_ (u"࠭ࡰࡥࡤࠪక"))
            bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఖ")] = bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫగ")][0]
          bstack1ll1lll1l1_opy_(bstack1ll1l1l1ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఘ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1111_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬఙ")] = bstack1111_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭చ")
          mod_globals[bstack1111_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧఛ")] = os.path.abspath(bstack1lll1lll1l_opy_[bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩజ")])
          exec(open(bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఝ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1111_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨఞ").format(str(e)))
          for driver in bstack11lll1111_opy_:
            bstack1111l1l1_opy_.append({
              bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧట"): bstack1lll1lll1l_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")],
              bstack1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪడ"): str(e),
              bstack1111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫఢ"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭ణ") + json.dumps(
                bstack1111_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥత") + str(e)) + bstack1111_opy_ (u"ࠨࡿࢀࠫథ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11lll1111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11llll11_opy_, CONFIG, logger)
      bstack1111l111l_opy_()
      bstack11l11111_opy_()
      bstack11111111l_opy_ = {
        bstack1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬద"): args[0],
        bstack1111_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪధ"): CONFIG,
        bstack1111_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬన"): bstack11l11l11l_opy_,
        bstack1111_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ఩"): bstack11llll11_opy_
      }
      percy.bstack1ll1ll111l_opy_()
      if bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩప") in CONFIG:
        bstack1ll1ll11l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llllll1l_opy_ = manager.list()
        if bstack1lll11llll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఫ")]):
            if index == 0:
              bstack11111111l_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫబ")] = args
            bstack1ll1ll11l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11111111l_opy_, bstack1llllll1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬభ")]):
            bstack1ll1ll11l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11111111l_opy_, bstack1llllll1l_opy_)))
        for t in bstack1ll1ll11l_opy_:
          t.start()
        for t in bstack1ll1ll11l_opy_:
          t.join()
        bstack1ll1ll1ll_opy_ = list(bstack1llllll1l_opy_)
      else:
        if bstack1lll11llll_opy_(args):
          bstack11111111l_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭మ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11111111l_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1lll1l1_opy_(bstack1ll1l1l1ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1111_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭య")] = bstack1111_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧర")
          mod_globals[bstack1111_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨఱ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ల") or bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧళ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll11ll1l1_opy_)
    bstack1111l111l_opy_()
    bstack1ll1lll1l1_opy_(bstack111ll111_opy_)
    if bstack1111_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧఴ") in args:
      i = args.index(bstack1111_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨవ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1lll11111l_opy_))
    args.insert(0, str(bstack1111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩశ")))
    pabot.main(args)
  elif bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ష"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll11ll1l1_opy_)
    for a in args:
      if bstack1111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬస") in a:
        bstack1llll11111_opy_ = int(a.split(bstack1111_opy_ (u"ࠧ࠻ࠩహ"))[1])
      if bstack1111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ఺") in a:
        bstack1ll1ll1l11_opy_ = str(a.split(bstack1111_opy_ (u"ࠩ࠽ࠫ఻"))[1])
      if bstack1111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ఼ࠪ") in a:
        bstack1l111l11_opy_ = str(a.split(bstack1111_opy_ (u"ࠫ࠿࠭ఽ"))[1])
    bstack11ll1l11l_opy_ = None
    if bstack1111_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫా") in args:
      i = args.index(bstack1111_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬి"))
      args.pop(i)
      bstack11ll1l11l_opy_ = args.pop(i)
    if bstack11ll1l11l_opy_ is not None:
      global bstack1llll1lll_opy_
      bstack1llll1lll_opy_ = bstack11ll1l11l_opy_
    bstack1ll1lll1l1_opy_(bstack111ll111_opy_)
    run_cli(args)
    if bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫీ") in multiprocessing.current_process().__dict__.keys():
      for bstack11lll1l1l_opy_ in multiprocessing.current_process().bstack1l1lll1l1_opy_:
        bstack1111l1l1_opy_.append(bstack11lll1l1l_opy_)
  elif bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨు"):
    bstack1111ll11l_opy_ = bstack1ll111ll1l_opy_(args, logger, CONFIG, bstack11111llll_opy_)
    bstack1111ll11l_opy_.bstack11l111lll_opy_()
    bstack1111l111l_opy_()
    bstack11ll11111_opy_ = True
    bstack1l1ll111_opy_ = bstack1111ll11l_opy_.bstack111l111l1_opy_()
    bstack1111ll11l_opy_.bstack11111111l_opy_(bstack1ll1lll11_opy_)
    bstack1ll1llllll_opy_ = bstack1111ll11l_opy_.bstack111111l1_opy_(bstack1ll11l1lll_opy_, {
      bstack1111_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪూ"): bstack11l11l11l_opy_,
      bstack1111_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬృ"): bstack11llll11_opy_,
      bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧౄ"): bstack11111llll_opy_
    })
    bstack1ll1lll1l_opy_ = 1 if len(bstack1ll1llllll_opy_) > 0 else 0
  elif bstack1ll1l1ll11_opy_ == bstack1111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ౅"):
    try:
      from behave.__main__ import main as bstack1ll1l111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l1l111_opy_(e, bstack1ll1111lll_opy_)
    bstack1111l111l_opy_()
    bstack11ll11111_opy_ = True
    bstack11ll111ll_opy_ = 1
    if bstack1111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ె") in CONFIG:
      bstack11ll111ll_opy_ = CONFIG[bstack1111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧే")]
    bstack11l11l1ll_opy_ = int(bstack11ll111ll_opy_) * int(len(CONFIG[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫై")]))
    config = Configuration(args)
    bstack1ll111l11l_opy_ = config.paths
    if len(bstack1ll111l11l_opy_) == 0:
      import glob
      pattern = bstack1111_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨ౉")
      bstack11l1l1l11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11l1l1l11_opy_)
      config = Configuration(args)
      bstack1ll111l11l_opy_ = config.paths
    bstack11ll1lll_opy_ = [os.path.normpath(item) for item in bstack1ll111l11l_opy_]
    bstack11111lll_opy_ = [os.path.normpath(item) for item in args]
    bstack111lll1ll_opy_ = [item for item in bstack11111lll_opy_ if item not in bstack11ll1lll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1111_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫొ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll1lll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l1l1l_opy_)))
                    for bstack1l1l1l1l_opy_ in bstack11ll1lll_opy_]
    bstack1ll111llll_opy_ = []
    for spec in bstack11ll1lll_opy_:
      bstack1lll11ll11_opy_ = []
      bstack1lll11ll11_opy_ += bstack111lll1ll_opy_
      bstack1lll11ll11_opy_.append(spec)
      bstack1ll111llll_opy_.append(bstack1lll11ll11_opy_)
    execution_items = []
    for bstack1lll11ll11_opy_ in bstack1ll111llll_opy_:
      for index, _ in enumerate(CONFIG[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧో")]):
        item = {}
        item[bstack1111_opy_ (u"ࠬࡧࡲࡨࠩౌ")] = bstack1111_opy_ (u"࠭ࠠࠨ్").join(bstack1lll11ll11_opy_)
        item[bstack1111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭౎")] = index
        execution_items.append(item)
    bstack1l1l11lll_opy_ = bstack1l1lll1ll1_opy_(execution_items, bstack11l11l1ll_opy_)
    for execution_item in bstack1l1l11lll_opy_:
      bstack1ll1ll11l_opy_ = []
      for item in execution_item:
        bstack1ll1ll11l_opy_.append(bstack1ll111111l_opy_(name=str(item[bstack1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ౏")]),
                                             target=bstack1l1111ll1_opy_,
                                             args=(item[bstack1111_opy_ (u"ࠩࡤࡶ࡬࠭౐")],)))
      for t in bstack1ll1ll11l_opy_:
        t.start()
      for t in bstack1ll1ll11l_opy_:
        t.join()
  else:
    bstack11llll111_opy_(bstack11llllll1_opy_)
  if not bstack1lll1lll1l_opy_:
    bstack11llll1ll_opy_()
def browserstack_initialize(bstack1lll1ll1l_opy_=None):
  run_on_browserstack(bstack1lll1ll1l_opy_, None, True)
def bstack11llll1ll_opy_():
  global CONFIG
  global bstack1l1ll111l_opy_
  global bstack1ll1lll1l_opy_
  bstack1l1lll11l_opy_.stop()
  bstack1l1lll11l_opy_.bstack1lll11ll1l_opy_()
  if bstack111ll1l1l_opy_.bstack11111l1l_opy_(CONFIG):
    bstack111ll1l1l_opy_.bstack11lll1ll1_opy_()
  [bstack1ll1l111ll_opy_, bstack1l11lllll_opy_] = bstack11l11ll1l_opy_()
  if bstack1ll1l111ll_opy_ is not None and bstack1111ll1l1_opy_() != -1:
    sessions = bstack1ll1lll1_opy_(bstack1ll1l111ll_opy_)
    bstack11l1l11l1_opy_(sessions, bstack1l11lllll_opy_)
  if bstack1l1ll111l_opy_ == bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ౑") and bstack1ll1lll1l_opy_ != 0:
    sys.exit(bstack1ll1lll1l_opy_)
def bstack1ll1111l11_opy_(bstack1ll11111l1_opy_):
  if bstack1ll11111l1_opy_:
    return bstack1ll11111l1_opy_.capitalize()
  else:
    return bstack1ll11111l1_opy_
def bstack1lll1lll_opy_(bstack1lll11l11l_opy_):
  if bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ౒") in bstack1lll11l11l_opy_ and bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౓")] != bstack1111_opy_ (u"࠭ࠧ౔"):
    return bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩౕࠬ")]
  else:
    bstack11l11llll_opy_ = bstack1111_opy_ (u"ࠣࠤౖ")
    if bstack1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ౗") in bstack1lll11l11l_opy_ and bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪౘ")] != None:
      bstack11l11llll_opy_ += bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫౙ")] + bstack1111_opy_ (u"ࠧ࠲ࠠࠣౚ")
      if bstack1lll11l11l_opy_[bstack1111_opy_ (u"࠭࡯ࡴࠩ౛")] == bstack1111_opy_ (u"ࠢࡪࡱࡶࠦ౜"):
        bstack11l11llll_opy_ += bstack1111_opy_ (u"ࠣ࡫ࡒࡗࠥࠨౝ")
      bstack11l11llll_opy_ += (bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭౞")] or bstack1111_opy_ (u"ࠪࠫ౟"))
      return bstack11l11llll_opy_
    else:
      bstack11l11llll_opy_ += bstack1ll1111l11_opy_(bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬౠ")]) + bstack1111_opy_ (u"ࠧࠦࠢౡ") + (
              bstack1lll11l11l_opy_[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨౢ")] or bstack1111_opy_ (u"ࠧࠨౣ")) + bstack1111_opy_ (u"ࠣ࠮ࠣࠦ౤")
      if bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠩࡲࡷࠬ౥")] == bstack1111_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ౦"):
        bstack11l11llll_opy_ += bstack1111_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ౧")
      bstack11l11llll_opy_ += bstack1lll11l11l_opy_[bstack1111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ౨")] or bstack1111_opy_ (u"࠭ࠧ౩")
      return bstack11l11llll_opy_
def bstack11l1l11ll_opy_(bstack11ll1ll1l_opy_):
  if bstack11ll1ll1l_opy_ == bstack1111_opy_ (u"ࠢࡥࡱࡱࡩࠧ౪"):
    return bstack1111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ౫")
  elif bstack11ll1ll1l_opy_ == bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౬"):
    return bstack1111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౭")
  elif bstack11ll1ll1l_opy_ == bstack1111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ౮"):
    return bstack1111_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౯")
  elif bstack11ll1ll1l_opy_ == bstack1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ౰"):
    return bstack1111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ౱")
  elif bstack11ll1ll1l_opy_ == bstack1111_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ౲"):
    return bstack1111_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ౳")
  elif bstack11ll1ll1l_opy_ == bstack1111_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦ౴"):
    return bstack1111_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౵")
  else:
    return bstack1111_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩ౶") + bstack1ll1111l11_opy_(
      bstack11ll1ll1l_opy_) + bstack1111_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౷")
def bstack1111l111_opy_(session):
  return bstack1111_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧ౸").format(
    session[bstack1111_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ౹")], bstack1lll1lll_opy_(session), bstack11l1l11ll_opy_(session[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨ౺")]),
    bstack11l1l11ll_opy_(session[bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ౻")]),
    bstack1ll1111l11_opy_(session[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ౼")] or session[bstack1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ౽")] or bstack1111_opy_ (u"࠭ࠧ౾")) + bstack1111_opy_ (u"ࠢࠡࠤ౿") + (session[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪಀ")] or bstack1111_opy_ (u"ࠩࠪಁ")),
    session[bstack1111_opy_ (u"ࠪࡳࡸ࠭ಂ")] + bstack1111_opy_ (u"ࠦࠥࠨಃ") + session[bstack1111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ಄")], session[bstack1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨಅ")] or bstack1111_opy_ (u"ࠧࠨಆ"),
    session[bstack1111_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬಇ")] if session[bstack1111_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ಈ")] else bstack1111_opy_ (u"ࠪࠫಉ"))
def bstack11l1l11l1_opy_(sessions, bstack1l11lllll_opy_):
  try:
    bstack11111l1ll_opy_ = bstack1111_opy_ (u"ࠦࠧಊ")
    if not os.path.exists(bstack11111ll1_opy_):
      os.mkdir(bstack11111ll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪಋ")), bstack1111_opy_ (u"࠭ࡲࠨಌ")) as f:
      bstack11111l1ll_opy_ = f.read()
    bstack11111l1ll_opy_ = bstack11111l1ll_opy_.replace(bstack1111_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫ಍"), str(len(sessions)))
    bstack11111l1ll_opy_ = bstack11111l1ll_opy_.replace(bstack1111_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨಎ"), bstack1l11lllll_opy_)
    bstack11111l1ll_opy_ = bstack11111l1ll_opy_.replace(bstack1111_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪಏ"),
                                              sessions[0].get(bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧಐ")) if sessions[0] else bstack1111_opy_ (u"ࠫࠬ಑"))
    with open(os.path.join(bstack11111ll1_opy_, bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩಒ")), bstack1111_opy_ (u"࠭ࡷࠨಓ")) as stream:
      stream.write(bstack11111l1ll_opy_.split(bstack1111_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫಔ"))[0])
      for session in sessions:
        stream.write(bstack1111l111_opy_(session))
      stream.write(bstack11111l1ll_opy_.split(bstack1111_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬಕ"))[1])
    logger.info(bstack1111_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬಖ").format(bstack11111ll1_opy_));
  except Exception as e:
    logger.debug(bstack11l1ll1ll_opy_.format(str(e)))
def bstack1ll1lll1_opy_(bstack1ll1l111ll_opy_):
  global CONFIG
  try:
    host = bstack1111_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ಗ") if bstack1111_opy_ (u"ࠫࡦࡶࡰࠨಘ") in CONFIG else bstack1111_opy_ (u"ࠬࡧࡰࡪࠩಙ")
    user = CONFIG[bstack1111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨಚ")]
    key = CONFIG[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪಛ")]
    bstack1lll111l1_opy_ = bstack1111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧಜ") if bstack1111_opy_ (u"ࠩࡤࡴࡵ࠭ಝ") in CONFIG else bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬಞ")
    url = bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩಟ").format(user, key, host, bstack1lll111l1_opy_,
                                                                                bstack1ll1l111ll_opy_)
    headers = {
      bstack1111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫಠ"): bstack1111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩಡ"),
    }
    proxies = bstack1l1llll11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬಢ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1l11ll_opy_.format(str(e)))
def bstack11l11ll1l_opy_():
  global CONFIG
  global bstack1lllllllll_opy_
  try:
    if bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಣ") in CONFIG:
      host = bstack1111_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬತ") if bstack1111_opy_ (u"ࠪࡥࡵࡶࠧಥ") in CONFIG else bstack1111_opy_ (u"ࠫࡦࡶࡩࠨದ")
      user = CONFIG[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧಧ")]
      key = CONFIG[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩನ")]
      bstack1lll111l1_opy_ = bstack1111_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭಩") if bstack1111_opy_ (u"ࠨࡣࡳࡴࠬಪ") in CONFIG else bstack1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫಫ")
      url = bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪಬ").format(user, key, host, bstack1lll111l1_opy_)
      headers = {
        bstack1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪಭ"): bstack1111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨಮ"),
      }
      if bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಯ") in CONFIG:
        params = {bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬರ"): CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಱ")], bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಲ"): CONFIG[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಳ")]}
      else:
        params = {bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ಴"): CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨವ")]}
      proxies = bstack1l1llll11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll1l111l1_opy_ = response.json()[0][bstack1111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩಶ")]
        if bstack1ll1l111l1_opy_:
          bstack1l11lllll_opy_ = bstack1ll1l111l1_opy_[bstack1111_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫಷ")].split(bstack1111_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧಸ"))[0] + bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪಹ") + bstack1ll1l111l1_opy_[
            bstack1111_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭಺")]
          logger.info(bstack1l1lllll_opy_.format(bstack1l11lllll_opy_))
          bstack1lllllllll_opy_ = bstack1ll1l111l1_opy_[bstack1111_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ಻")]
          bstack111l11111_opy_ = CONFIG[bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ಼")]
          if bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಽ") in CONFIG:
            bstack111l11111_opy_ += bstack1111_opy_ (u"ࠧࠡࠩಾ") + CONFIG[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಿ")]
          if bstack111l11111_opy_ != bstack1ll1l111l1_opy_[bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೀ")]:
            logger.debug(bstack1lllllll1l_opy_.format(bstack1ll1l111l1_opy_[bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨು")], bstack111l11111_opy_))
          return [bstack1ll1l111l1_opy_[bstack1111_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧೂ")], bstack1l11lllll_opy_]
    else:
      logger.warn(bstack1111l1l11_opy_)
  except Exception as e:
    logger.debug(bstack11ll1111_opy_.format(str(e)))
  return [None, None]
def bstack1ll111lll1_opy_(url, bstack1l11l1ll1_opy_=False):
  global CONFIG
  global bstack111l1lll_opy_
  if not bstack111l1lll_opy_:
    hostname = bstack1lll1l1ll1_opy_(url)
    is_private = bstack1l1lllll1_opy_(hostname)
    if (bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩೃ") in CONFIG and not CONFIG[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪೄ")]) and (is_private or bstack1l11l1ll1_opy_):
      bstack111l1lll_opy_ = hostname
def bstack1lll1l1ll1_opy_(url):
  return urlparse(url).hostname
def bstack1l1lllll1_opy_(hostname):
  for bstack111ll1ll_opy_ in bstack1l1111111_opy_:
    regex = re.compile(bstack111ll1ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1ll1ll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1llll11111_opy_
  if not bstack111ll1l1l_opy_.bstack1llll11l11_opy_(CONFIG, bstack1llll11111_opy_):
    logger.warning(bstack1111_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ೅"))
    return {}
  try:
    results = driver.execute_script(bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡲࡦࡵࡲࡰࡻ࡫ࠬࠡࡴࡨ࡮ࡪࡩࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡶࡾࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࡺࡪࡴࡴࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡇࡐࡠࡉࡈࡘࡤࡘࡅࡔࡗࡏࡘࡘ࠭ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡪࡳࠦ࠽ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬࡪࡼࡥ࡯ࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡸࡥ࡮ࡱࡹࡩࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡖࡊ࡙ࡕࡍࡖࡖࡣࡗࡋࡓࡑࡑࡑࡗࡊ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡴࡱ࡯ࡺࡪ࠮ࡥࡷࡧࡱࡸ࠳ࡪࡥࡵࡣ࡬ࡰ࠳ࡪࡡࡵࡣࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡪࡩࡴࡲࡤࡸࡨ࡮ࡅࡷࡧࡱࡸ࠭࡫ࡶࡦࡰࡷ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠦࡣࡢࡶࡦ࡬ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩ࡯࡫ࡣࡵࠪࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠣࠤࠥೆ"))
    return results
  except Exception:
    logger.error(bstack1111_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦೇ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1llll11111_opy_
  if not bstack111ll1l1l_opy_.bstack1llll11l11_opy_(CONFIG, bstack1llll11111_opy_):
    logger.warning(bstack1111_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢೈ"))
    return {}
  try:
    bstack1l1llll1l1_opy_ = driver.execute_script(bstack1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣࡌࡋࡔࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࠪ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰࠣࡁࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡧࡹࡩࡳࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡵࡩࡲࡵࡶࡦࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹ࡯࡭ࡸࡨࠬࡪࡼࡥ࡯ࡶ࠱ࡨࡪࡺࡡࡪ࡮࠱ࡷࡺࡳ࡭ࡢࡴࡼ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡡࡥࡦࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࡸࡨࡲࡹ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠡࡥࡤࡸࡨ࡮ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡪࡦࡥࡷࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࡿࠬ࠿ࠏࠦࠠࠡࠢࠥࠦࠧ೉"))
    return bstack1l1llll1l1_opy_
  except Exception:
    logger.error(bstack1111_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨೊ"))
    return {}