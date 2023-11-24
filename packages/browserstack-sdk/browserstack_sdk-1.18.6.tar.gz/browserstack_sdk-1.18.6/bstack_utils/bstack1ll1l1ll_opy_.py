# coding: UTF-8
import sys
bstack11ll1_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1l1ll1l_opy_ (bstack11l1111_opy_):
    global bstack11l11l_opy_
    bstack1ll1ll1_opy_ = ord (bstack11l1111_opy_ [-1])
    bstack111l11l_opy_ = bstack11l1111_opy_ [:-1]
    bstack1l1l1l_opy_ = bstack1ll1ll1_opy_ % len (bstack111l11l_opy_)
    bstack1l1l1ll_opy_ = bstack111l11l_opy_ [:bstack1l1l1l_opy_] + bstack111l11l_opy_ [bstack1l1l1l_opy_:]
    if bstack11ll1_opy_:
        bstack1l11l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1ll11_opy_ + bstack1ll1ll1_opy_) % bstack1l1lll1_opy_) for bstack1ll11_opy_, char in enumerate (bstack1l1l1ll_opy_)])
    else:
        bstack1l11l11_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1ll11_opy_ + bstack1ll1ll1_opy_) % bstack1l1lll1_opy_) for bstack1ll11_opy_, char in enumerate (bstack1l1l1ll_opy_)])
    return eval (bstack1l11l11_opy_)
import os
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack1l111l1l1l_opy_ as bstack111ll11ll1_opy_
from bstack_utils.helper import bstack111lll1l_opy_, bstack1ll1ll11l1_opy_, bstack1l11l1ll11_opy_, bstack1l11l1lll1_opy_, bstack1ll1l1l11_opy_, get_host_info, bstack1l11ll1l1l_opy_, bstack1111ll11l_opy_, bstack1l11lll1l1_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11lll1l1_opy_(class_method=False)
def _111ll1ll11_opy_(driver, bstack11l1l111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1ll1l_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫጒ"): caps.get(bstack1l1ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪጓ"), None),
        bstack1l1ll1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩጔ"): bstack11l1l111_opy_.get(bstack1l1ll1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩጕ"), None),
        bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭጖"): caps.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭጗"), None),
        bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫጘ"): caps.get(bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫጙ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨጚ") + str(error))
  return response
def bstack11lll1l11_opy_(config):
  return config.get(bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬጛ"), False) or any([p.get(bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ጜ"), False) == True for p in config[bstack1l1ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪጝ")]])
def bstack1ll1l111l1_opy_(config, bstack1ll11lll11_opy_):
  try:
    if not bstack1ll1ll11l1_opy_(config):
      return False
    bstack111ll1l111_opy_ = config.get(bstack1l1ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨጞ"), False)
    bstack111lll1l11_opy_ = config[bstack1l1ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬጟ")][bstack1ll11lll11_opy_].get(bstack1l1ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪጠ"), None)
    if bstack111lll1l11_opy_ != None:
      bstack111ll1l111_opy_ = bstack111lll1l11_opy_
    bstack111lll1ll1_opy_ = os.getenv(bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩጡ")) is not None and len(os.getenv(bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪጢ"))) > 0 and os.getenv(bstack1l1ll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫጣ")) != bstack1l1ll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬጤ")
    return bstack111ll1l111_opy_ and bstack111lll1ll1_opy_
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨጥ") + str(error))
  return False
