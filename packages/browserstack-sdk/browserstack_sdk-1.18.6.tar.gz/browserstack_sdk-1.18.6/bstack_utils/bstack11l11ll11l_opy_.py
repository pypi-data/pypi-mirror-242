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
import json
import os
import threading
from bstack_utils.helper import bstack11lll1llll_opy_, bstack11l11l1l1_opy_, bstack11l1lll11_opy_, bstack111l1lll1_opy_, \
    bstack1l1111l1ll_opy_
def bstack1111ll111_opy_(bstack111llll1l1_opy_):
    for driver in bstack111llll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11ll1111_opy_(type, name, status, reason, bstack1lll1111ll_opy_, bstack1111l1l1_opy_):
    bstack1ll1l1111_opy_ = {
        bstack1l1ll1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬዪ"): type,
        bstack1l1ll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩያ"): {}
    }
    if type == bstack1l1ll1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩዬ"):
        bstack1ll1l1111_opy_[bstack1l1ll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫይ")][bstack1l1ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨዮ")] = bstack1lll1111ll_opy_
        bstack1ll1l1111_opy_[bstack1l1ll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ዯ")][bstack1l1ll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩደ")] = json.dumps(str(bstack1111l1l1_opy_))
    if type == bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ዱ"):
        bstack1ll1l1111_opy_[bstack1l1ll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩዲ")][bstack1l1ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬዳ")] = name
    if type == bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫዴ"):
        bstack1ll1l1111_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬድ")][bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪዶ")] = status
        if status == bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫዷ") and str(reason) != bstack1l1ll1l_opy_ (u"ࠧࠨዸ"):
            bstack1ll1l1111_opy_[bstack1l1ll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩዹ")][bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧዺ")] = json.dumps(str(reason))
    bstack111llllll_opy_ = bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ዻ").format(json.dumps(bstack1ll1l1111_opy_))
    return bstack111llllll_opy_
def bstack11l1lll1_opy_(url, config, logger, bstack1lllllll1l_opy_=False):
    hostname = bstack11l11l1l1_opy_(url)
    is_private = bstack111l1lll1_opy_(hostname)
    try:
        if is_private or bstack1lllllll1l_opy_:
            file_path = bstack11lll1llll_opy_(bstack1l1ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩዼ"), bstack1l1ll1l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩዽ"), logger)
            if os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩዾ")) and eval(
                    os.environ.get(bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪዿ"))):
                return
            if (bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪጀ") in config and not config[bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫጁ")]):
                os.environ[bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ጂ")] = str(True)
                bstack111lll1lll_opy_ = {bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫጃ"): hostname}
                bstack1l1111l1ll_opy_(bstack1l1ll1l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩጄ"), bstack1l1ll1l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩጅ"), bstack111lll1lll_opy_, logger)
    except Exception as e:
        pass
def bstack111l11ll1_opy_(caps, bstack111llll111_opy_):
    if bstack1l1ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ጆ") in caps:
        caps[bstack1l1ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧጇ")][bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ገ")] = True
        if bstack111llll111_opy_:
            caps[bstack1l1ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩጉ")][bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫጊ")] = bstack111llll111_opy_
    else:
        caps[bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨጋ")] = True
        if bstack111llll111_opy_:
            caps[bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬጌ")] = bstack111llll111_opy_
def bstack11l11l111l_opy_(bstack111llll11l_opy_):
    bstack111llll1ll_opy_ = bstack11l1lll11_opy_(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩግ"), bstack1l1ll1l_opy_ (u"࠭ࠧጎ"))
    if bstack111llll1ll_opy_ == bstack1l1ll1l_opy_ (u"ࠧࠨጏ") or bstack111llll1ll_opy_ == bstack1l1ll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩጐ"):
        threading.current_thread().testStatus = bstack111llll11l_opy_
    else:
        if bstack111llll11l_opy_ == bstack1l1ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ጑"):
            threading.current_thread().testStatus = bstack111llll11l_opy_