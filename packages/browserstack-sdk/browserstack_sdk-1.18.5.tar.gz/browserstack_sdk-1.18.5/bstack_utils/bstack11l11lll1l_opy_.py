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
class bstack11l11ll1l1_opy_:
    def __init__(self, handler):
        self._11l11llll1_opy_ = None
        self.handler = handler
        self._11l11ll11l_opy_ = self.bstack11l11ll1ll_opy_()
        self.patch()
    def patch(self):
        self._11l11llll1_opy_ = self._11l11ll11l_opy_.execute
        self._11l11ll11l_opy_.execute = self.bstack11l11lll11_opy_()
    def bstack11l11lll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._11l11llll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._11l11ll11l_opy_.execute = self._11l11llll1_opy_
    @staticmethod
    def bstack11l11ll1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver