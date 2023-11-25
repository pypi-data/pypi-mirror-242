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
import json
import os
import threading
from bstack_utils.helper import bstack1l111lllll_opy_, bstack1ll1111ll1_opy_, bstack11lll111_opy_, bstack111lllll_opy_, \
    bstack1l11ll11ll_opy_
def bstack111l1111_opy_(bstack11l11l1l1l_opy_):
    for driver in bstack11l11l1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1ll_opy_(type, name, status, reason, bstack11l11l11_opy_, bstack1ll1llll_opy_):
    bstack1ll1lll111_opy_ = {
        bstack11lll1l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨኋ"): type,
        bstack11lll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬኌ"): {}
    }
    if type == bstack11lll1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬኍ"):
        bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ኎")][bstack11lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ኏")] = bstack11l11l11_opy_
        bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩነ")][bstack11lll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬኑ")] = json.dumps(str(bstack1ll1llll_opy_))
    if type == bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩኒ"):
        bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬና")][bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨኔ")] = name
    if type == bstack11lll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧን"):
        bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨኖ")][bstack11lll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ኗ")] = status
        if status == bstack11lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧኘ") and str(reason) != bstack11lll1l_opy_ (u"ࠣࠤኙ"):
            bstack1ll1lll111_opy_[bstack11lll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬኚ")][bstack11lll1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪኛ")] = json.dumps(str(reason))
    bstack111l1l1l1_opy_ = bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩኜ").format(json.dumps(bstack1ll1lll111_opy_))
    return bstack111l1l1l1_opy_
def bstack11l11ll11_opy_(url, config, logger, bstack1l111ll1l_opy_=False):
    hostname = bstack1ll1111ll1_opy_(url)
    is_private = bstack111lllll_opy_(hostname)
    try:
        if is_private or bstack1l111ll1l_opy_:
            file_path = bstack1l111lllll_opy_(bstack11lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬኝ"), bstack11lll1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬኞ"), logger)
            if os.environ.get(bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬኟ")) and eval(
                    os.environ.get(bstack11lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭አ"))):
                return
            if (bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ኡ") in config and not config[bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧኢ")]):
                os.environ[bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩኣ")] = str(True)
                bstack11l11l1l11_opy_ = {bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧኤ"): hostname}
                bstack1l11ll11ll_opy_(bstack11lll1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬእ"), bstack11lll1l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬኦ"), bstack11l11l1l11_opy_, logger)
    except Exception as e:
        pass
def bstack111ll1l1_opy_(caps, bstack11l11l1ll1_opy_):
    if bstack11lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩኧ") in caps:
        caps[bstack11lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪከ")][bstack11lll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩኩ")] = True
        if bstack11l11l1ll1_opy_:
            caps[bstack11lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬኪ")][bstack11lll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧካ")] = bstack11l11l1ll1_opy_
    else:
        caps[bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫኬ")] = True
        if bstack11l11l1ll1_opy_:
            caps[bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨክ")] = bstack11l11l1ll1_opy_
def bstack11l1ll111l_opy_(bstack11l11ll111_opy_):
    bstack11l11l1lll_opy_ = bstack11lll111_opy_(threading.current_thread(), bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬኮ"), bstack11lll1l_opy_ (u"ࠩࠪኯ"))
    if bstack11l11l1lll_opy_ == bstack11lll1l_opy_ (u"ࠪࠫኰ") or bstack11l11l1lll_opy_ == bstack11lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ኱"):
        threading.current_thread().testStatus = bstack11l11ll111_opy_
    else:
        if bstack11l11ll111_opy_ == bstack11lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬኲ"):
            threading.current_thread().testStatus = bstack11l11ll111_opy_