def bstack11l111lll_opy_(bstack111lll111l_opy_, test_tags):
  bstack111lll111l_opy_ = os.getenv(bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪጦ"))
  if bstack111lll111l_opy_ is None:
    return True
  bstack111lll111l_opy_ = json.loads(bstack111lll111l_opy_)
  try:
    include_tags = bstack111lll111l_opy_[bstack1l1ll1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨጧ")] if bstack1l1ll1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩጨ") in bstack111lll111l_opy_ and isinstance(bstack111lll111l_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪጩ")], list) else []
    exclude_tags = bstack111lll111l_opy_[bstack1l1ll1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫጪ")] if bstack1l1ll1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬጫ") in bstack111lll111l_opy_ and isinstance(bstack111lll111l_opy_[bstack1l1ll1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ጬ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤጭ") + str(error))
  return False
def bstack11111llll_opy_(config, bstack111ll11l1l_opy_, bstack111ll1lll1_opy_):
  bstack1l11l1l1ll_opy_ = bstack1l11l1ll11_opy_(config)
  bstack1l1l11111l_opy_ = bstack1l11l1lll1_opy_(config)
  if bstack1l11l1l1ll_opy_ is None or bstack1l1l11111l_opy_ is None:
    logger.error(bstack1l1ll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫጮ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬጯ"), bstack1l1ll1l_opy_ (u"ࠬࢁࡽࠨጰ")))
    data = {
        bstack1l1ll1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫጱ"): config[bstack1l1ll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬጲ")],
        bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫጳ"): config.get(bstack1l1ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬጴ"), os.path.basename(os.getcwd())),
        bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ጵ"): bstack111lll1l_opy_(),
        bstack1l1ll1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩጶ"): config.get(bstack1l1ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨጷ"), bstack1l1ll1l_opy_ (u"࠭ࠧጸ")),
        bstack1l1ll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧጹ"): {
            bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨጺ"): bstack111ll11l1l_opy_,
            bstack1l1ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬጻ"): bstack111ll1lll1_opy_,
            bstack1l1ll1l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧጼ"): __version__
        },
        bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ጽ"): settings,
        bstack1l1ll1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭ጾ"): bstack1l11ll1l1l_opy_(),
        bstack1l1ll1l_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭ጿ"): bstack1ll1l1l11_opy_(),
        bstack1l1ll1l_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩፀ"): get_host_info(),
        bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪፁ"): bstack1ll1ll11l1_opy_(config)
    }
    headers = {
        bstack1l1ll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨፂ"): bstack1l1ll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ፃ"),
    }
    config = {
        bstack1l1ll1l_opy_ (u"ࠫࡦࡻࡴࡩࠩፄ"): (bstack1l11l1l1ll_opy_, bstack1l1l11111l_opy_),
        bstack1l1ll1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ፅ"): headers
    }
    response = bstack1111ll11l_opy_(bstack1l1ll1l_opy_ (u"࠭ࡐࡐࡕࡗࠫፆ"), bstack111ll11ll1_opy_ + bstack1l1ll1l_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫፇ"), data, config)
    bstack1l11ll11ll_opy_ = response.json()
    if bstack1l11ll11ll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩፈ")]:
      parsed = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪፉ"), bstack1l1ll1l_opy_ (u"ࠪࡿࢂ࠭ፊ")))
      parsed[bstack1l1ll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬፋ")] = bstack1l11ll11ll_opy_[bstack1l1ll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪፌ")][bstack1l1ll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧፍ")]
      os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨፎ")] = json.dumps(parsed)
      return bstack1l11ll11ll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ፏ")][bstack1l1ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧፐ")], bstack1l11ll11ll_opy_[bstack1l1ll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨፑ")][bstack1l1ll1l_opy_ (u"ࠫ࡮ࡪࠧፒ")]
    else:
      logger.error(bstack1l1ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭ፓ") + bstack1l11ll11ll_opy_[bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧፔ")])
      if bstack1l11ll11ll_opy_[bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨፕ")] == bstack1l1ll1l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪፖ"):
        for bstack111ll1l1l1_opy_ in bstack1l11ll11ll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩፗ")]:
          logger.error(bstack111ll1l1l1_opy_[bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫፘ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1ll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧፙ") +  str(error))
    return None, None
def bstack11ll1lll1_opy_():
  if os.getenv(bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪፚ")) is None:
    return {
        bstack1l1ll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭፛"): bstack1l1ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭፜"),
        bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ፝"): bstack1l1ll1l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨ፞")
    }
  data = {bstack1l1ll1l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫ፟"): bstack111lll1l_opy_()}
  headers = {
      bstack1l1ll1l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ፠"): bstack1l1ll1l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭፡") + os.getenv(bstack1l1ll1l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ።")),
      bstack1l1ll1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭፣"): bstack1l1ll1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ፤")
  }
  response = bstack1111ll11l_opy_(bstack1l1ll1l_opy_ (u"ࠩࡓ࡙࡙࠭፥"), bstack111ll11ll1_opy_ + bstack1l1ll1l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬ፦"), data, { bstack1l1ll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ፧"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1ll1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨ፨") + datetime.utcnow().isoformat() + bstack1l1ll1l_opy_ (u"࡚࠭ࠨ፩"))
      return {bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ፪"): bstack1l1ll1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ፫"), bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ፬"): bstack1l1ll1l_opy_ (u"ࠪࠫ፭")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1ll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢ፮") + str(error))
    return {
        bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ፯"): bstack1l1ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ፰"),
        bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ፱"): str(error)
    }
