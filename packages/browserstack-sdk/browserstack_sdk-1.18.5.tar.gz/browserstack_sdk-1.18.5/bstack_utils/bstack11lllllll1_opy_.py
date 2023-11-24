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
class bstack1l111111ll_opy_:
    def __init__(self, handler):
        self._1l1111111l_opy_ = {}
        self._11llllll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._1l1111111l_opy_[bstack1111_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᅬ")] = Module._inject_setup_function_fixture
        self._1l1111111l_opy_[bstack1111_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᅭ")] = Module._inject_setup_module_fixture
        self._1l1111111l_opy_[bstack1111_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᅮ")] = Class._inject_setup_class_fixture
        self._1l1111111l_opy_[bstack1111_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᅯ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack1l1111l111_opy_(bstack1111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᅰ"))
        Module._inject_setup_module_fixture = self.bstack1l1111l111_opy_(bstack1111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᅱ"))
        Class._inject_setup_class_fixture = self.bstack1l1111l111_opy_(bstack1111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᅲ"))
        Class._inject_setup_method_fixture = self.bstack1l1111l111_opy_(bstack1111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᅳ"))
    def bstack1l11111ll1_opy_(self, bstack1l11111lll_opy_, hook_type):
        meth = getattr(bstack1l11111lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11llllll11_opy_[hook_type] = meth
            setattr(bstack1l11111lll_opy_, hook_type, self.bstack1l1111l11l_opy_(hook_type))
    def bstack1l11111l11_opy_(self, instance, bstack11llllll1l_opy_):
        if bstack11llllll1l_opy_ == bstack1111_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᅴ"):
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦᅵ"))
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᅶ"))
        if bstack11llllll1l_opy_ == bstack1111_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᅷ"):
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧᅸ"))
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤᅹ"))
        if bstack11llllll1l_opy_ == bstack1111_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᅺ"):
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢᅻ"))
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦᅼ"))
        if bstack11llllll1l_opy_ == bstack1111_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᅽ"):
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦᅾ"))
            self.bstack1l11111ll1_opy_(instance.obj, bstack1111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣᅿ"))
    @staticmethod
    def bstack11lllll1ll_opy_(hook_type, func, args):
        if hook_type in [bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᆀ"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᆁ")]:
            _11llllllll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1l1111l11l_opy_(self, hook_type):
        def bstack1l11111111_opy_(arg=None):
            self.handler(hook_type, bstack1111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᆂ"))
            result = None
            exception = None
            try:
                self.bstack11lllll1ll_opy_(hook_type, self._11llllll11_opy_[hook_type], (arg,))
                result = Result(result=bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᆃ"))
            except Exception as e:
                result = Result(result=bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᆄ"), exception=e)
                self.handler(hook_type, bstack1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᆅ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᆆ"), result)
        def bstack1l111111l1_opy_(this, arg=None):
            self.handler(hook_type, bstack1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᆇ"))
            result = None
            exception = None
            try:
                self.bstack11lllll1ll_opy_(hook_type, self._11llllll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᆈ"))
            except Exception as e:
                result = Result(result=bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᆉ"), exception=e)
                self.handler(hook_type, bstack1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᆊ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᆋ"), result)
        if hook_type in [bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᆌ"), bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᆍ")]:
            return bstack1l111111l1_opy_
        return bstack1l11111111_opy_
    def bstack1l1111l111_opy_(self, bstack11llllll1l_opy_):
        def bstack1l11111l1l_opy_(this, *args, **kwargs):
            self.bstack1l11111l11_opy_(this, bstack11llllll1l_opy_)
            self._1l1111111l_opy_[bstack11llllll1l_opy_](this, *args, **kwargs)
        return bstack1l11111l1l_opy_