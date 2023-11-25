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
import threading
bstack11l1l1l1l1_opy_ = 1000
bstack11l1l111l1_opy_ = 5
bstack11l1l11111_opy_ = 30
bstack11l1l1l11l_opy_ = 2
class bstack11l1l11ll1_opy_:
    def __init__(self, handler, bstack11l1l1l111_opy_=bstack11l1l1l1l1_opy_, bstack11l1l11l11_opy_=bstack11l1l111l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11l1l1l111_opy_ = bstack11l1l1l111_opy_
        self.bstack11l1l11l11_opy_ = bstack11l1l11l11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack11l1l11l1l_opy_()
    def bstack11l1l11l1l_opy_(self):
        self.timer = threading.Timer(self.bstack11l1l11l11_opy_, self.bstack11l1l1111l_opy_)
        self.timer.start()
    def bstack11l1l11lll_opy_(self):
        self.timer.cancel()
    def bstack11l1l111ll_opy_(self):
        self.bstack11l1l11lll_opy_()
        self.bstack11l1l11l1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11l1l1l111_opy_:
                t = threading.Thread(target=self.bstack11l1l1111l_opy_)
                t.start()
                self.bstack11l1l111ll_opy_()
    def bstack11l1l1111l_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack11l1l1l111_opy_]
        del self.queue[:self.bstack11l1l1l111_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack11l1l11lll_opy_()
        while len(self.queue) > 0:
            self.bstack11l1l1111l_opy_()