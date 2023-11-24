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
import re
from bstack_utils.bstack11l1l1ll11_opy_ import bstack11l1ll1l11_opy_
def bstack11l1ll1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ቗")):
        return bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧቘ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ቙")):
        return bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧቚ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧቛ")):
        return bstack1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧቜ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩቝ")):
        return bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧ቞")
def bstack11l1ll1l1l_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ቟"), fixture_name))
def bstack11l1l1l1ll_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨበ"), fixture_name))
def bstack11l1ll111l_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨቡ"), fixture_name))
def bstack11l1lll11l_opy_(fixture_name):
    if fixture_name.startswith(bstack1111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫቢ")):
        return bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫባ"), bstack1111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩቤ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬብ")):
        return bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬቦ"), bstack1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫቧ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ቨ")):
        return bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ቩ"), bstack1111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧቪ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧቫ")):
        return bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧቬ"), bstack1111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩቭ")
    return None, None
def bstack11l1lll111_opy_(hook_name):
    if hook_name in [bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ቮ"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪቯ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11l1ll1ll1_opy_(hook_name):
    if hook_name in [bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪተ"), bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩቱ")]:
        return bstack1111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩቲ")
    elif hook_name in [bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫታ"), bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫቴ")]:
        return bstack1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫት")
    elif hook_name in [bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬቶ"), bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫቷ")]:
        return bstack1111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧቸ")
    elif hook_name in [bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ቹ"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ቺ")]:
        return bstack1111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩቻ")
    return hook_name
def bstack11l1ll11l1_opy_(node, scenario):
    if hasattr(node, bstack1111_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩቼ")):
        parts = node.nodeid.rsplit(bstack1111_opy_ (u"ࠣ࡝ࠥች"))
        params = parts[-1]
        return bstack1111_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤቾ").format(scenario.name, params)
    return scenario.name
def bstack11l1ll1111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1111_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬቿ")):
            examples = list(node.callspec.params[bstack1111_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪኀ")].values())
        return examples
    except:
        return []
def bstack11l1l1lll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l1ll11ll_opy_(report):
    try:
        status = bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬኁ")
        if report.passed or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣኂ"))):
            status = bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧኃ")
        elif report.skipped:
            status = bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩኄ")
        bstack11l1ll1l11_opy_(status)
    except:
        pass
def bstack111l11ll1_opy_(status):
    try:
        bstack11l1l1llll_opy_ = bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩኅ")
        if status == bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪኆ"):
            bstack11l1l1llll_opy_ = bstack1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫኇ")
        elif status == bstack1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ኈ"):
            bstack11l1l1llll_opy_ = bstack1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ኉")
        bstack11l1ll1l11_opy_(bstack11l1l1llll_opy_)
    except:
        pass
def bstack11l1l1ll1l_opy_(item=None, report=None, summary=None, extra=None):
    return