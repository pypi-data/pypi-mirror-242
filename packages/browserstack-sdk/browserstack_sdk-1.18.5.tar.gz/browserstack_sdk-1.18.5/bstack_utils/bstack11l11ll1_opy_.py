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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l1l1lll1l_opy_, bstack1111lll11_opy_, get_host_info, bstack1l1l1l1111_opy_, bstack1l1l11lll1_opy_, bstack1l111lllll_opy_, \
    bstack1l111l1ll1_opy_, bstack1l11lll111_opy_, bstack1ll1111l_opy_, bstack1l111llll1_opy_, bstack1l11l1ll11_opy_, bstack1l1l1ll1ll_opy_
from bstack_utils.bstack11l1l11ll1_opy_ import bstack11l1l1l11l_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack11l11l111l_opy_
bstack111ll11111_opy_ = [
    bstack1111_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧየ"), bstack1111_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨዩ"), bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧዪ"), bstack1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧያ"),
    bstack1111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩዬ"), bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩይ"), bstack1111_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪዮ")
]
bstack111lll1lll_opy_ = bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪዯ")
logger = logging.getLogger(__name__)
class bstack1l1lll11l_opy_:
    bstack11l1l11ll1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1l1ll1ll_opy_(class_method=True)
    def launch(cls, bs_config, bstack111llll111_opy_):
        cls.bs_config = bs_config
        if not cls.bstack111lll1l11_opy_():
            return
        cls.bstack111ll11l1l_opy_()
        bstack1l1l1l11l1_opy_ = bstack1l1l1l1111_opy_(bs_config)
        bstack1l1l1l1ll1_opy_ = bstack1l1l11lll1_opy_(bs_config)
        data = {
            bstack1111_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫደ"): bstack1111_opy_ (u"ࠬࡰࡳࡰࡰࠪዱ"),
            bstack1111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬዲ"): bs_config.get(bstack1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬዳ"), bstack1111_opy_ (u"ࠨࠩዴ")),
            bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧድ"): bs_config.get(bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ዶ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧዷ"): bs_config.get(bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧዸ")),
            bstack1111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫዹ"): bs_config.get(bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪዺ"), bstack1111_opy_ (u"ࠨࠩዻ")),
            bstack1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡠࡶ࡬ࡱࡪ࠭ዼ"): datetime.datetime.now().isoformat(),
            bstack1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨዽ"): bstack1l111lllll_opy_(bs_config),
            bstack1111_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧዾ"): get_host_info(),
            bstack1111_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ዿ"): bstack1111lll11_opy_(),
            bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ጀ"): os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ጁ")),
            bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ጂ"): os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧጃ"), False),
            bstack1111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬጄ"): bstack1l1l1lll1l_opy_(),
            bstack1111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬጅ"): {
                bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬጆ"): bstack111llll111_opy_.get(bstack1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧጇ"), bstack1111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧገ")),
                bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫጉ"): bstack111llll111_opy_.get(bstack1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ጊ")),
                bstack1111_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧጋ"): bstack111llll111_opy_.get(bstack1111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩጌ"))
            }
        }
        config = {
            bstack1111_opy_ (u"ࠬࡧࡵࡵࡪࠪግ"): (bstack1l1l1l11l1_opy_, bstack1l1l1l1ll1_opy_),
            bstack1111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧጎ"): cls.default_headers()
        }
        response = bstack1ll1111l_opy_(bstack1111_opy_ (u"ࠧࡑࡑࡖࡘࠬጏ"), cls.request_url(bstack1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳࠨጐ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ጑")] = bstack1111_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩጒ")
            os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬጓ")] = bstack1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪጔ")
            os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬጕ")] = bstack1111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ጖")
            os.environ[bstack1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ጗")] = bstack1111_opy_ (u"ࠤࡱࡹࡱࡲࠢጘ")
            bstack111ll1lll1_opy_ = response.json()
            if bstack111ll1lll1_opy_ and bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫጙ")]:
                error_message = bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬጚ")]
                if bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡘࡾࡶࡥࠨጛ")] == bstack1111_opy_ (u"࠭ࡅࡓࡔࡒࡖࡤࡏࡎࡗࡃࡏࡍࡉࡥࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࠫጜ"):
                    logger.error(error_message)
                elif bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪጝ")] == bstack1111_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠧጞ"):
                    logger.info(error_message)
                elif bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬጟ")] == bstack1111_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡖࡈࡐࡥࡄࡆࡒࡕࡉࡈࡇࡔࡆࡆࠪጠ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1111_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨጡ"))
            return [None, None, None]
        logger.debug(bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩጢ"))
        os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬጣ")] = bstack1111_opy_ (u"ࠧࡵࡴࡸࡩࠬጤ")
        bstack111ll1lll1_opy_ = response.json()
        if bstack111ll1lll1_opy_.get(bstack1111_opy_ (u"ࠨ࡬ࡺࡸࠬጥ")):
            os.environ[bstack1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪጦ")] = bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠪ࡮ࡼࡺࠧጧ")]
            os.environ[bstack1111_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨጨ")] = json.dumps({
                bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧጩ"): bstack1l1l1l11l1_opy_,
                bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨጪ"): bstack1l1l1l1ll1_opy_
            })
        if bstack111ll1lll1_opy_.get(bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩጫ")):
            os.environ[bstack1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧጬ")] = bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫጭ")]
        if bstack111ll1lll1_opy_.get(bstack1111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧጮ")):
            os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬጯ")] = str(bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩጰ")])
        return [bstack111ll1lll1_opy_[bstack1111_opy_ (u"࠭ࡪࡸࡶࠪጱ")], bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩጲ")], bstack111ll1lll1_opy_[bstack1111_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬጳ")]]
    @classmethod
    @bstack1l1l1ll1ll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪጴ")] == bstack1111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣጵ") or os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪጶ")] == bstack1111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥጷ"):
            print(bstack1111_opy_ (u"࠭ࡅ࡙ࡅࡈࡔ࡙ࡏࡏࡏࠢࡌࡒࠥࡹࡴࡰࡲࡅࡹ࡮ࡲࡤࡖࡲࡶࡸࡷ࡫ࡡ࡮ࠢࡕࡉࡖ࡛ࡅࡔࡖࠣࡘࡔࠦࡔࡆࡕࡗࠤࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠤ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧጸ"))
            return {
                bstack1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧጹ"): bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧጺ"),
                bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪጻ"): bstack1111_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨጼ")
            }
        else:
            cls.bstack11l1l11ll1_opy_.shutdown()
            data = {
                bstack1111_opy_ (u"ࠫࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࠧጽ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1111_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ጾ"): cls.default_headers()
            }
            bstack1l111l1l1l_opy_ = bstack1111_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧጿ").format(os.environ[bstack1111_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨፀ")])
            bstack111ll1l1l1_opy_ = cls.request_url(bstack1l111l1l1l_opy_)
            response = bstack1ll1111l_opy_(bstack1111_opy_ (u"ࠨࡒࡘࡘࠬፁ"), bstack111ll1l1l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1111_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣፂ"))
    @classmethod
    def bstack111ll1l11l_opy_(cls):
        if cls.bstack11l1l11ll1_opy_ is None:
            return
        cls.bstack11l1l11ll1_opy_.shutdown()
    @classmethod
    def bstack1lll11ll1l_opy_(cls):
        if cls.on():
            print(
                bstack1111_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭ፃ").format(os.environ[bstack1111_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥፄ")]))
    @classmethod
    def bstack111ll11l1l_opy_(cls):
        if cls.bstack11l1l11ll1_opy_ is not None:
            return
        cls.bstack11l1l11ll1_opy_ = bstack11l1l1l11l_opy_(cls.bstack111lll1l1l_opy_)
        cls.bstack11l1l11ll1_opy_.start()
    @classmethod
    def bstack111l1llll1_opy_(cls, bstack111ll11l11_opy_, bstack111lll11l1_opy_=bstack1111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫፅ")):
        if not cls.on():
            return
        bstack1ll1l1111l_opy_ = bstack111ll11l11_opy_[bstack1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪፆ")]
        bstack111ll1l1ll_opy_ = {
            bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨፇ"): bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬፈ"),
            bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫፉ"): bstack1111_opy_ (u"ࠪࡘࡪࡹࡴࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬፊ"),
            bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬፋ"): bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡰ࡯ࡰࡱࡧࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫፌ"),
            bstack1111_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪፍ"): bstack1111_opy_ (u"ࠧࡍࡱࡪࡣ࡚ࡶ࡬ࡰࡣࡧࠫፎ"),
            bstack1111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩፏ"): bstack1111_opy_ (u"ࠩࡋࡳࡴࡱ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ፐ"),
            bstack1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬፑ"): bstack1111_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ፒ"),
            bstack1111_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩፓ"): bstack1111_opy_ (u"࠭ࡃࡃࡖࡢ࡙ࡵࡲ࡯ࡢࡦࠪፔ")
        }.get(bstack1ll1l1111l_opy_)
        if bstack111lll11l1_opy_ == bstack1111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ፕ"):
            cls.bstack111ll11l1l_opy_()
            cls.bstack11l1l11ll1_opy_.add(bstack111ll11l11_opy_)
        elif bstack111lll11l1_opy_ == bstack1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ፖ"):
            cls.bstack111lll1l1l_opy_([bstack111ll11l11_opy_], bstack111lll11l1_opy_)
    @classmethod
    @bstack1l1l1ll1ll_opy_(class_method=True)
    def bstack111lll1l1l_opy_(cls, bstack111ll11l11_opy_, bstack111lll11l1_opy_=bstack1111_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨፗ")):
        config = {
            bstack1111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫፘ"): cls.default_headers()
        }
        response = bstack1ll1111l_opy_(bstack1111_opy_ (u"ࠫࡕࡕࡓࡕࠩፙ"), cls.request_url(bstack111lll11l1_opy_), bstack111ll11l11_opy_, config)
        bstack1l1l11l1ll_opy_ = response.json()
    @classmethod
    @bstack1l1l1ll1ll_opy_(class_method=True)
    def bstack111ll1l111_opy_(cls, bstack111ll1llll_opy_):
        bstack111ll111l1_opy_ = []
        for log in bstack111ll1llll_opy_:
            bstack111lll1ll1_opy_ = {
                bstack1111_opy_ (u"ࠬࡱࡩ࡯ࡦࠪፚ"): bstack1111_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨ፛"),
                bstack1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭፜"): log[bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ፝")],
                bstack1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ፞"): log[bstack1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭፟")],
                bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫ፠"): {},
                bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭፡"): log[bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ።")],
            }
            if bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፣") in log:
                bstack111lll1ll1_opy_[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ፤")] = log[bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ፥")]
            elif bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ፦") in log:
                bstack111lll1ll1_opy_[bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ፧")] = log[bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ፨")]
            bstack111ll111l1_opy_.append(bstack111lll1ll1_opy_)
        cls.bstack111l1llll1_opy_({
            bstack1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ፩"): bstack1111_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ፪"),
            bstack1111_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭፫"): bstack111ll111l1_opy_
        })
    @classmethod
    @bstack1l1l1ll1ll_opy_(class_method=True)
    def bstack111ll1111l_opy_(cls, steps):
        bstack111ll1ll1l_opy_ = []
        for step in steps:
            bstack111lll1111_opy_ = {
                bstack1111_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ፬"): bstack1111_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭፭"),
                bstack1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ፮"): step[bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ፯")],
                bstack1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ፰"): step[bstack1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ፱")],
                bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ፲"): step[bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ፳")],
                bstack1111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ፴"): step[bstack1111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭፵")]
            }
            if bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ፶") in step:
                bstack111lll1111_opy_[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭፷")] = step[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፸")]
            elif bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ፹") in step:
                bstack111lll1111_opy_[bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ፺")] = step[bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ፻")]
            bstack111ll1ll1l_opy_.append(bstack111lll1111_opy_)
        cls.bstack111l1llll1_opy_({
            bstack1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ፼"): bstack1111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ፽"),
            bstack1111_opy_ (u"࠭࡬ࡰࡩࡶࠫ፾"): bstack111ll1ll1l_opy_
        })
    @classmethod
    @bstack1l1l1ll1ll_opy_(class_method=True)
    def bstack111ll11ll1_opy_(cls, screenshot):
        cls.bstack111l1llll1_opy_({
            bstack1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ፿"): bstack1111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᎀ"),
            bstack1111_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᎁ"): [{
                bstack1111_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᎂ"): bstack1111_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ᎃ"),
                bstack1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᎄ"): datetime.datetime.utcnow().isoformat() + bstack1111_opy_ (u"࡚࠭ࠨᎅ"),
                bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᎆ"): screenshot[bstack1111_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᎇ")],
                bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᎈ"): screenshot[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᎉ")]
            }]
        }, bstack111lll11l1_opy_=bstack1111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᎊ"))
    @classmethod
    @bstack1l1l1ll1ll_opy_(class_method=True)
    def bstack1ll11l111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111l1llll1_opy_({
            bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᎋ"): bstack1111_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᎌ"),
            bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᎍ"): {
                bstack1111_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᎎ"): cls.current_test_uuid(),
                bstack1111_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣᎏ"): cls.bstack111l1lllll_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫ᎐"), None) is None or os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬ᎑")] == bstack1111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᎒"):
            return False
        return True
    @classmethod
    def bstack111lll1l11_opy_(cls):
        return bstack1l11l1ll11_opy_(cls.bs_config.get(bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᎓"), False))
    @staticmethod
    def request_url(url):
        return bstack1111_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭᎔").format(bstack111lll1lll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ᎕"): bstack1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ᎖"),
            bstack1111_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭᎗"): bstack1111_opy_ (u"ࠫࡹࡸࡵࡦࠩ᎘")
        }
        if os.environ.get(bstack1111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭᎙"), None):
            headers[bstack1111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᎚")] = bstack1111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ᎛").format(os.environ[bstack1111_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠤ᎜")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭᎝"), None)
    @staticmethod
    def bstack111l1lllll_opy_(driver):
        return {
            bstack1l11lll111_opy_(): bstack1l111l1ll1_opy_(driver)
        }
    @staticmethod
    def bstack111ll1ll11_opy_(exception_info, report):
        return [{bstack1111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᎞"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l11lll11l_opy_(typename):
        if bstack1111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ᎟") in typename:
            return bstack1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᎠ")
        return bstack1111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᎡ")
    @staticmethod
    def bstack111ll111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lll11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111llll1ll_opy_(test, hook_name=None):
        bstack111lll111l_opy_ = test.parent
        if hook_name in [bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᎢ"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᎣ"), bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᎤ"), bstack1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᎥ")]:
            bstack111lll111l_opy_ = test
        scope = []
        while bstack111lll111l_opy_ is not None:
            scope.append(bstack111lll111l_opy_.name)
            bstack111lll111l_opy_ = bstack111lll111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack111ll11lll_opy_(hook_type):
        if hook_type == bstack1111_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤᎦ"):
            return bstack1111_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤᎧ")
        elif hook_type == bstack1111_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥᎨ"):
            return bstack1111_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢᎩ")
    @staticmethod
    def bstack111lll11ll_opy_(bstack11ll1lll_opy_):
        try:
            if not bstack1l1lll11l_opy_.on():
                return bstack11ll1lll_opy_
            if os.environ.get(bstack1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨᎪ"), None) == bstack1111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᎫ"):
                tests = os.environ.get(bstack1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢᎬ"), None)
                if tests is None or tests == bstack1111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᎭ"):
                    return bstack11ll1lll_opy_
                bstack11ll1lll_opy_ = tests.split(bstack1111_opy_ (u"ࠬ࠲ࠧᎮ"))
                return bstack11ll1lll_opy_
        except Exception as exc:
            print(bstack1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢᎯ"), str(exc))
        return bstack11ll1lll_opy_
    @classmethod
    def bstack111llll11l_opy_(cls, event: str, bstack111ll11l11_opy_: bstack11l11l111l_opy_):
        bstack111llll1l1_opy_ = {
            bstack1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᎰ"): event,
            bstack111ll11l11_opy_.bstack11l11111ll_opy_(): bstack111ll11l11_opy_.bstack11l1111l11_opy_(event)
        }
        bstack1l1lll11l_opy_.bstack111l1llll1_opy_(bstack111llll1l1_opy_)