def bstack11lll111l_opy_(caps, options):
  try:
    bstack111lll1111_opy_ = caps.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ፲"), {}).get(bstack1l1ll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭፳"), caps.get(bstack1l1ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ፴"), bstack1l1ll1l_opy_ (u"ࠫࠬ፵")))
    if bstack111lll1111_opy_:
      logger.warn(bstack1l1ll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ፶"))
      return False
    browser = caps.get(bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ፷"), bstack1l1ll1l_opy_ (u"ࠧࠨ፸")).lower()
    if browser != bstack1l1ll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ፹"):
      logger.warn(bstack1l1ll1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ፺"))
      return False
    browser_version = caps.get(bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ፻"), caps.get(bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭፼")))
    if browser_version and browser_version != bstack1l1ll1l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ፽") and int(browser_version.split(bstack1l1ll1l_opy_ (u"࠭࠮ࠨ፾"))[0]) <= 94:
      logger.warn(bstack1l1ll1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠷࠲ࠧ፿"))
      return False
    if not options is None:
      bstack111ll1llll_opy_ = options.to_capabilities().get(bstack1l1ll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᎀ"), {})
      if bstack1l1ll1l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᎁ") in bstack111ll1llll_opy_.get(bstack1l1ll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᎂ"), []):
        logger.warn(bstack1l1ll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᎃ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢᎄ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack111lll1l1l_opy_ = config.get(bstack1l1ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᎅ"), {})
    bstack111lll1l1l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᎆ")] = os.getenv(bstack1l1ll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᎇ"))
    bstack111lll11l1_opy_ = json.loads(os.getenv(bstack1l1ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᎈ"), bstack1l1ll1l_opy_ (u"ࠪࡿࢂ࠭ᎉ"))).get(bstack1l1ll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᎊ"))
    caps[bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᎋ")] = True
    if bstack1l1ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᎌ") in caps:
      caps[bstack1l1ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᎍ")][bstack1l1ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᎎ")] = bstack111lll1l1l_opy_
      caps[bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᎏ")][bstack1l1ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᎐")][bstack1l1ll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᎑")] = bstack111lll11l1_opy_
    else:
      caps[bstack1l1ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᎒")] = bstack111lll1l1l_opy_
      caps[bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᎓")][bstack1l1ll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᎔")] = bstack111lll11l1_opy_
  except Exception as error:
    logger.debug(bstack1l1ll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤ᎕") +  str(error))
def bstack11l11l111_opy_(driver, bstack111ll1l11l_opy_):
  try:
    session = driver.session_id
    if session:
      bstack111ll1l1ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111ll1l1ll_opy_ = False
      bstack111ll1l1ll_opy_ = url.scheme in [bstack1l1ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࠢ᎖"), bstack1l1ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ᎗")]
      if bstack111ll1l1ll_opy_:
        if bstack111ll1l11l_opy_:
          logger.info(bstack1l1ll1l_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦ᎘"))
          driver.execute_async_script(bstack1l1ll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡀࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛ࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡨࡱࠤࡂࠦࠨࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡗ࡙ࡇࡒࡕࡇࡇࠫ࠱ࠦࡦ࡯࠴ࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡆࡐࡔࡆࡉࡤ࡙ࡔࡂࡔࡗࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡪࡳ࠸ࠠ࠾ࠢࠫ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡳࡧࡰࡳࡻ࡫ࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡖࡘࡆࡘࡔࡆࡆࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠪࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡧࡰࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ᎙"))
          logger.info(bstack1l1ll1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠨ᎚"))
        else:
          driver.execute_script(bstack1l1ll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡇࡑࡕࡇࡊࡥࡓࡕࡑࡓࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ᎛"))
      return bstack111ll1l11l_opy_
  except Exception as e:
    logger.error(bstack1l1ll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ᎜") + str(e))
    return False
def bstack11lll1l1_opy_(driver, class_name, name, module_name, path, bstack11l1l111_opy_):
  try:
    bstack111ll1ll1l_opy_ = [class_name] if not class_name is None else []
    bstack111ll11lll_opy_ = {
        bstack1l1ll1l_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢ᎝"): True,
        bstack1l1ll1l_opy_ (u"ࠥࡸࡪࡹࡴࡅࡧࡷࡥ࡮ࡲࡳࠣ᎞"): {
            bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᎟"): name,
            bstack1l1ll1l_opy_ (u"ࠧࡺࡥࡴࡶࡕࡹࡳࡏࡤࠣᎠ"): os.environ.get(bstack1l1ll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬᎡ")),
            bstack1l1ll1l_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤᎢ"): str(path),
            bstack1l1ll1l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࡌࡪࡵࡷࠦᎣ"): [module_name, *bstack111ll1ll1l_opy_, name],
        },
        bstack1l1ll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᎤ"): _111ll1ll11_opy_(driver, bstack11l1l111_opy_)
    }
    driver.execute_script(bstack1l1ll1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࠿ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡࡡࡳࡩࡸࡱࡪࡴࡴࡴ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷ࡬࡮ࡹ࠮ࡳࡧࡶࠤࡂࠦ࡮ࡶ࡮࡯࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࠫࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡ࠰࡞࠰ࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡕࡔࡄࡒࡘࡖࡏࡓࡖࡈࡖࠬ࠲ࠠࠩࡧࡹࡩࡳࡺࠩࠡ࠿ࡁࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡶࡤࡴ࡙ࡸࡡ࡯ࡵࡳࡳࡷࡺࡥࡳࡆࡤࡸࡦࠦ࠽ࠡࡧࡹࡩࡳࡺ࠮ࡥࡧࡷࡥ࡮ࡲ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡯ࡳ࠯ࡴࡨࡷࠥࡃࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡵࡣࡳࡘࡷࡧ࡮ࡴࡲࡲࡶࡹ࡫ࡲࡅࡣࡷࡥࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠫࡸ࡭࡯ࡳ࠯ࡴࡨࡷ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡇࡑࡈࠬ࠲ࠠࡼࠢࡧࡩࡹࡧࡩ࡭࠼ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡ࠰࡞ࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࠪࠤࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࡡ࠰࡞࠰ࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠢࠣࠤᎥ"), bstack111ll11lll_opy_)
    logger.info(bstack1l1ll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᎦ"))
  except Exception as bstack111lll11ll_opy_:
    logger.error(bstack1l1ll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᎧ") + str(path) + bstack1l1ll1l_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᎨ") + str(bstack111lll11ll_opy_))