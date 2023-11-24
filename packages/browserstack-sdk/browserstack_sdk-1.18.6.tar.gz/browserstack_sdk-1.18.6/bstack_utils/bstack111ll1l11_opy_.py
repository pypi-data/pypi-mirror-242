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
import re
from bstack_utils.bstack11l11ll11l_opy_ import bstack11l11l111l_opy_
def bstack11l111llll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ኷")):
        return bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬኸ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬኹ")):
        return bstack1l1ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬኺ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬኻ")):
        return bstack1l1ll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬኼ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧኽ")):
        return bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬኾ")
def bstack11l11ll111_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ኿"), fixture_name))
def bstack11l11l1111_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ዀ"), fixture_name))
def bstack11l111ll1l_opy_(fixture_name):
    return bool(re.match(bstack1l1ll1l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭዁"), fixture_name))
def bstack11l11l1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩዂ")):
        return bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩዃ"), bstack1l1ll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧዄ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪዅ")):
        return bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ዆"), bstack1l1ll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ዇")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫወ")):
        return bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫዉ"), bstack1l1ll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬዊ")
    elif fixture_name.startswith(bstack1l1ll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬዋ")):
        return bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬዌ"), bstack1l1ll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧው")
    return None, None
def bstack11l11l11ll_opy_(hook_name):
    if hook_name in [bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫዎ"), bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨዏ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11l111ll11_opy_(hook_name):
    if hook_name in [bstack1l1ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨዐ"), bstack1l1ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧዑ")]:
        return bstack1l1ll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧዒ")
    elif hook_name in [bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩዓ"), bstack1l1ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩዔ")]:
        return bstack1l1ll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩዕ")
    elif hook_name in [bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪዖ"), bstack1l1ll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ዗")]:
        return bstack1l1ll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬዘ")
    elif hook_name in [bstack1l1ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫዙ"), bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫዚ")]:
        return bstack1l1ll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧዛ")
    return hook_name
def bstack11l111lll1_opy_(node, scenario):
    if hasattr(node, bstack1l1ll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧዜ")):
        parts = node.nodeid.rsplit(bstack1l1ll1l_opy_ (u"ࠨ࡛ࠣዝ"))
        params = parts[-1]
        return bstack1l1ll1l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢዞ").format(scenario.name, params)
    return scenario.name
def bstack1l1l11l1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1ll1l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪዟ")):
            examples = list(node.callspec.params[bstack1l1ll1l_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨዠ")].values())
        return examples
    except:
        return []
def bstack11l11l1l1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l11l1l11_opy_(report):
    try:
        status = bstack1l1ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዡ")
        if report.passed or (report.failed and hasattr(report, bstack1l1ll1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨዢ"))):
            status = bstack1l1ll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬዣ")
        elif report.skipped:
            status = bstack1l1ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧዤ")
        bstack11l11l111l_opy_(status)
    except:
        pass
def bstack1ll1lll1_opy_(status):
    try:
        bstack11l11l1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧዥ")
        if status == bstack1l1ll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨዦ"):
            bstack11l11l1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዧ")
        elif status == bstack1l1ll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫየ"):
            bstack11l11l1ll1_opy_ = bstack1l1ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬዩ")
        bstack11l11l111l_opy_(bstack11l11l1ll1_opy_)
    except:
        pass
def bstack11l11l11l1_opy_(item=None, report=None, summary=None, extra=None):
    return