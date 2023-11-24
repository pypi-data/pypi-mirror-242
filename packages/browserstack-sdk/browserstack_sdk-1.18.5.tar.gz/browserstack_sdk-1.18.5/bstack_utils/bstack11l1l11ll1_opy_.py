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
import threading
bstack11l1l1111l_opy_ = 1000
bstack11l1l1l111_opy_ = 5
bstack11l1l11l1l_opy_ = 30
bstack11l1l111ll_opy_ = 2
class bstack11l1l1l11l_opy_:
    def __init__(self, handler, bstack11l1l11111_opy_=bstack11l1l1111l_opy_, bstack11l1l11l11_opy_=bstack11l1l1l111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
        self.bstack11l1l11l11_opy_ = bstack11l1l11l11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack11l1l11lll_opy_()
    def bstack11l1l11lll_opy_(self):
        self.timer = threading.Timer(self.bstack11l1l11l11_opy_, self.bstack11l1l111l1_opy_)
        self.timer.start()
    def bstack11l11lllll_opy_(self):
        self.timer.cancel()
    def bstack11l1l1l1l1_opy_(self):
        self.bstack11l11lllll_opy_()
        self.bstack11l1l11lll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11l1l11111_opy_:
                t = threading.Thread(target=self.bstack11l1l111l1_opy_)
                t.start()
                self.bstack11l1l1l1l1_opy_()
    def bstack11l1l111l1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack11l1l11111_opy_]
        del self.queue[:self.bstack11l1l11111_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack11l11lllll_opy_()
        while len(self.queue) > 0:
            self.bstack11l1l111l1_opy_()