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
import os
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack1l1l1ll111_opy_ as bstack1l1l1llll1_opy_
from bstack_utils.helper import bstack11l1l1111_opy_, bstack1l1l11l1_opy_, bstack1l1l1lllll_opy_, bstack1l1l11l1ll_opy_, bstack1ll11111_opy_, get_host_info, bstack1l1l1ll1l1_opy_, bstack11l1l11l1_opy_, bstack1l1l1l1lll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l1l1l1lll_opy_(class_method=False)
def _1l1l11lll1_opy_(driver, bstack11ll1ll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11lll1l_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨ೶"): caps.get(bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ೷"), None),
        bstack11lll1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭೸"): bstack11ll1ll11_opy_.get(bstack11lll1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೹"), None),
        bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ೺"): caps.get(bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ೻"), None),
        bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ೼"): caps.get(bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ೽"), None)
    }
  except Exception as error:
    logger.debug(bstack11lll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ೾") + str(error))
  return response
def bstack1ll1ll111l_opy_(config):
  return config.get(bstack11lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ೿"), False) or any([p.get(bstack11lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪഀ"), False) == True for p in config[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഁ")]])
def bstack1l11111ll_opy_(config, bstack1ll11ll11l_opy_):
  try:
    if not bstack1l1l11l1_opy_(config):
      return False
    bstack1l1l1ll11l_opy_ = config.get(bstack11lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬം"), False)
    bstack1l1l11ll11_opy_ = config[bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഃ")][bstack1ll11ll11l_opy_].get(bstack11lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧഄ"), None)
    if bstack1l1l11ll11_opy_ != None:
      bstack1l1l1ll11l_opy_ = bstack1l1l11ll11_opy_
    bstack1l1l1l111l_opy_ = os.getenv(bstack11lll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭അ")) is not None and len(os.getenv(bstack11lll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧആ"))) > 0 and os.getenv(bstack11lll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨഇ")) != bstack11lll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩഈ")
    return bstack1l1l1ll11l_opy_ and bstack1l1l1l111l_opy_
  except Exception as error:
    logger.debug(bstack11lll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬഉ") + str(error))
  return False
def bstack1lll11l1l_opy_(bstack1l1l1lll1l_opy_, test_tags):
  bstack1l1l1lll1l_opy_ = os.getenv(bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧഊ"))
  if bstack1l1l1lll1l_opy_ is None:
    return True
  bstack1l1l1lll1l_opy_ = json.loads(bstack1l1l1lll1l_opy_)
  try:
    include_tags = bstack1l1l1lll1l_opy_[bstack11lll1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬഋ")] if bstack11lll1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ഌ") in bstack1l1l1lll1l_opy_ and isinstance(bstack1l1l1lll1l_opy_[bstack11lll1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ഍")], list) else []
    exclude_tags = bstack1l1l1lll1l_opy_[bstack11lll1l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨഎ")] if bstack11lll1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩഏ") in bstack1l1l1lll1l_opy_ and isinstance(bstack1l1l1lll1l_opy_[bstack11lll1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪഐ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨ഑") + str(error))
  return False
def bstack1ll111111_opy_(config, bstack1l1ll111ll_opy_, bstack1l1l1l11ll_opy_):
  bstack1l1l1l11l1_opy_ = bstack1l1l1lllll_opy_(config)
  bstack1l1l1l1ll1_opy_ = bstack1l1l11l1ll_opy_(config)
  if bstack1l1l1l11l1_opy_ is None or bstack1l1l1l1ll1_opy_ is None:
    logger.error(bstack11lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨഒ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩഓ"), bstack11lll1l_opy_ (u"ࠩࡾࢁࠬഔ")))
    data = {
        bstack11lll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨക"): config[bstack11lll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩഖ")],
        bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨഗ"): config.get(bstack11lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩഘ"), os.path.basename(os.getcwd())),
        bstack11lll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪങ"): bstack11l1l1111_opy_(),
        bstack11lll1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ച"): config.get(bstack11lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬഛ"), bstack11lll1l_opy_ (u"ࠪࠫജ")),
        bstack11lll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഝ"): {
            bstack11lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬഞ"): bstack1l1ll111ll_opy_,
            bstack11lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩട"): bstack1l1l1l11ll_opy_,
            bstack11lll1l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫഠ"): __version__
        },
        bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪഡ"): settings,
        bstack11lll1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪഢ"): bstack1l1l1ll1l1_opy_(),
        bstack11lll1l_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪണ"): bstack1ll11111_opy_(),
        bstack11lll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭ത"): get_host_info(),
        bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧഥ"): bstack1l1l11l1_opy_(config)
    }
    headers = {
        bstack11lll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬദ"): bstack11lll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪധ"),
    }
    config = {
        bstack11lll1l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ന"): (bstack1l1l1l11l1_opy_, bstack1l1l1l1ll1_opy_),
        bstack11lll1l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪഩ"): headers
    }
    response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨപ"), bstack1l1l1llll1_opy_ + bstack11lll1l_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨഫ"), data, config)
    bstack1l1l1l1111_opy_ = response.json()
    if bstack1l1l1l1111_opy_[bstack11lll1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ബ")]:
      parsed = json.loads(os.getenv(bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧഭ"), bstack11lll1l_opy_ (u"ࠧࡼࡿࠪമ")))
      parsed[bstack11lll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩയ")] = bstack1l1l1l1111_opy_[bstack11lll1l_opy_ (u"ࠩࡧࡥࡹࡧࠧര")][bstack11lll1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫറ")]
      os.environ[bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬല")] = json.dumps(parsed)
      return bstack1l1l1l1111_opy_[bstack11lll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪള")][bstack11lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫഴ")], bstack1l1l1l1111_opy_[bstack11lll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬവ")][bstack11lll1l_opy_ (u"ࠨ࡫ࡧࠫശ")]
    else:
      logger.error(bstack11lll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪഷ") + bstack1l1l1l1111_opy_[bstack11lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫസ")])
      if bstack1l1l1l1111_opy_[bstack11lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬഹ")] == bstack11lll1l_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧഺ"):
        for bstack1l1l11ll1l_opy_ in bstack1l1l1l1111_opy_[bstack11lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ഻࠭")]:
          logger.error(bstack1l1l11ll1l_opy_[bstack11lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ഼")])
      return None, None
  except Exception as error:
    logger.error(bstack11lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤഽ") +  str(error))
    return None, None
def bstack1111l1l1_opy_():
  if os.getenv(bstack11lll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧാ")) is None:
    return {
        bstack11lll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪി"): bstack11lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪീ"),
        bstack11lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ു"): bstack11lll1l_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬൂ")
    }
  data = {bstack11lll1l_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨൃ"): bstack11l1l1111_opy_()}
  headers = {
      bstack11lll1l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨൄ"): bstack11lll1l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪ൅") + os.getenv(bstack11lll1l_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣെ")),
      bstack11lll1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪേ"): bstack11lll1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨൈ")
  }
  response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"࠭ࡐࡖࡖࠪ൉"), bstack1l1l1llll1_opy_ + bstack11lll1l_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩൊ"), data, { bstack11lll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩോ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11lll1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥൌ") + datetime.utcnow().isoformat() + bstack11lll1l_opy_ (u"ࠪ࡞്ࠬ"))
      return {bstack11lll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫൎ"): bstack11lll1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭൏"), bstack11lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ൐"): bstack11lll1l_opy_ (u"ࠧࠨ൑")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦ൒") + str(error))
    return {
        bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ൓"): bstack11lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩൔ"),
        bstack11lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൕ"): str(error)
    }
