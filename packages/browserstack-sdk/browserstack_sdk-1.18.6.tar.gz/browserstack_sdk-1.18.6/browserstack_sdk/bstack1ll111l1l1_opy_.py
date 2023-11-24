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
import threading
class bstack11l1l1l1_opy_(threading.Thread):
    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
    def join(self, timeout=None):
        super(bstack11l1l1l1_opy_, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret