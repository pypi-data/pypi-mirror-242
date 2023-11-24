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
import os
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack1l1l1l1l1l_opy_ as bstack1l1l11ll11_opy_
from bstack_utils.helper import bstack1111111l1_opy_, bstack1l111lll1_opy_, bstack1l1l1l1111_opy_, bstack1l1l11lll1_opy_, bstack1111lll11_opy_, get_host_info, bstack1l1l1lll1l_opy_, bstack1ll1111l_opy_, bstack1l1l1ll1ll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l1l1ll1ll_opy_(class_method=False)
def _1l1ll111ll_opy_(driver, bstack111l1l1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1111_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧ೵"): caps.get(bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭೶"), None),
        bstack1111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ೷"): bstack111l1l1l_opy_.get(bstack1111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ೸"), None),
        bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩ೹"): caps.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ೺"), None),
        bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ೻"): caps.get(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ೼"), None)
    }
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫ೽") + str(error))
  return response
def bstack11111l1l_opy_(config):
  return config.get(bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ೾"), False) or any([p.get(bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ೿"), False) == True for p in config[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ഀ")]])
def bstack1llll11l11_opy_(config, bstack1ll111ll1_opy_):
  try:
    if not bstack1l111lll1_opy_(config):
      return False
    bstack1l1l1lll11_opy_ = config.get(bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫഁ"), False)
    bstack1l1l11ll1l_opy_ = config[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨം")][bstack1ll111ll1_opy_].get(bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ഃ"), None)
    if bstack1l1l11ll1l_opy_ != None:
      bstack1l1l1lll11_opy_ = bstack1l1l11ll1l_opy_
    bstack1l1ll1111l_opy_ = os.getenv(bstack1111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬഄ")) is not None and len(os.getenv(bstack1111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭അ"))) > 0 and os.getenv(bstack1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧആ")) != bstack1111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨഇ")
    return bstack1l1l1lll11_opy_ and bstack1l1ll1111l_opy_
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫഈ") + str(error))
  return False
