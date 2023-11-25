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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11llllllll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1l11111l11_opy_:
    def __init__(self, handler):
        self._11lllll1ll_opy_ = {}
        self._1l111111ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11lllll1ll_opy_[bstack11lll1l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᅭ")] = Module._inject_setup_function_fixture
        self._11lllll1ll_opy_[bstack11lll1l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᅮ")] = Module._inject_setup_module_fixture
        self._11lllll1ll_opy_[bstack11lll1l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᅯ")] = Class._inject_setup_class_fixture
        self._11lllll1ll_opy_[bstack11lll1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᅰ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11llllll11_opy_(bstack11lll1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᅱ"))
        Module._inject_setup_module_fixture = self.bstack11llllll11_opy_(bstack11lll1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᅲ"))
        Class._inject_setup_class_fixture = self.bstack11llllll11_opy_(bstack11lll1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᅳ"))
        Class._inject_setup_method_fixture = self.bstack11llllll11_opy_(bstack11lll1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᅴ"))
    def bstack1l1111111l_opy_(self, bstack1l1111l11l_opy_, hook_type):
        meth = getattr(bstack1l1111l11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1l111111ll_opy_[hook_type] = meth
            setattr(bstack1l1111l11l_opy_, hook_type, self.bstack11lllllll1_opy_(hook_type))
    def bstack11llllll1l_opy_(self, instance, bstack1l111111l1_opy_):
        if bstack1l111111l1_opy_ == bstack11lll1l_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᅵ"):
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᅶ"))
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᅷ"))
        if bstack1l111111l1_opy_ == bstack11lll1l_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᅸ"):
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᅹ"))
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᅺ"))
        if bstack1l111111l1_opy_ == bstack11lll1l_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᅻ"):
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᅼ"))
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᅽ"))
        if bstack1l111111l1_opy_ == bstack11lll1l_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᅾ"):
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᅿ"))
            self.bstack1l1111111l_opy_(instance.obj, bstack11lll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᆀ"))
    @staticmethod
    def bstack1l1111l111_opy_(hook_type, func, args):
        if hook_type in [bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᆁ"), bstack11lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᆂ")]:
            _11llllllll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11lllllll1_opy_(self, hook_type):
        def bstack1l11111l1l_opy_(arg=None):
            self.handler(hook_type, bstack11lll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᆃ"))
            result = None
            exception = None
            try:
                self.bstack1l1111l111_opy_(hook_type, self._1l111111ll_opy_[hook_type], (arg,))
                result = Result(result=bstack11lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᆄ"))
            except Exception as e:
                result = Result(result=bstack11lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᆅ"), exception=e)
                self.handler(hook_type, bstack11lll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᆆ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᆇ"), result)
        def bstack1l11111ll1_opy_(this, arg=None):
            self.handler(hook_type, bstack11lll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᆈ"))
            result = None
            exception = None
            try:
                self.bstack1l1111l111_opy_(hook_type, self._1l111111ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11lll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᆉ"))
            except Exception as e:
                result = Result(result=bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᆊ"), exception=e)
                self.handler(hook_type, bstack11lll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᆋ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᆌ"), result)
        if hook_type in [bstack11lll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᆍ"), bstack11lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᆎ")]:
            return bstack1l11111ll1_opy_
        return bstack1l11111l1l_opy_
    def bstack11llllll11_opy_(self, bstack1l111111l1_opy_):
        def bstack1l11111lll_opy_(this, *args, **kwargs):
            self.bstack11llllll1l_opy_(this, bstack1l111111l1_opy_)
            self._11lllll1ll_opy_[bstack1l111111l1_opy_](this, *args, **kwargs)
        return bstack1l11111lll_opy_