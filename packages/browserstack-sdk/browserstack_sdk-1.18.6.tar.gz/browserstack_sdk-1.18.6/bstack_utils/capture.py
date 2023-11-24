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
import sys
class bstack111ll11111_opy_:
    def __init__(self, handler):
        self._111ll111l1_opy_ = sys.stdout.write
        self._111ll111ll_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack111ll11l11_opy_
        sys.stdout.error = self.bstack111ll1111l_opy_
    def bstack111ll11l11_opy_(self, _str):
        self._111ll111l1_opy_(_str)
        if self.handler:
            self.handler({bstack1l1ll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ꭹ"): bstack1l1ll1l_opy_ (u"ࠨࡋࡑࡊࡔ࠭Ꭺ"), bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᎫ"): _str})
    def bstack111ll1111l_opy_(self, _str):
        self._111ll111ll_opy_(_str)
        if self.handler:
            self.handler({bstack1l1ll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᎬ"): bstack1l1ll1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪᎭ"), bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ꭾ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._111ll111l1_opy_
        sys.stderr.write = self._111ll111ll_opy_