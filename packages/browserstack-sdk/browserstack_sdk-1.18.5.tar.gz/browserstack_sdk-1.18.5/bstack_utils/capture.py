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
import sys
class bstack1l1l111l1l_opy_:
    def __init__(self, handler):
        self._1l1l11l111_opy_ = sys.stdout.write
        self._1l1l111ll1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1l1l111lll_opy_
        sys.stdout.error = self.bstack1l1l11l11l_opy_
    def bstack1l1l111lll_opy_(self, _str):
        self._1l1l11l111_opy_(_str)
        if self.handler:
            self.handler({bstack1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩඌ"): bstack1111_opy_ (u"ࠫࡎࡔࡆࡐࠩඍ"), bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ඎ"): _str})
    def bstack1l1l11l11l_opy_(self, _str):
        self._1l1l111ll1_opy_(_str)
        if self.handler:
            self.handler({bstack1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬඏ"): bstack1111_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ඐ"), bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඑ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1l1l11l111_opy_
        sys.stderr.write = self._1l1l111ll1_opy_