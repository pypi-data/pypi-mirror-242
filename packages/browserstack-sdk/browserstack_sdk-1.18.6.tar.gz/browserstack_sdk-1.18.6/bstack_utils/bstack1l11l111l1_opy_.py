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
bstack11l111l11l_opy_ = 1000
bstack11l111l1l1_opy_ = 5
bstack11l1111lll_opy_ = 30
bstack11l11111l1_opy_ = 2
class bstack1l11l11l11_opy_:
    def __init__(self, handler, bstack11l111l1ll_opy_=bstack11l111l11l_opy_, bstack11l1111l11_opy_=bstack11l111l1l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11l111l1ll_opy_ = bstack11l111l1ll_opy_
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack11l1111ll1_opy_()
    def bstack11l1111ll1_opy_(self):
        self.timer = threading.Timer(self.bstack11l1111l11_opy_, self.bstack11l1111l1l_opy_)
        self.timer.start()
    def bstack11l111l111_opy_(self):
        self.timer.cancel()
    def bstack11l11111ll_opy_(self):
        self.bstack11l111l111_opy_()
        self.bstack11l1111ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11l111l1ll_opy_:
                t = threading.Thread(target=self.bstack11l1111l1l_opy_)
                t.start()
                self.bstack11l11111ll_opy_()
    def bstack11l1111l1l_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack11l111l1ll_opy_]
        del self.queue[:self.bstack11l111l1ll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack11l111l111_opy_()
        while len(self.queue) > 0:
            self.bstack11l1111l1l_opy_()