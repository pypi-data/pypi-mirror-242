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
class bstack11l11lll11_opy_:
    def __init__(self, handler):
        self._11l11llll1_opy_ = None
        self.handler = handler
        self._11l11ll1l1_opy_ = self.bstack11l11lll1l_opy_()
        self.patch()
    def patch(self):
        self._11l11llll1_opy_ = self._11l11ll1l1_opy_.execute
        self._11l11ll1l1_opy_.execute = self.bstack11l11ll11l_opy_()
    def bstack11l11ll11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._11l11llll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._11l11ll1l1_opy_.execute = self._11l11llll1_opy_
    @staticmethod
    def bstack11l11lll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver