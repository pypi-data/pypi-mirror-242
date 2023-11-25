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
import sys
class bstack1l1l111ll1_opy_:
    def __init__(self, handler):
        self._1l1l111lll_opy_ = sys.stdout.write
        self._1l1l11l11l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1l1l11l111_opy_
        sys.stdout.error = self.bstack1l1l111l1l_opy_
    def bstack1l1l11l111_opy_(self, _str):
        self._1l1l111lll_opy_(_str)
        if self.handler:
            self.handler({bstack11lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪඍ"): bstack11lll1l_opy_ (u"ࠬࡏࡎࡇࡑࠪඎ"), bstack11lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧඏ"): _str})
    def bstack1l1l111l1l_opy_(self, _str):
        self._1l1l11l11l_opy_(_str)
        if self.handler:
            self.handler({bstack11lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ඐ"): bstack11lll1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧඑ"), bstack11lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪඒ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1l1l111lll_opy_
        sys.stderr.write = self._1l1l11l11l_opy_