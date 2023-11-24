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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack11ll1l1lll_opy_
def bstack11l11lllll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11l11llll1_opy_(bstack11l11ll1ll_opy_, bstack11l11ll1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11l11ll1ll_opy_):
        with open(bstack11l11ll1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11l11lllll_opy_(bstack11l11ll1ll_opy_):
        pac = get_pac(url=bstack11l11ll1ll_opy_)
    else:
        raise Exception(bstack1l1ll1l_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨኒ").format(bstack11l11ll1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1ll1l_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥና"), 80))
        bstack11l11lll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11l11lll11_opy_ = bstack1l1ll1l_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫኔ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11l11ll1l1_opy_, bstack11l11lll11_opy_)
    return proxy_url
def bstack1l1ll1l11_opy_(config):
    return bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧን") in config or bstack1l1ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩኖ") in config
def bstack1l11111l_opy_(config):
    if not bstack1l1ll1l11_opy_(config):
        return
    if config.get(bstack1l1ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩኗ")):
        return config.get(bstack1l1ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪኘ"))
    if config.get(bstack1l1ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬኙ")):
        return config.get(bstack1l1ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ኚ"))
def bstack1ll11ll111_opy_(config, bstack11l11ll1l1_opy_):
    proxy = bstack1l11111l_opy_(config)
    proxies = {}
    if config.get(bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ኛ")) or config.get(bstack1l1ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨኜ")):
        if proxy.endswith(bstack1l1ll1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪኝ")):
            proxies = bstack11111l11l_opy_(proxy, bstack11l11ll1l1_opy_)
        else:
            proxies = {
                bstack1l1ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬኞ"): proxy
            }
    return proxies
def bstack11111l11l_opy_(bstack11l11ll1ll_opy_, bstack11l11ll1l1_opy_):
    proxies = {}
    global bstack11l1l11111_opy_
    if bstack1l1ll1l_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪኟ") in globals():
        return bstack11l1l11111_opy_
    try:
        proxy = bstack11l11llll1_opy_(bstack11l11ll1ll_opy_, bstack11l11ll1l1_opy_)
        if bstack1l1ll1l_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣአ") in proxy:
            proxies = {}
        elif bstack1l1ll1l_opy_ (u"ࠤࡋࡘ࡙ࡖࠢኡ") in proxy or bstack1l1ll1l_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤኢ") in proxy or bstack1l1ll1l_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥኣ") in proxy:
            bstack11l11lll1l_opy_ = proxy.split(bstack1l1ll1l_opy_ (u"ࠧࠦࠢኤ"))
            if bstack1l1ll1l_opy_ (u"ࠨ࠺࠰࠱ࠥእ") in bstack1l1ll1l_opy_ (u"ࠢࠣኦ").join(bstack11l11lll1l_opy_[1:]):
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧኧ"): bstack1l1ll1l_opy_ (u"ࠤࠥከ").join(bstack11l11lll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩኩ"): str(bstack11l11lll1l_opy_[0]).lower() + bstack1l1ll1l_opy_ (u"ࠦ࠿࠵࠯ࠣኪ") + bstack1l1ll1l_opy_ (u"ࠧࠨካ").join(bstack11l11lll1l_opy_[1:])
                }
        elif bstack1l1ll1l_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧኬ") in proxy:
            bstack11l11lll1l_opy_ = proxy.split(bstack1l1ll1l_opy_ (u"ࠢࠡࠤክ"))
            if bstack1l1ll1l_opy_ (u"ࠣ࠼࠲࠳ࠧኮ") in bstack1l1ll1l_opy_ (u"ࠤࠥኯ").join(bstack11l11lll1l_opy_[1:]):
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩኰ"): bstack1l1ll1l_opy_ (u"ࠦࠧ኱").join(bstack11l11lll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫኲ"): bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢኳ") + bstack1l1ll1l_opy_ (u"ࠢࠣኴ").join(bstack11l11lll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧኵ"): proxy
            }
    except Exception as e:
        print(bstack1l1ll1l_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨ኶"), bstack11ll1l1lll_opy_.format(bstack11l11ll1ll_opy_, str(e)))
    bstack11l1l11111_opy_ = proxies
    return proxies