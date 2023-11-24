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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l11ll1l1l_opy_, bstack1ll1l1l11_opy_, get_host_info, bstack1l11l1ll11_opy_, bstack1l11l1lll1_opy_, bstack1l11ll11l1_opy_, \
    bstack1l11l1l1l1_opy_, bstack1l11l1l111_opy_, bstack1111ll11l_opy_, bstack1l11ll1l11_opy_, bstack1l1l111ll1_opy_, bstack1l11lll1l1_opy_
from bstack_utils.bstack1l11l111l1_opy_ import bstack1l11l11l11_opy_
from bstack_utils.bstack1l1l1l1l11_opy_ import bstack1l1l1llll1_opy_
bstack1l11l11ll1_opy_ = [
    bstack1l1ll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨഫ"), bstack1l1ll1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩബ"), bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨഭ"), bstack1l1ll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨമ"),
    bstack1l1ll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪയ"), bstack1l1ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪര"), bstack1l1ll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫറ")
]
bstack1l11l1111l_opy_ = bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫല")
logger = logging.getLogger(__name__)
class bstack1l1l111l_opy_:
    bstack1l11l111l1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l11ll1lll_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1l11ll1ll1_opy_():
            return
        cls.bstack1l11l111ll_opy_()
        bstack1l11l1l1ll_opy_ = bstack1l11l1ll11_opy_(bs_config)
        bstack1l1l11111l_opy_ = bstack1l11l1lll1_opy_(bs_config)
        data = {
            bstack1l1ll1l_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬള"): bstack1l1ll1l_opy_ (u"࠭ࡪࡴࡱࡱࠫഴ"),
            bstack1l1ll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭വ"): bs_config.get(bstack1l1ll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ശ"), bstack1l1ll1l_opy_ (u"ࠩࠪഷ")),
            bstack1l1ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨസ"): bs_config.get(bstack1l1ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧഹ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1l1ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഺ"): bs_config.get(bstack1l1ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ഻")),
            bstack1l1ll1l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲ഼ࠬ"): bs_config.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫഽ"), bstack1l1ll1l_opy_ (u"ࠩࠪാ")),
            bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧി"): datetime.datetime.now().isoformat(),
            bstack1l1ll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩീ"): bstack1l11ll11l1_opy_(bs_config),
            bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨു"): get_host_info(),
            bstack1l1ll1l_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧൂ"): bstack1ll1l1l11_opy_(),
            bstack1l1ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧൃ"): os.environ.get(bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧൄ")),
            bstack1l1ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧ൅"): os.environ.get(bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨെ"), False),
            bstack1l1ll1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭േ"): bstack1l11ll1l1l_opy_(),
            bstack1l1ll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ൈ"): {
                bstack1l1ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭൉"): bstack1l11ll1lll_opy_.get(bstack1l1ll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨൊ"), bstack1l1ll1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨോ")),
                bstack1l1ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬൌ"): bstack1l11ll1lll_opy_.get(bstack1l1ll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴ്ࠧ")),
                bstack1l1ll1l_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨൎ"): bstack1l11ll1lll_opy_.get(bstack1l1ll1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ൏"))
            }
        }
        config = {
            bstack1l1ll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ൐"): (bstack1l11l1l1ll_opy_, bstack1l1l11111l_opy_),
            bstack1l1ll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ൑"): cls.default_headers()
        }
        response = bstack1111ll11l_opy_(bstack1l1ll1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭൒"), cls.request_url(bstack1l1ll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩ൓")), data, config)
        if response.status_code != 200:
            os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩൔ")] = bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪൕ")
            os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ൖ")] = bstack1l1ll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫൗ")
            os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭൘")] = bstack1l1ll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨ൙")
            os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ൚")] = bstack1l1ll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ൛")
            bstack1l11l11l1l_opy_ = response.json()
            if bstack1l11l11l1l_opy_ and bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ൜")]:
                error_message = bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൝")]
                if bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩ൞")] == bstack1l1ll1l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬൟ"):
                    logger.error(error_message)
                elif bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫൠ")] == bstack1l1ll1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨൡ"):
                    logger.info(error_message)
                elif bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ൢ")] == bstack1l1ll1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫൣ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1ll1l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢ൤"))
            return [None, None, None]
        logger.debug(bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ൥"))
        os.environ[bstack1l1ll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭൦")] = bstack1l1ll1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭൧")
        bstack1l11l11l1l_opy_ = response.json()
        if bstack1l11l11l1l_opy_.get(bstack1l1ll1l_opy_ (u"ࠩ࡭ࡻࡹ࠭൨")):
            os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫ൩")] = bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠫ࡯ࡽࡴࠨ൪")]
            os.environ[bstack1l1ll1l_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ൫")] = json.dumps({
                bstack1l1ll1l_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ൬"): bstack1l11l1l1ll_opy_,
                bstack1l1ll1l_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩ൭"): bstack1l1l11111l_opy_
            })
        if bstack1l11l11l1l_opy_.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ൮")):
            os.environ[bstack1l1ll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ൯")] = bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ൰")]
        if bstack1l11l11l1l_opy_.get(bstack1l1ll1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ൱")):
            os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭൲")] = str(bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ൳")])
        return [bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠧ࡫ࡹࡷࠫ൴")], bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ൵")], bstack1l11l11l1l_opy_[bstack1l1ll1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭൶")]]
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫ൷")] == bstack1l1ll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ൸") or os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ൹")] == bstack1l1ll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦൺ"):
            print(bstack1l1ll1l_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨൻ"))
            return {
                bstack1l1ll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨർ"): bstack1l1ll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨൽ"),
                bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫൾ"): bstack1l1ll1l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩൿ")
            }
        else:
            cls.bstack1l11l111l1_opy_.shutdown()
            data = {
                bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨ඀"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1l1ll1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧඁ"): cls.default_headers()
            }
            bstack1l11llll11_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨං").format(os.environ[bstack1l1ll1l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢඃ")])
            bstack1l1l1111ll_opy_ = cls.request_url(bstack1l11llll11_opy_)
            response = bstack1111ll11l_opy_(bstack1l1ll1l_opy_ (u"ࠩࡓ࡙࡙࠭඄"), bstack1l1l1111ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1ll1l_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤඅ"))
    @classmethod
    def bstack1l1l111lll_opy_(cls):
        if cls.bstack1l11l111l1_opy_ is None:
            return
        cls.bstack1l11l111l1_opy_.shutdown()
    @classmethod
    def bstack1lll11l111_opy_(cls):
        if cls.on():
            print(
                bstack1l1ll1l_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧආ").format(os.environ[bstack1l1ll1l_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦඇ")]))
    @classmethod
    def bstack1l11l111ll_opy_(cls):
        if cls.bstack1l11l111l1_opy_ is not None:
            return
        cls.bstack1l11l111l1_opy_ = bstack1l11l11l11_opy_(cls.bstack1l11llllll_opy_)
        cls.bstack1l11l111l1_opy_.start()
    @classmethod
    def bstack1l11ll111l_opy_(cls, bstack1l111lllll_opy_, bstack1l1l111111_opy_=bstack1l1ll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬඈ")):
        if not cls.on():
            return
        bstack1llll111ll_opy_ = bstack1l111lllll_opy_[bstack1l1ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫඉ")]
        bstack1l111lll1l_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩඊ"): bstack1l1ll1l_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭උ"),
            bstack1l1ll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬඌ"): bstack1l1ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ඍ"),
            bstack1l1ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ඎ"): bstack1l1ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬඏ"),
            bstack1l1ll1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫඐ"): bstack1l1ll1l_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬඑ"),
            bstack1l1ll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪඒ"): bstack1l1ll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧඓ"),
            bstack1l1ll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ඔ"): bstack1l1ll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧඕ"),
            bstack1l1ll1l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪඖ"): bstack1l1ll1l_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫ඗")
        }.get(bstack1llll111ll_opy_)
        if bstack1l1l111111_opy_ == bstack1l1ll1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ඘"):
            cls.bstack1l11l111ll_opy_()
            cls.bstack1l11l111l1_opy_.add(bstack1l111lllll_opy_)
        elif bstack1l1l111111_opy_ == bstack1l1ll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ඙"):
            cls.bstack1l11llllll_opy_([bstack1l111lllll_opy_], bstack1l1l111111_opy_)
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1l11llllll_opy_(cls, bstack1l111lllll_opy_, bstack1l1l111111_opy_=bstack1l1ll1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩක")):
        config = {
            bstack1l1ll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬඛ"): cls.default_headers()
        }
        response = bstack1111ll11l_opy_(bstack1l1ll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪග"), cls.request_url(bstack1l1l111111_opy_), bstack1l111lllll_opy_, config)
        bstack1l11ll11ll_opy_ = response.json()
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1l11l1llll_opy_(cls, bstack1l11lll1ll_opy_):
        bstack1l1l1111l1_opy_ = []
        for log in bstack1l11lll1ll_opy_:
            bstack1l11l11lll_opy_ = {
                bstack1l1ll1l_opy_ (u"࠭࡫ࡪࡰࡧࠫඝ"): bstack1l1ll1l_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩඞ"),
                bstack1l1ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧඟ"): log[bstack1l1ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨච")],
                bstack1l1ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ඡ"): log[bstack1l1ll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧජ")],
                bstack1l1ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬඣ"): {},
                bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧඤ"): log[bstack1l1ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨඥ")],
            }
            if bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨඦ") in log:
                bstack1l11l11lll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩට")] = log[bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪඨ")]
            elif bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫඩ") in log:
                bstack1l11l11lll_opy_[bstack1l1ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬඪ")] = log[bstack1l1ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ණ")]
            bstack1l1l1111l1_opy_.append(bstack1l11l11lll_opy_)
        cls.bstack1l11ll111l_opy_({
            bstack1l1ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫඬ"): bstack1l1ll1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬත"),
            bstack1l1ll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧථ"): bstack1l1l1111l1_opy_
        })
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1l111ll1ll_opy_(cls, steps):
        bstack1l11lll11l_opy_ = []
        for step in steps:
            bstack1l11l1ll1l_opy_ = {
                bstack1l1ll1l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨද"): bstack1l1ll1l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧධ"),
                bstack1l1ll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫන"): step[bstack1l1ll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ඲")],
                bstack1l1ll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪඳ"): step[bstack1l1ll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫප")],
                bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪඵ"): step[bstack1l1ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫබ")],
                bstack1l1ll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭භ"): step[bstack1l1ll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧම")]
            }
            if bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ඹ") in step:
                bstack1l11l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧය")] = step[bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨර")]
            elif bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ඼") in step:
                bstack1l11l1ll1l_opy_[bstack1l1ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪල")] = step[bstack1l1ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ඾")]
            bstack1l11lll11l_opy_.append(bstack1l11l1ll1l_opy_)
        cls.bstack1l11ll111l_opy_({
            bstack1l1ll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ඿"): bstack1l1ll1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪව"),
            bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬශ"): bstack1l11lll11l_opy_
        })
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1l111llll1_opy_(cls, screenshot):
        cls.bstack1l11ll111l_opy_({
            bstack1l1ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬෂ"): bstack1l1ll1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ස"),
            bstack1l1ll1l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨහ"): [{
                bstack1l1ll1l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩළ"): bstack1l1ll1l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧෆ"),
                bstack1l1ll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ෇"): datetime.datetime.utcnow().isoformat() + bstack1l1ll1l_opy_ (u"࡛ࠧࠩ෈"),
                bstack1l1ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ෉"): screenshot[bstack1l1ll1l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ්")],
                bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ෋"): screenshot[bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ෌")]
            }]
        }, bstack1l1l111111_opy_=bstack1l1ll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ෍"))
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1ll1l111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11ll111l_opy_({
            bstack1l1ll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ෎"): bstack1l1ll1l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫා"),
            bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪැ"): {
                bstack1l1ll1l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢෑ"): cls.current_test_uuid(),
                bstack1l1ll1l_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤි"): cls.bstack1l1l111l1l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬී"), None) is None or os.environ[bstack1l1ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ු")] == bstack1l1ll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ෕"):
            return False
        return True
    @classmethod
    def bstack1l11ll1ll1_opy_(cls):
        return bstack1l1l111ll1_opy_(cls.bs_config.get(bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫූ"), False))
    @staticmethod
    def request_url(url):
        return bstack1l1ll1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ෗").format(bstack1l11l1111l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1ll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨෘ"): bstack1l1ll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ෙ"),
            bstack1l1ll1l_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧේ"): bstack1l1ll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪෛ")
        }
        if os.environ.get(bstack1l1ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧො"), None):
            headers[bstack1l1ll1l_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧෝ")] = bstack1l1ll1l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫෞ").format(os.environ[bstack1l1ll1l_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥෟ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ෠"), None)
    @staticmethod
    def bstack1l1l111l1l_opy_(driver):
        return {
            bstack1l11l1l111_opy_(): bstack1l11l1l1l1_opy_(driver)
        }
    @staticmethod
    def bstack1l1l111l11_opy_(exception_info, report):
        return [{bstack1l1ll1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ෡"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l1l1l111l_opy_(typename):
        if bstack1l1ll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ෢") in typename:
            return bstack1l1ll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ෣")
        return bstack1l1ll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ෤")
    @staticmethod
    def bstack1l11lllll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1l111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11l1l11l_opy_(test, hook_name=None):
        bstack1l111lll11_opy_ = test.parent
        if hook_name in [bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭෥"), bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ෦"), bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ෧"), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭෨")]:
            bstack1l111lll11_opy_ = test
        scope = []
        while bstack1l111lll11_opy_ is not None:
            scope.append(bstack1l111lll11_opy_.name)
            bstack1l111lll11_opy_ = bstack1l111lll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l11ll1111_opy_(hook_type):
        if hook_type == bstack1l1ll1l_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥ෩"):
            return bstack1l1ll1l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥ෪")
        elif hook_type == bstack1l1ll1l_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦ෫"):
            return bstack1l1ll1l_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣ෬")
    @staticmethod
    def bstack1l11lll111_opy_(bstack1lll111l_opy_):
        try:
            if not bstack1l1l111l_opy_.on():
                return bstack1lll111l_opy_
            if os.environ.get(bstack1l1ll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢ෭"), None) == bstack1l1ll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣ෮"):
                tests = os.environ.get(bstack1l1ll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣ෯"), None)
                if tests is None or tests == bstack1l1ll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ෰"):
                    return bstack1lll111l_opy_
                bstack1lll111l_opy_ = tests.split(bstack1l1ll1l_opy_ (u"࠭ࠬࠨ෱"))
                return bstack1lll111l_opy_
        except Exception as exc:
            print(bstack1l1ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣෲ"), str(exc))
        return bstack1lll111l_opy_
    @classmethod
    def bstack1l11l11111_opy_(cls, event: str, bstack1l111lllll_opy_: bstack1l1l1llll1_opy_):
        bstack1l11llll1l_opy_ = {
            bstack1l1ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬෳ"): event,
            bstack1l111lllll_opy_.bstack1l1l1ll1ll_opy_(): bstack1l111lllll_opy_.bstack1l1l11lll1_opy_(event)
        }
        bstack1l1l111l_opy_.bstack1l11ll111l_opy_(bstack1l11llll1l_opy_)