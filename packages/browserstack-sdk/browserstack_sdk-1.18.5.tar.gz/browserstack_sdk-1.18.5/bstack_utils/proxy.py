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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11llll1lll_opy_
def bstack11l1llll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11l1llllll_opy_(bstack11l1lll1ll_opy_, bstack11ll111111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11l1lll1ll_opy_):
        with open(bstack11l1lll1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11l1llll11_opy_(bstack11l1lll1ll_opy_):
        pac = get_pac(url=bstack11l1lll1ll_opy_)
    else:
        raise Exception(bstack1111_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪሲ").format(bstack11l1lll1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1111_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧሳ"), 80))
        bstack11l1llll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11l1llll1l_opy_ = bstack1111_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ሴ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11ll111111_opy_, bstack11l1llll1l_opy_)
    return proxy_url
def bstack1l1l11ll1_opy_(config):
    return bstack1111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩስ") in config or bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫሶ") in config
def bstack111ll1111_opy_(config):
    if not bstack1l1l11ll1_opy_(config):
        return
    if config.get(bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫሷ")):
        return config.get(bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬሸ"))
    if config.get(bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧሹ")):
        return config.get(bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨሺ"))
def bstack1l1llll11_opy_(config, bstack11ll111111_opy_):
    proxy = bstack111ll1111_opy_(config)
    proxies = {}
    if config.get(bstack1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨሻ")) or config.get(bstack1111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪሼ")):
        if proxy.endswith(bstack1111_opy_ (u"ࠧ࠯ࡲࡤࡧࠬሽ")):
            proxies = bstack111llllll_opy_(proxy, bstack11ll111111_opy_)
        else:
            proxies = {
                bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧሾ"): proxy
            }
    return proxies
def bstack111llllll_opy_(bstack11l1lll1ll_opy_, bstack11ll111111_opy_):
    proxies = {}
    global bstack11l1lllll1_opy_
    if bstack1111_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬሿ") in globals():
        return bstack11l1lllll1_opy_
    try:
        proxy = bstack11l1llllll_opy_(bstack11l1lll1ll_opy_, bstack11ll111111_opy_)
        if bstack1111_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥቀ") in proxy:
            proxies = {}
        elif bstack1111_opy_ (u"ࠦࡍ࡚ࡔࡑࠤቁ") in proxy or bstack1111_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦቂ") in proxy or bstack1111_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧቃ") in proxy:
            bstack11l1lll1l1_opy_ = proxy.split(bstack1111_opy_ (u"ࠢࠡࠤቄ"))
            if bstack1111_opy_ (u"ࠣ࠼࠲࠳ࠧቅ") in bstack1111_opy_ (u"ࠤࠥቆ").join(bstack11l1lll1l1_opy_[1:]):
                proxies = {
                    bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩቇ"): bstack1111_opy_ (u"ࠦࠧቈ").join(bstack11l1lll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ቉"): str(bstack11l1lll1l1_opy_[0]).lower() + bstack1111_opy_ (u"ࠨ࠺࠰࠱ࠥቊ") + bstack1111_opy_ (u"ࠢࠣቋ").join(bstack11l1lll1l1_opy_[1:])
                }
        elif bstack1111_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢቌ") in proxy:
            bstack11l1lll1l1_opy_ = proxy.split(bstack1111_opy_ (u"ࠤࠣࠦቍ"))
            if bstack1111_opy_ (u"ࠥ࠾࠴࠵ࠢ቎") in bstack1111_opy_ (u"ࠦࠧ቏").join(bstack11l1lll1l1_opy_[1:]):
                proxies = {
                    bstack1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫቐ"): bstack1111_opy_ (u"ࠨࠢቑ").join(bstack11l1lll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ቒ"): bstack1111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤቓ") + bstack1111_opy_ (u"ࠤࠥቔ").join(bstack11l1lll1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩቕ"): proxy
            }
    except Exception as e:
        print(bstack1111_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣቖ"), bstack11llll1lll_opy_.format(bstack11l1lll1ll_opy_, str(e)))
    bstack11l1lllll1_opy_ = proxies
    return proxies