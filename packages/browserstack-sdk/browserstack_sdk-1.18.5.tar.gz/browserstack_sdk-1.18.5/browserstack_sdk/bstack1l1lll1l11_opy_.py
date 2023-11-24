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
import logging
logger = logging.getLogger(__name__)
class bstack1l1lll11l1_opy_:
    def bstack1l1lll111l_opy_():
        bstack1l1lll1l1l_opy_ = {}
        try:
            bstack1l1lll11ll_opy_ = json.loads(os.environ[bstack1111_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧೋ")])
            bstack1l1ll11l1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨೌ"))
            if bstack1l1ll11l1_opy_ is not None and eval(bstack1l1ll11l1_opy_):
                bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫್ࠢ")] = bstack1l1lll11ll_opy_[bstack1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ೎")]
                bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ೏")] = bstack1l1lll11ll_opy_[bstack1111_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ೐")]
                bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ೑")] = bstack1l1lll11ll_opy_[bstack1111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೒")]
            else:
                bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠢࡰࡵࠥ೓")] = bstack1l1lll11ll_opy_[bstack1111_opy_ (u"ࠣࡱࡶࠦ೔")]
                bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧೕ")] = bstack1l1lll11ll_opy_[bstack1111_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨೖ")]
                bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ೗")] = bstack1l1lll11ll_opy_[bstack1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ೘")]
                bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ೙")] = bstack1l1lll11ll_opy_[bstack1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೚")]
            bstack1l1lll1l1l_opy_[bstack1111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ೛")] = bstack1l1lll11ll_opy_.get(bstack1111_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ೜"), None)
        except Exception as error:
            logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡥࡹࡧ࠺ࠡࠤೝ") +  str(error))
        return bstack1l1lll1l1l_opy_