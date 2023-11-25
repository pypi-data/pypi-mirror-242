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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l1l1ll1l1_opy_, bstack1ll11111_opy_, get_host_info, bstack1l1l1lllll_opy_, bstack1l1l11l1ll_opy_, bstack1l11l11111_opy_, \
    bstack1l11l1llll_opy_, bstack1l1111l1ll_opy_, bstack11l1l11l1_opy_, bstack1l11ll111l_opy_, bstack1l111lll1l_opy_, bstack1l1l1l1lll_opy_
from bstack_utils.bstack11l11lllll_opy_ import bstack11l1l11ll1_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack11l111llll_opy_
bstack111ll111l1_opy_ = [
    bstack11lll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨዩ"), bstack11lll1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩዪ"), bstack11lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨያ"), bstack11lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨዬ"),
    bstack11lll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪይ"), bstack11lll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪዮ"), bstack11lll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫዯ")
]
bstack111l1llll1_opy_ = bstack11lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫደ")
logger = logging.getLogger(__name__)
class bstack111lll111_opy_:
    bstack11l11lllll_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1l1l1lll_opy_(class_method=True)
    def launch(cls, bs_config, bstack111llll1ll_opy_):
        cls.bs_config = bs_config
        if not cls.bstack111ll1111l_opy_():
            return
        cls.bstack111llll1l1_opy_()
        bstack1l1l1l11l1_opy_ = bstack1l1l1lllll_opy_(bs_config)
        bstack1l1l1l1ll1_opy_ = bstack1l1l11l1ll_opy_(bs_config)
        data = {
            bstack11lll1l_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬዱ"): bstack11lll1l_opy_ (u"࠭ࡪࡴࡱࡱࠫዲ"),
            bstack11lll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ዳ"): bs_config.get(bstack11lll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ዴ"), bstack11lll1l_opy_ (u"ࠩࠪድ")),
            bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨዶ"): bs_config.get(bstack11lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧዷ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨዸ"): bs_config.get(bstack11lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨዹ")),
            bstack11lll1l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬዺ"): bs_config.get(bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫዻ"), bstack11lll1l_opy_ (u"ࠩࠪዼ")),
            bstack11lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧዽ"): datetime.datetime.now().isoformat(),
            bstack11lll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩዾ"): bstack1l11l11111_opy_(bs_config),
            bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨዿ"): get_host_info(),
            bstack11lll1l_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧጀ"): bstack1ll11111_opy_(),
            bstack11lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧጁ"): os.environ.get(bstack11lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧጂ")),
            bstack11lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧጃ"): os.environ.get(bstack11lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨጄ"), False),
            bstack11lll1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ጅ"): bstack1l1l1ll1l1_opy_(),
            bstack11lll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ጆ"): {
                bstack11lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ጇ"): bstack111llll1ll_opy_.get(bstack11lll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨገ"), bstack11lll1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨጉ")),
                bstack11lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬጊ"): bstack111llll1ll_opy_.get(bstack11lll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧጋ")),
                bstack11lll1l_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨጌ"): bstack111llll1ll_opy_.get(bstack11lll1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪግ"))
            }
        }
        config = {
            bstack11lll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫጎ"): (bstack1l1l1l11l1_opy_, bstack1l1l1l1ll1_opy_),
            bstack11lll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨጏ"): cls.default_headers()
        }
        response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ጐ"), cls.request_url(bstack11lll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩ጑")), data, config)
        if response.status_code != 200:
            os.environ[bstack11lll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩጒ")] = bstack11lll1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪጓ")
            os.environ[bstack11lll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ጔ")] = bstack11lll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫጕ")
            os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭጖")] = bstack11lll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨ጗")
            os.environ[bstack11lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪጘ")] = bstack11lll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣጙ")
            bstack111lll1111_opy_ = response.json()
            if bstack111lll1111_opy_ and bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬጚ")]:
                error_message = bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ጛ")]
                if bstack111lll1111_opy_[bstack11lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩጜ")] == bstack11lll1l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬጝ"):
                    logger.error(error_message)
                elif bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫጞ")] == bstack11lll1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨጟ"):
                    logger.info(error_message)
                elif bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ጠ")] == bstack11lll1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫጡ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11lll1l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢጢ"))
            return [None, None, None]
        logger.debug(bstack11lll1l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪጣ"))
        os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ጤ")] = bstack11lll1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ጥ")
        bstack111lll1111_opy_ = response.json()
        if bstack111lll1111_opy_.get(bstack11lll1l_opy_ (u"ࠩ࡭ࡻࡹ࠭ጦ")):
            os.environ[bstack11lll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫጧ")] = bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠫ࡯ࡽࡴࠨጨ")]
            os.environ[bstack11lll1l_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩጩ")] = json.dumps({
                bstack11lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨጪ"): bstack1l1l1l11l1_opy_,
                bstack11lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩጫ"): bstack1l1l1l1ll1_opy_
            })
        if bstack111lll1111_opy_.get(bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪጬ")):
            os.environ[bstack11lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨጭ")] = bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬጮ")]
        if bstack111lll1111_opy_.get(bstack11lll1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨጯ")):
            os.environ[bstack11lll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ጰ")] = str(bstack111lll1111_opy_[bstack11lll1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪጱ")])
        return [bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠧ࡫ࡹࡷࠫጲ")], bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪጳ")], bstack111lll1111_opy_[bstack11lll1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ጴ")]]
    @classmethod
    @bstack1l1l1l1lll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11lll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫጵ")] == bstack11lll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤጶ") or os.environ[bstack11lll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫጷ")] == bstack11lll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦጸ"):
            print(bstack11lll1l_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨጹ"))
            return {
                bstack11lll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨጺ"): bstack11lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨጻ"),
                bstack11lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫጼ"): bstack11lll1l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩጽ")
            }
        else:
            cls.bstack11l11lllll_opy_.shutdown()
            data = {
                bstack11lll1l_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨጾ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11lll1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧጿ"): cls.default_headers()
            }
            bstack1l111l11l1_opy_ = bstack11lll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨፀ").format(os.environ[bstack11lll1l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢፁ")])
            bstack111lll1l11_opy_ = cls.request_url(bstack1l111l11l1_opy_)
            response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"ࠩࡓ࡙࡙࠭ፂ"), bstack111lll1l11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11lll1l_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤፃ"))
    @classmethod
    def bstack111lll111l_opy_(cls):
        if cls.bstack11l11lllll_opy_ is None:
            return
        cls.bstack11l11lllll_opy_.shutdown()
    @classmethod
    def bstack1l1ll1111_opy_(cls):
        if cls.on():
            print(
                bstack11lll1l_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧፄ").format(os.environ[bstack11lll1l_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦፅ")]))
    @classmethod
    def bstack111llll1l1_opy_(cls):
        if cls.bstack11l11lllll_opy_ is not None:
            return
        cls.bstack11l11lllll_opy_ = bstack11l1l11ll1_opy_(cls.bstack111llll11l_opy_)
        cls.bstack11l11lllll_opy_.start()
    @classmethod
    def bstack111ll11lll_opy_(cls, bstack111ll11ll1_opy_, bstack111lll1ll1_opy_=bstack11lll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬፆ")):
        if not cls.on():
            return
        bstack111ll111_opy_ = bstack111ll11ll1_opy_[bstack11lll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫፇ")]
        bstack111ll1l1ll_opy_ = {
            bstack11lll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩፈ"): bstack11lll1l_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ፉ"),
            bstack11lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬፊ"): bstack11lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ፋ"),
            bstack11lll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ፌ"): bstack11lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬፍ"),
            bstack11lll1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫፎ"): bstack11lll1l_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬፏ"),
            bstack11lll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪፐ"): bstack11lll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧፑ"),
            bstack11lll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ፒ"): bstack11lll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧፓ"),
            bstack11lll1l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪፔ"): bstack11lll1l_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫፕ")
        }.get(bstack111ll111_opy_)
        if bstack111lll1ll1_opy_ == bstack11lll1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧፖ"):
            cls.bstack111llll1l1_opy_()
            cls.bstack11l11lllll_opy_.add(bstack111ll11ll1_opy_)
        elif bstack111lll1ll1_opy_ == bstack11lll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧፗ"):
            cls.bstack111llll11l_opy_([bstack111ll11ll1_opy_], bstack111lll1ll1_opy_)
    @classmethod
    @bstack1l1l1l1lll_opy_(class_method=True)
    def bstack111llll11l_opy_(cls, bstack111ll11ll1_opy_, bstack111lll1ll1_opy_=bstack11lll1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩፘ")):
        config = {
            bstack11lll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬፙ"): cls.default_headers()
        }
        response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪፚ"), cls.request_url(bstack111lll1ll1_opy_), bstack111ll11ll1_opy_, config)
        bstack1l1l1l1111_opy_ = response.json()
    @classmethod
    @bstack1l1l1l1lll_opy_(class_method=True)
    def bstack111ll1l111_opy_(cls, bstack111ll1ll11_opy_):
        bstack111ll1ll1l_opy_ = []
        for log in bstack111ll1ll11_opy_:
            bstack111lll11ll_opy_ = {
                bstack11lll1l_opy_ (u"࠭࡫ࡪࡰࡧࠫ፛"): bstack11lll1l_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩ፜"),
                bstack11lll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ፝"): log[bstack11lll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ፞")],
                bstack11lll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭፟"): log[bstack11lll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ፠")],
                bstack11lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬ፡"): {},
                bstack11lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ።"): log[bstack11lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ፣")],
            }
            if bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ፤") in log:
                bstack111lll11ll_opy_[bstack11lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ፥")] = log[bstack11lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ፦")]
            elif bstack11lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ፧") in log:
                bstack111lll11ll_opy_[bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ፨")] = log[bstack11lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭፩")]
            bstack111ll1ll1l_opy_.append(bstack111lll11ll_opy_)
        cls.bstack111ll11lll_opy_({
            bstack11lll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ፪"): bstack11lll1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ፫"),
            bstack11lll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ፬"): bstack111ll1ll1l_opy_
        })
    @classmethod
    @bstack1l1l1l1lll_opy_(class_method=True)
    def bstack111ll11111_opy_(cls, steps):
        bstack111ll11l11_opy_ = []
        for step in steps:
            bstack111ll1l11l_opy_ = {
                bstack11lll1l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ፭"): bstack11lll1l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ፮"),
                bstack11lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ፯"): step[bstack11lll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ፰")],
                bstack11lll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ፱"): step[bstack11lll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ፲")],
                bstack11lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ፳"): step[bstack11lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ፴")],
                bstack11lll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭፵"): step[bstack11lll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ፶")]
            }
            if bstack11lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭፷") in step:
                bstack111ll1l11l_opy_[bstack11lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፸")] = step[bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ፹")]
            elif bstack11lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ፺") in step:
                bstack111ll1l11l_opy_[bstack11lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ፻")] = step[bstack11lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ፼")]
            bstack111ll11l11_opy_.append(bstack111ll1l11l_opy_)
        cls.bstack111ll11lll_opy_({
            bstack11lll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ፽"): bstack11lll1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ፾"),
            bstack11lll1l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ፿"): bstack111ll11l11_opy_
        })
    @classmethod
    @bstack1l1l1l1lll_opy_(class_method=True)
    def bstack111llll111_opy_(cls, screenshot):
        cls.bstack111ll11lll_opy_({
            bstack11lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᎀ"): bstack11lll1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᎁ"),
            bstack11lll1l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᎂ"): [{
                bstack11lll1l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᎃ"): bstack11lll1l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᎄ"),
                bstack11lll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᎅ"): datetime.datetime.utcnow().isoformat() + bstack11lll1l_opy_ (u"࡛ࠧࠩᎆ"),
                bstack11lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᎇ"): screenshot[bstack11lll1l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᎈ")],
                bstack11lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᎉ"): screenshot[bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᎊ")]
            }]
        }, bstack111lll1ll1_opy_=bstack11lll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᎋ"))
    @classmethod
    @bstack1l1l1l1lll_opy_(class_method=True)
    def bstack1111111l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111ll11lll_opy_({
            bstack11lll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᎌ"): bstack11lll1l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᎍ"),
            bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᎎ"): {
                bstack11lll1l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᎏ"): cls.current_test_uuid(),
                bstack11lll1l_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤ᎐"): cls.bstack111lll1l1l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11lll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬ᎑"), None) is None or os.environ[bstack11lll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭᎒")] == bstack11lll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ᎓"):
            return False
        return True
    @classmethod
    def bstack111ll1111l_opy_(cls):
        return bstack1l111lll1l_opy_(cls.bs_config.get(bstack11lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᎔"), False))
    @staticmethod
    def request_url(url):
        return bstack11lll1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ᎕").format(bstack111l1llll1_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11lll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ᎖"): bstack11lll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭᎗"),
            bstack11lll1l_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧ᎘"): bstack11lll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ᎙")
        }
        if os.environ.get(bstack11lll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧ᎚"), None):
            headers[bstack11lll1l_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ᎛")] = bstack11lll1l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ᎜").format(os.environ[bstack11lll1l_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥ᎝")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ᎞"), None)
    @staticmethod
    def bstack111lll1l1l_opy_(driver):
        return {
            bstack1l1111l1ll_opy_(): bstack1l11l1llll_opy_(driver)
        }
    @staticmethod
    def bstack111ll111ll_opy_(exception_info, report):
        return [{bstack11lll1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᎟"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l111l1ll1_opy_(typename):
        if bstack11lll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᎠ") in typename:
            return bstack11lll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᎡ")
        return bstack11lll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᎢ")
    @staticmethod
    def bstack111lll1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111lll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111lll11l1_opy_(test, hook_name=None):
        bstack111ll11l1l_opy_ = test.parent
        if hook_name in [bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭Ꭳ"), bstack11lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᎤ"), bstack11lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᎥ"), bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꭶ")]:
            bstack111ll11l1l_opy_ = test
        scope = []
        while bstack111ll11l1l_opy_ is not None:
            scope.append(bstack111ll11l1l_opy_.name)
            bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack111ll1l1l1_opy_(hook_type):
        if hook_type == bstack11lll1l_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥᎧ"):
            return bstack11lll1l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥᎨ")
        elif hook_type == bstack11lll1l_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦᎩ"):
            return bstack11lll1l_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣᎪ")
    @staticmethod
    def bstack111l1lllll_opy_(bstack1ll1l111l_opy_):
        try:
            if not bstack111lll111_opy_.on():
                return bstack1ll1l111l_opy_
            if os.environ.get(bstack11lll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢᎫ"), None) == bstack11lll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᎬ"):
                tests = os.environ.get(bstack11lll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣᎭ"), None)
                if tests is None or tests == bstack11lll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᎮ"):
                    return bstack1ll1l111l_opy_
                bstack1ll1l111l_opy_ = tests.split(bstack11lll1l_opy_ (u"࠭ࠬࠨᎯ"))
                return bstack1ll1l111l_opy_
        except Exception as exc:
            print(bstack11lll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣᎰ"), str(exc))
        return bstack1ll1l111l_opy_
    @classmethod
    def bstack111ll1lll1_opy_(cls, event: str, bstack111ll11ll1_opy_: bstack11l111llll_opy_):
        bstack111ll1llll_opy_ = {
            bstack11lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᎱ"): event,
            bstack111ll11ll1_opy_.bstack111lllllll_opy_(): bstack111ll11ll1_opy_.bstack11l111l111_opy_(event)
        }
        bstack111lll111_opy_.bstack111ll11lll_opy_(bstack111ll1llll_opy_)