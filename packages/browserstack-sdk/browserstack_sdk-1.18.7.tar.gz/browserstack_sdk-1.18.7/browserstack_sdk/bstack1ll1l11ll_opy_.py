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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1llll1111_opy_ import *
from bstack_utils.helper import bstack1lll1l1l1l_opy_
from bstack_utils.messages import bstack1l1l11l1l_opy_
from bstack_utils.constants import bstack1l1l11111_opy_
class bstack1111111l_opy_:
    def __init__(self, args, logger, bstack1l1ll11l1l_opy_, bstack1l1ll11l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l1ll11l1l_opy_ = bstack1l1ll11l1l_opy_
        self.bstack1l1ll11l11_opy_ = bstack1l1ll11l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1l111l_opy_ = []
        self.bstack1l1ll1ll1l_opy_ = None
        self.bstack111111111_opy_ = []
        self.bstack1l1ll1l1ll_opy_ = self.bstack1111l11l_opy_()
        self.bstack11111ll11_opy_ = -1
    def bstack1llll1l1ll_opy_(self, bstack1l1ll11lll_opy_):
        self.parse_args()
        self.bstack1l1lll1111_opy_()
        self.bstack1l1ll11ll1_opy_(bstack1l1ll11lll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l1ll1l1l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11111ll11_opy_ = -1
        if bstack11lll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ೟") in self.bstack1l1ll11l1l_opy_:
            self.bstack11111ll11_opy_ = self.bstack1l1ll11l1l_opy_[bstack11lll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ೠ")]
        try:
            bstack1l1ll1ll11_opy_ = [bstack11lll1l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩೡ"), bstack11lll1l_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫೢ"), bstack11lll1l_opy_ (u"ࠩ࠰ࡴࠬೣ")]
            if self.bstack11111ll11_opy_ >= 0:
                bstack1l1ll1ll11_opy_.extend([bstack11lll1l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ೤"), bstack11lll1l_opy_ (u"ࠫ࠲ࡴࠧ೥")])
            for arg in bstack1l1ll1ll11_opy_:
                self.bstack1l1ll1l1l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l1lll1111_opy_(self):
        bstack1l1ll1ll1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l1ll1ll1l_opy_ = bstack1l1ll1ll1l_opy_
        return bstack1l1ll1ll1l_opy_
    def bstack1lll111l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1l1ll1lll1_opy_ = importlib.find_loader(bstack11lll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ೦"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l11l1l_opy_)
    def bstack1l1ll11ll1_opy_(self, bstack1l1ll11lll_opy_):
        if bstack1l1ll11lll_opy_:
            self.bstack1l1ll1ll1l_opy_.append(bstack11lll1l_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ೧"))
            self.bstack1l1ll1ll1l_opy_.append(bstack11lll1l_opy_ (u"ࠧࡕࡴࡸࡩࠬ೨"))
        self.bstack1l1ll1ll1l_opy_.append(bstack11lll1l_opy_ (u"ࠨ࠯ࡳࠫ೩"))
        self.bstack1l1ll1ll1l_opy_.append(bstack11lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧ೪"))
        self.bstack1l1ll1ll1l_opy_.append(bstack11lll1l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ೫"))
        self.bstack1l1ll1ll1l_opy_.append(bstack11lll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ೬"))
        if self.bstack11111ll11_opy_ > 1:
            self.bstack1l1ll1ll1l_opy_.append(bstack11lll1l_opy_ (u"ࠬ࠳࡮ࠨ೭"))
            self.bstack1l1ll1ll1l_opy_.append(str(self.bstack11111ll11_opy_))
    def bstack1l1ll1l11l_opy_(self):
        bstack111111111_opy_ = []
        for spec in self.bstack1ll1l111l_opy_:
            bstack1lllll1l1_opy_ = [spec]
            bstack1lllll1l1_opy_ += self.bstack1l1ll1ll1l_opy_
            bstack111111111_opy_.append(bstack1lllll1l1_opy_)
        self.bstack111111111_opy_ = bstack111111111_opy_
        return bstack111111111_opy_
    def bstack1111l11l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1l1ll1l1ll_opy_ = True
            return True
        except Exception as e:
            self.bstack1l1ll1l1ll_opy_ = False
        return self.bstack1l1ll1l1ll_opy_
    def bstack1ll111ll1_opy_(self, bstack1l1ll1llll_opy_, bstack1llll1l1ll_opy_):
        bstack1llll1l1ll_opy_[bstack11lll1l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭೮")] = self.bstack1l1ll11l1l_opy_
        multiprocessing.set_start_method(bstack11lll1l_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭೯"))
        if bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೰") in self.bstack1l1ll11l1l_opy_:
            bstack1lll111ll1_opy_ = []
            manager = multiprocessing.Manager()
            bstack1ll11l1l1l_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1l1ll11l1l_opy_[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೱ")]):
                bstack1lll111ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l1ll1llll_opy_,
                                                           args=(self.bstack1l1ll1ll1l_opy_, bstack1llll1l1ll_opy_, bstack1ll11l1l1l_opy_)))
            i = 0
            bstack1l1ll1l111_opy_ = len(self.bstack1l1ll11l1l_opy_[bstack11lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ೲ")])
            for t in bstack1lll111ll1_opy_:
                os.environ[bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫೳ")] = str(i)
                os.environ[bstack11lll1l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭೴")] = json.dumps(self.bstack1l1ll11l1l_opy_[bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ೵")][i % bstack1l1ll1l111_opy_])
                i += 1
                t.start()
            for t in bstack1lll111ll1_opy_:
                t.join()
            return list(bstack1ll11l1l1l_opy_)