def bstack11lll11l_opy_(bstack1l1l1llll1_opy_, test_tags):
  bstack1l1l1llll1_opy_ = os.getenv(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ഉ"))
  if bstack1l1l1llll1_opy_ is None:
    return True
  bstack1l1l1llll1_opy_ = json.loads(bstack1l1l1llll1_opy_)
  try:
    include_tags = bstack1l1l1llll1_opy_[bstack1111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫഊ")] if bstack1111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬഋ") in bstack1l1l1llll1_opy_ and isinstance(bstack1l1l1llll1_opy_[bstack1111_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ഌ")], list) else []
    exclude_tags = bstack1l1l1llll1_opy_[bstack1111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ഍")] if bstack1111_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨഎ") in bstack1l1l1llll1_opy_ and isinstance(bstack1l1l1llll1_opy_[bstack1111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩഏ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧഐ") + str(error))
  return False
def bstack1l1l1llll_opy_(config, bstack1l1l1l1l11_opy_, bstack1l1ll111l1_opy_):
  bstack1l1l1l11l1_opy_ = bstack1l1l1l1111_opy_(config)
  bstack1l1l1l1ll1_opy_ = bstack1l1l11lll1_opy_(config)
  if bstack1l1l1l11l1_opy_ is None or bstack1l1l1l1ll1_opy_ is None:
    logger.error(bstack1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ഑"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨഒ"), bstack1111_opy_ (u"ࠨࡽࢀࠫഓ")))
    data = {
        bstack1111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧഔ"): config[bstack1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨക")],
        bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧഖ"): config.get(bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨഗ"), os.path.basename(os.getcwd())),
        bstack1111_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩഘ"): bstack1111111l1_opy_(),
        bstack1111_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬങ"): config.get(bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫച"), bstack1111_opy_ (u"ࠩࠪഛ")),
        bstack1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪജ"): {
            bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫഝ"): bstack1l1l1l1l11_opy_,
            bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨഞ"): bstack1l1ll111l1_opy_,
            bstack1111_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪട"): __version__
        },
        bstack1111_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩഠ"): settings,
        bstack1111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩഡ"): bstack1l1l1lll1l_opy_(),
        bstack1111_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩഢ"): bstack1111lll11_opy_(),
        bstack1111_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬണ"): get_host_info(),
        bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ത"): bstack1l111lll1_opy_(config)
    }
    headers = {
        bstack1111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫഥ"): bstack1111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩദ"),
    }
    config = {
        bstack1111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬധ"): (bstack1l1l1l11l1_opy_, bstack1l1l1l1ll1_opy_),
        bstack1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩന"): headers
    }
    response = bstack1ll1111l_opy_(bstack1111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧഩ"), bstack1l1l11ll11_opy_ + bstack1111_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧപ"), data, config)
    bstack1l1l11l1ll_opy_ = response.json()
    if bstack1l1l11l1ll_opy_[bstack1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬഫ")]:
      parsed = json.loads(os.getenv(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ബ"), bstack1111_opy_ (u"࠭ࡻࡾࠩഭ")))
      parsed[bstack1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨമ")] = bstack1l1l11l1ll_opy_[bstack1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭യ")][bstack1111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪര")]
      os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫറ")] = json.dumps(parsed)
      return bstack1l1l11l1ll_opy_[bstack1111_opy_ (u"ࠫࡩࡧࡴࡢࠩല")][bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪള")], bstack1l1l11l1ll_opy_[bstack1111_opy_ (u"࠭ࡤࡢࡶࡤࠫഴ")][bstack1111_opy_ (u"ࠧࡪࡦࠪവ")]
    else:
      logger.error(bstack1111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩശ") + bstack1l1l11l1ll_opy_[bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪഷ")])
      if bstack1l1l11l1ll_opy_[bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫസ")] == bstack1111_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ഹ"):
        for bstack1l1l11llll_opy_ in bstack1l1l11l1ll_opy_[bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬഺ")]:
          logger.error(bstack1l1l11llll_opy_[bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫഻ࠧ")])
      return None, None
  except Exception as error:
    logger.error(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀ഼ࠠࠣ") +  str(error))
    return None, None
def bstack11lll1ll1_opy_():
  if os.getenv(bstack1111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ഽ")) is None:
    return {
        bstack1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩാ"): bstack1111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩി"),
        bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬീ"): bstack1111_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫു")
    }
  data = {bstack1111_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧൂ"): bstack1111111l1_opy_()}
  headers = {
      bstack1111_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧൃ"): bstack1111_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩൄ") + os.getenv(bstack1111_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢ൅")),
      bstack1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩെ"): bstack1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧേ")
  }
  response = bstack1ll1111l_opy_(bstack1111_opy_ (u"ࠬࡖࡕࡕࠩൈ"), bstack1l1l11ll11_opy_ + bstack1111_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨ൉"), data, { bstack1111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨൊ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1111_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤോ") + datetime.utcnow().isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫൌ"))
      return {bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ്ࠪ"): bstack1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬൎ"), bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൏"): bstack1111_opy_ (u"࠭ࠧ൐")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥ൑") + str(error))
    return {
        bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ൒"): bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ൓"),
        bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫൔ"): str(error)
    }
def bstack1lll11l111_opy_(caps, options):
  try:
    bstack1l1l11l1l1_opy_ = caps.get(bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬൕ"), {}).get(bstack1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩൖ"), caps.get(bstack1111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ൗ"), bstack1111_opy_ (u"ࠧࠨ൘")))
    if bstack1l1l11l1l1_opy_:
      logger.warn(bstack1111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ൙"))
      return False
    browser = caps.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ൚"), bstack1111_opy_ (u"ࠪࠫ൛")).lower()
    if browser != bstack1111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ൜"):
      logger.warn(bstack1111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ൝"))
      return False
    browser_version = caps.get(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ൞"), caps.get(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩൟ")))
    if browser_version and browser_version != bstack1111_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨൠ") and int(browser_version.split(bstack1111_opy_ (u"ࠩ࠱ࠫൡ"))[0]) <= 94:
      logger.warn(bstack1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤ࠾࠺࠮ࠣൢ"))
      return False
    if not options is None:
      bstack1l1l1ll1l1_opy_ = options.to_capabilities().get(bstack1111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩൣ"), {})
      if bstack1111_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩ൤") in bstack1l1l1ll1l1_opy_.get(bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫ൥"), []):
        logger.warn(bstack1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ൦"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥ൧") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1l1l1l1lll_opy_ = config.get(bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ൨"), {})
    bstack1l1l1l1lll_opy_[bstack1111_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭൩")] = os.getenv(bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ൪"))
    bstack1l1l1l11ll_opy_ = json.loads(os.getenv(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭൫"), bstack1111_opy_ (u"࠭ࡻࡾࠩ൬"))).get(bstack1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ൭"))
    caps[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ൮")] = True
    if bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ൯") in caps:
      caps[bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ൰")][bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ൱")] = bstack1l1l1l1lll_opy_
      caps[bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭൲")][bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭൳")][bstack1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ൴")] = bstack1l1l1l11ll_opy_
    else:
      caps[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ൵")] = bstack1l1l1l1lll_opy_
      caps[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൶")][bstack1111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ൷")] = bstack1l1l1l11ll_opy_
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧ൸") +  str(error))
def bstack111lll1l1_opy_(driver, bstack1l1l1ll11l_opy_):
  try:
    session = driver.session_id
    if session:
      bstack1l1ll11111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1l1ll11111_opy_ = False
      bstack1l1ll11111_opy_ = url.scheme in [bstack1111_opy_ (u"ࠧ࡮ࡴࡵࡲࠥ൹"), bstack1111_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧൺ")]
      if bstack1l1ll11111_opy_:
        if bstack1l1l1ll11l_opy_:
          logger.info(bstack1111_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢൻ"))
          driver.execute_async_script(bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡃࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞ࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡴࠠ࠾ࠢࠫ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡢࡦࡧࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡓࡕࡃࡕࡘࡊࡊࠧ࠭ࠢࡩࡲ࠷࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡉࡓࡗࡉࡅࡠࡕࡗࡅࡗ࡚ࠧࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡦ࡯࠴ࠣࡁࠥ࠮ࠩࠡ࠿ࡁࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡶࡪࡳ࡯ࡷࡧࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡖࡄࡔࡤ࡙ࡔࡂࡔࡗࡉࡉ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡪࡳ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣർ"))
          logger.info(bstack1111_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠤൽ"))
        else:
          driver.execute_script(bstack1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡊࡔࡘࡃࡆࡡࡖࡘࡔࡖࠧࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡊࡼࡥ࡯ࡶࠫࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨൾ"))
      return bstack1l1l1ll11l_opy_
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢൿ") + str(e))
    return False
def bstack1ll1llll1l_opy_(driver, class_name, name, module_name, path, bstack111l1l1l_opy_):
  try:
    bstack1l1l1l111l_opy_ = [class_name] if not class_name is None else []
    bstack1l1l1lllll_opy_ = {
        bstack1111_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥ඀"): True,
        bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡈࡪࡺࡡࡪ࡮ࡶࠦඁ"): {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧං"): name,
            bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡘࡵ࡯ࡋࡧࠦඃ"): os.environ.get(bstack1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡔࡘࡒࡤࡏࡄࠨ඄")),
            bstack1111_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧඅ"): str(path),
            bstack1111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࡏ࡭ࡸࡺࠢආ"): [module_name, *bstack1l1l1l111l_opy_, name],
        },
        bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢඇ"): _1l1ll111ll_opy_(driver, bstack111l1l1l_opy_)
    }
    driver.execute_script(bstack1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡂࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝ࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡪࡵ࠱ࡶࡪࡹࠠ࠾ࠢࡱࡹࡱࡲ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝࠳ࡡ࠳ࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡘࡗࡇࡎࡔࡒࡒࡖ࡙ࡋࡒࠨ࠮ࠣࠬࡪࡼࡥ࡯ࡶࠬࠤࡂࡄࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡹࡧࡰࡕࡴࡤࡲࡸࡶ࡯ࡳࡶࡨࡶࡉࡧࡴࡢࠢࡀࠤࡪࡼࡥ࡯ࡶ࠱ࡨࡪࡺࡡࡪ࡮࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠡ࠿ࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡸࡦࡶࡔࡳࡣࡱࡷࡵࡵࡲࡵࡧࡵࡈࡦࡺࡡ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡆࡕࡗࡣࡊࡔࡄࠨ࠮ࠣࡿࠥࡪࡥࡵࡣ࡬ࡰ࠿ࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝࠳ࡡࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡊࡼࡥ࡯ࡶࠫࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤ࠭ࠧࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝࠳ࡡ࠳ࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠥࠦࠧඈ"), bstack1l1l1lllll_opy_)
    logger.info(bstack1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥඉ"))
  except Exception as bstack1l1l1ll111_opy_:
    logger.error(bstack1111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥඊ") + str(path) + bstack1111_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦඋ") + str(bstack1l1l1ll111_opy_))