def bstack1ll11ll11_opy_(caps, options):
  try:
    bstack1l1l1lll11_opy_ = caps.get(bstack11lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ൖ"), {}).get(bstack11lll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪൗ"), caps.get(bstack11lll1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ൘"), bstack11lll1l_opy_ (u"ࠨࠩ൙")))
    if bstack1l1l1lll11_opy_:
      logger.warn(bstack11lll1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ൚"))
      return False
    browser = caps.get(bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ൛"), bstack11lll1l_opy_ (u"ࠫࠬ൜")).lower()
    if browser != bstack11lll1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ൝"):
      logger.warn(bstack11lll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ൞"))
      return False
    browser_version = caps.get(bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨൟ"), caps.get(bstack11lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪൠ")))
    if browser_version and browser_version != bstack11lll1l_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩൡ") and int(browser_version.split(bstack11lll1l_opy_ (u"ࠪ࠲ࠬൢ"))[0]) <= 94:
      logger.warn(bstack11lll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠴࠯ࠤൣ"))
      return False
    if not options is None:
      bstack1l1ll111l1_opy_ = options.to_capabilities().get(bstack11lll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ൤"), {})
      if bstack11lll1l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪ൥") in bstack1l1ll111l1_opy_.get(bstack11lll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ൦"), []):
        logger.warn(bstack11lll1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥ൧"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦ൨") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1l1ll11111_opy_ = config.get(bstack11lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ൩"), {})
    bstack1l1ll11111_opy_[bstack11lll1l_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧ൪")] = os.getenv(bstack11lll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ൫"))
    bstack1l1l1l1l11_opy_ = json.loads(os.getenv(bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ൬"), bstack11lll1l_opy_ (u"ࠧࡼࡿࠪ൭"))).get(bstack11lll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ൮"))
    caps[bstack11lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ൯")] = True
    if bstack11lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ൰") in caps:
      caps[bstack11lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ൱")][bstack11lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ൲")] = bstack1l1ll11111_opy_
      caps[bstack11lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ൳")][bstack11lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ൴")][bstack11lll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ൵")] = bstack1l1l1l1l11_opy_
    else:
      caps[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൶")] = bstack1l1ll11111_opy_
      caps[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ൷")][bstack11lll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ൸")] = bstack1l1l1l1l11_opy_
  except Exception as error:
    logger.debug(bstack11lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨ൹") +  str(error))
def bstack1lll1lll1l_opy_(driver, bstack1l1l11l1l1_opy_):
  try:
    session = driver.session_id
    if session:
      bstack1l1l1l1l1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1l1l1l1l1l_opy_ = False
      bstack1l1l1l1l1l_opy_ = url.scheme in [bstack11lll1l_opy_ (u"ࠨࡨࡵࡶࡳࠦൺ"), bstack11lll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨൻ")]
      if bstack1l1l1l1l1l_opy_:
        if bstack1l1l11l1l1_opy_:
          logger.info(bstack11lll1l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣർ"))
          driver.execute_async_script(bstack11lll1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦ࠽ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࡟ࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࠬ࠮ࠦ࠽࠿ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠨ࠮ࠣࡪࡳ࠸ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡊࡔࡘࡃࡆࡡࡖࡘࡆࡘࡔࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰ࠵ࠤࡂࠦࠨࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡓࡕࡃࡕࡘࡊࡊࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡴࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤൽ"))
          logger.info(bstack11lll1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠥൾ"))
        else:
          driver.execute_script(bstack11lll1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣࡋࡕࡒࡄࡇࡢࡗ࡙ࡕࡐࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢൿ"))
      return bstack1l1l11l1l1_opy_
  except Exception as e:
    logger.error(bstack11lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ඀") + str(e))
    return False
def bstack11lll11l1_opy_(driver, class_name, name, module_name, path, bstack11ll1ll11_opy_):
  try:
    bstack1l1l1ll1ll_opy_ = [class_name] if not class_name is None else []
    bstack1l1ll1111l_opy_ = {
        bstack11lll1l_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦඁ"): True,
        bstack11lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡉ࡫ࡴࡢ࡫࡯ࡷࠧං"): {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨඃ"): name,
            bstack11lll1l_opy_ (u"ࠤࡷࡩࡸࡺࡒࡶࡰࡌࡨࠧ඄"): os.environ.get(bstack11lll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩඅ")),
            bstack11lll1l_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨආ"): str(path),
            bstack11lll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࡐ࡮ࡹࡴࠣඇ"): [module_name, *bstack1l1l1ll1ll_opy_, name],
        },
        bstack11lll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣඈ"): _1l1l11lll1_opy_(driver, bstack11ll1ll11_opy_)
    }
    driver.execute_script(bstack11lll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡃࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞ࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠡ࠿ࠣࡲࡺࡲ࡬࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࠨࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣ࡙ࡘࡁࡏࡕࡓࡓࡗ࡚ࡅࡓࠩ࠯ࠤ࠭࡫ࡶࡦࡰࡷ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡺࡡࡱࡖࡵࡥࡳࡹࡰࡰࡴࡷࡩࡷࡊࡡࡵࡣࠣࡁࠥ࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠢࡀࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡹࡧࡰࡕࡴࡤࡲࡸࡶ࡯ࡳࡶࡨࡶࡉࡧࡴࡢ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡋࡎࡅࠩ࠯ࠤࢀࠦࡤࡦࡶࡤ࡭ࡱࡀࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨඉ"), bstack1l1ll1111l_opy_)
    logger.info(bstack11lll1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦඊ"))
  except Exception as bstack1l1l11llll_opy_:
    logger.error(bstack11lll1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦඋ") + str(path) + bstack11lll1l_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧඌ") + str(bstack1l1l11llll_opy_))