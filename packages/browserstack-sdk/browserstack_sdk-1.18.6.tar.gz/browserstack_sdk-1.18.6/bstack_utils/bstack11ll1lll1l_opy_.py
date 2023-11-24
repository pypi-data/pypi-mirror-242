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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11lll1l111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11lll11ll1_opy_:
    def __init__(self, handler):
        self._11lll11lll_opy_ = {}
        self._11ll1lll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11lll11lll_opy_[bstack1l1ll1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᇌ")] = Module._inject_setup_function_fixture
        self._11lll11lll_opy_[bstack1l1ll1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᇍ")] = Module._inject_setup_module_fixture
        self._11lll11lll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᇎ")] = Class._inject_setup_class_fixture
        self._11lll11lll_opy_[bstack1l1ll1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᇏ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11lll111l1_opy_(bstack1l1ll1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᇐ"))
        Module._inject_setup_module_fixture = self.bstack11lll111l1_opy_(bstack1l1ll1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᇑ"))
        Class._inject_setup_class_fixture = self.bstack11lll111l1_opy_(bstack1l1ll1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᇒ"))
        Class._inject_setup_method_fixture = self.bstack11lll111l1_opy_(bstack1l1ll1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᇓ"))
    def bstack11ll1ll1ll_opy_(self, bstack11ll1lllll_opy_, hook_type):
        meth = getattr(bstack11ll1lllll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11ll1lll11_opy_[hook_type] = meth
            setattr(bstack11ll1lllll_opy_, hook_type, self.bstack11lll111ll_opy_(hook_type))
    def bstack11lll11l1l_opy_(self, instance, bstack11lll1111l_opy_):
        if bstack11lll1111l_opy_ == bstack1l1ll1l_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᇔ"):
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᇕ"))
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᇖ"))
        if bstack11lll1111l_opy_ == bstack1l1ll1l_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᇗ"):
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥᇘ"))
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢᇙ"))
        if bstack11lll1111l_opy_ == bstack1l1ll1l_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᇚ"):
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧᇛ"))
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤᇜ"))
        if bstack11lll1111l_opy_ == bstack1l1ll1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᇝ"):
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤᇞ"))
            self.bstack11ll1ll1ll_opy_(instance.obj, bstack1l1ll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨᇟ"))
    @staticmethod
    def bstack11lll11l11_opy_(hook_type, func, args):
        if hook_type in [bstack1l1ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᇠ"), bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᇡ")]:
            _11lll1l111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11lll111ll_opy_(self, hook_type):
        def bstack11lll1l11l_opy_(arg=None):
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᇢ"))
            result = None
            exception = None
            try:
                self.bstack11lll11l11_opy_(hook_type, self._11ll1lll11_opy_[hook_type], (arg,))
                result = Result(result=bstack1l1ll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᇣ"))
            except Exception as e:
                result = Result(result=bstack1l1ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᇤ"), exception=e)
                self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᇥ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᇦ"), result)
        def bstack11lll11111_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᇧ"))
            result = None
            exception = None
            try:
                self.bstack11lll11l11_opy_(hook_type, self._11ll1lll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᇨ"))
            except Exception as e:
                result = Result(result=bstack1l1ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᇩ"), exception=e)
                self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᇪ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1ll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᇫ"), result)
        if hook_type in [bstack1l1ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᇬ"), bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᇭ")]:
            return bstack11lll11111_opy_
        return bstack11lll1l11l_opy_
    def bstack11lll111l1_opy_(self, bstack11lll1111l_opy_):
        def bstack11ll1llll1_opy_(this, *args, **kwargs):
            self.bstack11lll11l1l_opy_(this, bstack11lll1111l_opy_)
            self._11lll11lll_opy_[bstack11lll1111l_opy_](this, *args, **kwargs)
        return bstack11ll1llll1_opy_