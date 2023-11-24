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
class bstack11l1111111_opy_:
    def __init__(self, handler):
        self._111lllll1l_opy_ = None
        self.handler = handler
        self._111lllllll_opy_ = self.bstack111lllll11_opy_()
        self.patch()
    def patch(self):
        self._111lllll1l_opy_ = self._111lllllll_opy_.execute
        self._111lllllll_opy_.execute = self.bstack111llllll1_opy_()
    def bstack111llllll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._111lllll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._111lllllll_opy_.execute = self._111lllll1l_opy_
    @staticmethod
    def bstack111lllll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver