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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11lllll1l1_opy_
def bstack11l1lll1l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11l1llllll_opy_(bstack11l1llll11_opy_, bstack11l1lllll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11l1llll11_opy_):
        with open(bstack11l1llll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11l1lll1l1_opy_(bstack11l1llll11_opy_):
        pac = get_pac(url=bstack11l1llll11_opy_)
    else:
        raise Exception(bstack11lll1l_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫሳ").format(bstack11l1llll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11lll1l_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨሴ"), 80))
        bstack11ll111111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11ll111111_opy_ = bstack11lll1l_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧስ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11l1lllll1_opy_, bstack11ll111111_opy_)
    return proxy_url
def bstack1llllll1ll_opy_(config):
    return bstack11lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪሶ") in config or bstack11lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬሷ") in config
def bstack11lllll1l_opy_(config):
    if not bstack1llllll1ll_opy_(config):
        return
    if config.get(bstack11lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬሸ")):
        return config.get(bstack11lll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ሹ"))
    if config.get(bstack11lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨሺ")):
        return config.get(bstack11lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩሻ"))
def bstack11lll1111_opy_(config, bstack11l1lllll1_opy_):
    proxy = bstack11lllll1l_opy_(config)
    proxies = {}
    if config.get(bstack11lll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩሼ")) or config.get(bstack11lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫሽ")):
        if proxy.endswith(bstack11lll1l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ሾ")):
            proxies = bstack1ll11l1l1_opy_(proxy, bstack11l1lllll1_opy_)
        else:
            proxies = {
                bstack11lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨሿ"): proxy
            }
    return proxies
def bstack1ll11l1l1_opy_(bstack11l1llll11_opy_, bstack11l1lllll1_opy_):
    proxies = {}
    global bstack11l1lll1ll_opy_
    if bstack11lll1l_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ቀ") in globals():
        return bstack11l1lll1ll_opy_
    try:
        proxy = bstack11l1llllll_opy_(bstack11l1llll11_opy_, bstack11l1lllll1_opy_)
        if bstack11lll1l_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦቁ") in proxy:
            proxies = {}
        elif bstack11lll1l_opy_ (u"ࠧࡎࡔࡕࡒࠥቂ") in proxy or bstack11lll1l_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧቃ") in proxy or bstack11lll1l_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨቄ") in proxy:
            bstack11l1llll1l_opy_ = proxy.split(bstack11lll1l_opy_ (u"ࠣࠢࠥቅ"))
            if bstack11lll1l_opy_ (u"ࠤ࠽࠳࠴ࠨቆ") in bstack11lll1l_opy_ (u"ࠥࠦቇ").join(bstack11l1llll1l_opy_[1:]):
                proxies = {
                    bstack11lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪቈ"): bstack11lll1l_opy_ (u"ࠧࠨ቉").join(bstack11l1llll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬቊ"): str(bstack11l1llll1l_opy_[0]).lower() + bstack11lll1l_opy_ (u"ࠢ࠻࠱࠲ࠦቋ") + bstack11lll1l_opy_ (u"ࠣࠤቌ").join(bstack11l1llll1l_opy_[1:])
                }
        elif bstack11lll1l_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣቍ") in proxy:
            bstack11l1llll1l_opy_ = proxy.split(bstack11lll1l_opy_ (u"ࠥࠤࠧ቎"))
            if bstack11lll1l_opy_ (u"ࠦ࠿࠵࠯ࠣ቏") in bstack11lll1l_opy_ (u"ࠧࠨቐ").join(bstack11l1llll1l_opy_[1:]):
                proxies = {
                    bstack11lll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬቑ"): bstack11lll1l_opy_ (u"ࠢࠣቒ").join(bstack11l1llll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧቓ"): bstack11lll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥቔ") + bstack11lll1l_opy_ (u"ࠥࠦቕ").join(bstack11l1llll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack11lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪቖ"): proxy
            }
    except Exception as e:
        print(bstack11lll1l_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ቗"), bstack11lllll1l1_opy_.format(bstack11l1llll11_opy_, str(e)))
    bstack11l1lll1ll_opy_ = proxies
    return proxies