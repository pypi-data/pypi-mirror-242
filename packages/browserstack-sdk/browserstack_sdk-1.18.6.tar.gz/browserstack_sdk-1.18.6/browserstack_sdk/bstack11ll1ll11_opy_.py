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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1ll111l1l1_opy_ import *
from bstack_utils.helper import bstack111lllll_opy_
from bstack_utils.messages import bstack11111l11_opy_
from bstack_utils.constants import bstack1ll111l1l_opy_
class bstack1111ll1l_opy_:
    def __init__(self, args, logger, bstack1l1ll1llll_opy_, bstack1l1ll11ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l1ll1llll_opy_ = bstack1l1ll1llll_opy_
        self.bstack1l1ll11ll1_opy_ = bstack1l1ll11ll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll111l_opy_ = []
        self.bstack1l1ll11lll_opy_ = None
        self.bstack1l1111lll_opy_ = []
        self.bstack1l1ll1ll1l_opy_ = self.bstack1l11l11ll_opy_()
        self.bstack1lll1lll11_opy_ = -1
    def bstack1l1l1111l_opy_(self, bstack1l1ll11l1l_opy_):
        self.parse_args()
        self.bstack1l1ll1l11l_opy_()
        self.bstack1l1lll1111_opy_(bstack1l1ll11l1l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l1ll1ll11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll1lll11_opy_ = -1
        if bstack1l1ll1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫೞ") in self.bstack1l1ll1llll_opy_:
            self.bstack1lll1lll11_opy_ = self.bstack1l1ll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ೟")]
        try:
            bstack1l1ll1lll1_opy_ = [bstack1l1ll1l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨೠ"), bstack1l1ll1l_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪೡ"), bstack1l1ll1l_opy_ (u"ࠨ࠯ࡳࠫೢ")]
            if self.bstack1lll1lll11_opy_ >= 0:
                bstack1l1ll1lll1_opy_.extend([bstack1l1ll1l_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪೣ"), bstack1l1ll1l_opy_ (u"ࠪ࠱ࡳ࠭೤")])
            for arg in bstack1l1ll1lll1_opy_:
                self.bstack1l1ll1ll11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l1ll1l11l_opy_(self):
        bstack1l1ll11lll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l1ll11lll_opy_ = bstack1l1ll11lll_opy_
        return bstack1l1ll11lll_opy_
    def bstack1l1llll1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1l1ll1l111_opy_ = importlib.find_loader(bstack1l1ll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭೥"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11111l11_opy_)
    def bstack1l1lll1111_opy_(self, bstack1l1ll11l1l_opy_):
        if bstack1l1ll11l1l_opy_:
            self.bstack1l1ll11lll_opy_.append(bstack1l1ll1l_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ೦"))
            self.bstack1l1ll11lll_opy_.append(bstack1l1ll1l_opy_ (u"࠭ࡔࡳࡷࡨࠫ೧"))
        self.bstack1l1ll11lll_opy_.append(bstack1l1ll1l_opy_ (u"ࠧ࠮ࡲࠪ೨"))
        self.bstack1l1ll11lll_opy_.append(bstack1l1ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭೩"))
        self.bstack1l1ll11lll_opy_.append(bstack1l1ll1l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫ೪"))
        self.bstack1l1ll11lll_opy_.append(bstack1l1ll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ೫"))
        if self.bstack1lll1lll11_opy_ > 1:
            self.bstack1l1ll11lll_opy_.append(bstack1l1ll1l_opy_ (u"ࠫ࠲ࡴࠧ೬"))
            self.bstack1l1ll11lll_opy_.append(str(self.bstack1lll1lll11_opy_))
    def bstack1l1ll1l1l1_opy_(self):
        bstack1l1111lll_opy_ = []
        for spec in self.bstack1lll111l_opy_:
            bstack1lll111lll_opy_ = [spec]
            bstack1lll111lll_opy_ += self.bstack1l1ll11lll_opy_
            bstack1l1111lll_opy_.append(bstack1lll111lll_opy_)
        self.bstack1l1111lll_opy_ = bstack1l1111lll_opy_
        return bstack1l1111lll_opy_
    def bstack1l11l11ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1l1ll1ll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack1l1ll1ll1l_opy_ = False
        return self.bstack1l1ll1ll1l_opy_
    def bstack11llllll_opy_(self, bstack1l1ll11l11_opy_, bstack1l1l1111l_opy_):
        bstack1l1l1111l_opy_[bstack1l1ll1l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ೭")] = self.bstack1l1ll1llll_opy_
        multiprocessing.set_start_method(bstack1l1ll1l_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬ೮"))
        if bstack1l1ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ೯") in self.bstack1l1ll1llll_opy_:
            bstack1l1l11ll_opy_ = []
            manager = multiprocessing.Manager()
            bstack111l1l1ll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1l1ll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೰")]):
                bstack1l1l11ll_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l1ll11l11_opy_,
                                                           args=(self.bstack1l1ll11lll_opy_, bstack1l1l1111l_opy_, bstack111l1l1ll_opy_)))
            i = 0
            bstack1l1ll1l1ll_opy_ = len(self.bstack1l1ll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೱ")])
            for t in bstack1l1l11ll_opy_:
                os.environ[bstack1l1ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪೲ")] = str(i)
                os.environ[bstack1l1ll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬೳ")] = json.dumps(self.bstack1l1ll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೴")][i % bstack1l1ll1l1ll_opy_])
                i += 1
                t.start()
            for t in bstack1l1l11ll_opy_:
                t.join()
            return list(bstack111l1l1ll_opy_)