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
import re
from bstack_utils.bstack11l1ll1l1l_opy_ import bstack11l1ll111l_opy_
def bstack11l1ll11ll_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨቘ")):
        return bstack11lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ቙")
    elif fixture_name.startswith(bstack11lll1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨቚ")):
        return bstack11lll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨቛ")
    elif fixture_name.startswith(bstack11lll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨቜ")):
        return bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨቝ")
    elif fixture_name.startswith(bstack11lll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ቞")):
        return bstack11lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨ቟")
def bstack11l1ll1lll_opy_(fixture_name):
    return bool(re.match(bstack11lll1l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬበ"), fixture_name))
def bstack11l1l1ll1l_opy_(fixture_name):
    return bool(re.match(bstack11lll1l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩቡ"), fixture_name))
def bstack11l1l1llll_opy_(fixture_name):
    return bool(re.match(bstack11lll1l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩቢ"), fixture_name))
def bstack11l1ll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11lll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬባ")):
        return bstack11lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬቤ"), bstack11lll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪብ")
    elif fixture_name.startswith(bstack11lll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ቦ")):
        return bstack11lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ቧ"), bstack11lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬቨ")
    elif fixture_name.startswith(bstack11lll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧቩ")):
        return bstack11lll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧቪ"), bstack11lll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨቫ")
    elif fixture_name.startswith(bstack11lll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨቬ")):
        return bstack11lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨቭ"), bstack11lll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪቮ")
    return None, None
def bstack11l1lll11l_opy_(hook_name):
    if hook_name in [bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧቯ"), bstack11lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫተ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11l1ll1111_opy_(hook_name):
    if hook_name in [bstack11lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫቱ"), bstack11lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪቲ")]:
        return bstack11lll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪታ")
    elif hook_name in [bstack11lll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬቴ"), bstack11lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬት")]:
        return bstack11lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬቶ")
    elif hook_name in [bstack11lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ቷ"), bstack11lll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬቸ")]:
        return bstack11lll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨቹ")
    elif hook_name in [bstack11lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧቺ"), bstack11lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧቻ")]:
        return bstack11lll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪቼ")
    return hook_name
def bstack11l1l1ll11_opy_(node, scenario):
    if hasattr(node, bstack11lll1l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪች")):
        parts = node.nodeid.rsplit(bstack11lll1l_opy_ (u"ࠤ࡞ࠦቾ"))
        params = parts[-1]
        return bstack11lll1l_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥቿ").format(scenario.name, params)
    return scenario.name
def bstack11l1l1lll1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11lll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ኀ")):
            examples = list(node.callspec.params[bstack11lll1l_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫኁ")].values())
        return examples
    except:
        return []
def bstack11l1lll111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l1ll1l11_opy_(report):
    try:
        status = bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ኂ")
        if report.passed or (report.failed and hasattr(report, bstack11lll1l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤኃ"))):
            status = bstack11lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨኄ")
        elif report.skipped:
            status = bstack11lll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪኅ")
        bstack11l1ll111l_opy_(status)
    except:
        pass
def bstack11l11l111_opy_(status):
    try:
        bstack11l1l1l1ll_opy_ = bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪኆ")
        if status == bstack11lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫኇ"):
            bstack11l1l1l1ll_opy_ = bstack11lll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬኈ")
        elif status == bstack11lll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ኉"):
            bstack11l1l1l1ll_opy_ = bstack11lll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨኊ")
        bstack11l1ll111l_opy_(bstack11l1l1l1ll_opy_)
    except:
        pass
def bstack11l1ll11l1_opy_(item=None, report=None, summary=None, extra=None):
    return