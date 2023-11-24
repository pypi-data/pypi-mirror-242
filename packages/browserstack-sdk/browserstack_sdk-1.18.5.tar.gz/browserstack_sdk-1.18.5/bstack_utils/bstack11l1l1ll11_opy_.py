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
import json
import os
import threading
from bstack_utils.helper import bstack1l111l11ll_opy_, bstack1lll1l1ll1_opy_, bstack1ll111l111_opy_, bstack1l1lllll1_opy_, \
    bstack1l11ll1l11_opy_
def bstack1llllll111_opy_(bstack11l11l1l11_opy_):
    for driver in bstack11l11l1l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1lll1_opy_(type, name, status, reason, bstack111l1l1l1_opy_, bstack1lll1ll11_opy_):
    bstack1l1lll1ll_opy_ = {
        bstack1111_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧኊ"): type,
        bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫኋ"): {}
    }
    if type == bstack1111_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫኌ"):
        bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ኍ")][bstack1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ኎")] = bstack111l1l1l1_opy_
        bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ኏")][bstack1111_opy_ (u"࠭ࡤࡢࡶࡤࠫነ")] = json.dumps(str(bstack1lll1ll11_opy_))
    if type == bstack1111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨኑ"):
        bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫኒ")][bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧና")] = name
    if type == bstack1111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ኔ"):
        bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧን")][bstack1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬኖ")] = status
        if status == bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ኗ") and str(reason) != bstack1111_opy_ (u"ࠢࠣኘ"):
            bstack1l1lll1ll_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫኙ")][bstack1111_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩኚ")] = json.dumps(str(reason))
    bstack1lll1l11ll_opy_ = bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨኛ").format(json.dumps(bstack1l1lll1ll_opy_))
    return bstack1lll1l11ll_opy_
def bstack1ll111lll1_opy_(url, config, logger, bstack1l11l1ll1_opy_=False):
    hostname = bstack1lll1l1ll1_opy_(url)
    is_private = bstack1l1lllll1_opy_(hostname)
    try:
        if is_private or bstack1l11l1ll1_opy_:
            file_path = bstack1l111l11ll_opy_(bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫኜ"), bstack1111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫኝ"), logger)
            if os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫኞ")) and eval(
                    os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬኟ"))):
                return
            if (bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬአ") in config and not config[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ኡ")]):
                os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨኢ")] = str(True)
                bstack11l11l1lll_opy_ = {bstack1111_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ኣ"): hostname}
                bstack1l11ll1l11_opy_(bstack1111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫኤ"), bstack1111_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫእ"), bstack11l11l1lll_opy_, logger)
    except Exception as e:
        pass
def bstack1lll1l1111_opy_(caps, bstack11l11l1l1l_opy_):
    if bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨኦ") in caps:
        caps[bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩኧ")][bstack1111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨከ")] = True
        if bstack11l11l1l1l_opy_:
            caps[bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫኩ")][bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ኪ")] = bstack11l11l1l1l_opy_
    else:
        caps[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪካ")] = True
        if bstack11l11l1l1l_opy_:
            caps[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧኬ")] = bstack11l11l1l1l_opy_
def bstack11l1ll1l11_opy_(bstack11l11l1ll1_opy_):
    bstack11l11ll111_opy_ = bstack1ll111l111_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫክ"), bstack1111_opy_ (u"ࠨࠩኮ"))
    if bstack11l11ll111_opy_ == bstack1111_opy_ (u"ࠩࠪኯ") or bstack11l11ll111_opy_ == bstack1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫኰ"):
        threading.current_thread().testStatus = bstack11l11l1ll1_opy_
    else:
        if bstack11l11l1ll1_opy_ == bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ኱"):
            threading.current_thread().testStatus = bstack11l11l1ll1_opy_