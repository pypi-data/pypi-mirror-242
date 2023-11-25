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
import logging
logger = logging.getLogger(__name__)
class bstack1l1lll11l1_opy_:
    def bstack1l1lll1l11_opy_():
        bstack1l1lll111l_opy_ = {}
        try:
            bstack1l1lll11ll_opy_ = json.loads(os.environ[bstack11lll1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨೌ")])
            bstack11l11l1ll_opy_ = os.environ.get(bstack11lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆ್ࠩ"))
            if bstack11l11l1ll_opy_ is not None and eval(bstack11l11l1ll_opy_):
                bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ೎")] = bstack1l1lll11ll_opy_[bstack11lll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ೏")]
                bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ೐")] = bstack1l1lll11ll_opy_[bstack11lll1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ೑")]
                bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೒")] = bstack1l1lll11ll_opy_[bstack11lll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ೓")]
            else:
                bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠣࡱࡶࠦ೔")] = bstack1l1lll11ll_opy_[bstack11lll1l_opy_ (u"ࠤࡲࡷࠧೕ")]
                bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨೖ")] = bstack1l1lll11ll_opy_[bstack11lll1l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ೗")]
                bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ೘")] = bstack1l1lll11ll_opy_[bstack11lll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ೙")]
                bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೚")] = bstack1l1lll11ll_opy_[bstack11lll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ೛")]
            bstack1l1lll111l_opy_[bstack11lll1l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ೜")] = bstack1l1lll11ll_opy_.get(bstack11lll1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧೝ"), None)
        except Exception as error:
            logger.error(bstack11lll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥೞ") +  str(error))
        return bstack1l1lll111l_opy_