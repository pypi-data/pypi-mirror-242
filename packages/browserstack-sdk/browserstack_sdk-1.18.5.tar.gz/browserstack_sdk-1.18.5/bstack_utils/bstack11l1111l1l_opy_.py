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
import os
from uuid import uuid4
from bstack_utils.helper import bstack1111111l1_opy_, bstack1l11lll1ll_opy_
from bstack_utils.bstack1l1llllll1_opy_ import bstack11l1ll1111_opy_
class bstack11l11l111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11l11l11l1_opy_=None, framework=None, tags=[], scope=[], bstack11l11111l1_opy_=None, bstack11l111ll11_opy_=True, bstack111lllllll_opy_=None, bstack1ll1l1111l_opy_=None, result=None, duration=None, meta={}):
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11l111ll11_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11l11l11l1_opy_ = bstack11l11l11l1_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11l11111l1_opy_ = bstack11l11111l1_opy_
        self.bstack111lllllll_opy_ = bstack111lllllll_opy_
        self.bstack1ll1l1111l_opy_ = bstack1ll1l1111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11l111l111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l111ll1l_opy_(self):
        bstack11l111l1l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨኲ"): bstack11l111l1l1_opy_,
            bstack1111_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨኳ"): bstack11l111l1l1_opy_,
            bstack1111_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬኴ"): bstack11l111l1l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1111_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤኵ") + key)
            setattr(self, key, val)
    def bstack11l11l1111_opy_(self):
        return {
            bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ኶"): self.name,
            bstack1111_opy_ (u"ࠪࡦࡴࡪࡹࠨ኷"): {
                bstack1111_opy_ (u"ࠫࡱࡧ࡮ࡨࠩኸ"): bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬኹ"),
                bstack1111_opy_ (u"࠭ࡣࡰࡦࡨࠫኺ"): self.code
            },
            bstack1111_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧኻ"): self.scope,
            bstack1111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ኼ"): self.tags,
            bstack1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬኽ"): self.framework,
            bstack1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧኾ"): self.bstack11l11l11l1_opy_
        }
    def bstack11l11l11ll_opy_(self):
        return {
         bstack1111_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ኿"): self.meta
        }
    def bstack11l111l1ll_opy_(self):
        return {
            bstack1111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨዀ"): {
                bstack1111_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ዁"): self.bstack11l11111l1_opy_
            }
        }
    def bstack11l111l11l_opy_(self, bstack11l1111lll_opy_, details):
        step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠧࡪࡦࠪዂ")] == bstack11l1111lll_opy_, self.meta[bstack1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧዃ")]), None)
        step.update(details)
    def bstack111lllll11_opy_(self, bstack11l1111lll_opy_):
        step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠩ࡬ࡨࠬዄ")] == bstack11l1111lll_opy_, self.meta[bstack1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩዅ")]), None)
        step.update({
            bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ዆"): bstack1111111l1_opy_()
        })
    def bstack11l1111111_opy_(self, bstack11l1111lll_opy_, result):
        bstack111lllllll_opy_ = bstack1111111l1_opy_()
        step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠬ࡯ࡤࠨ዇")] == bstack11l1111lll_opy_, self.meta[bstack1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬወ")]), None)
        step.update({
            bstack1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬዉ"): bstack111lllllll_opy_,
            bstack1111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪዊ"): bstack1l11lll1ll_opy_(step[bstack1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ዋ")], bstack111lllllll_opy_),
            bstack1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪዌ"): result.result,
            bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬው"): str(result.exception) if result.exception else None
        })
    def bstack111llllll1_opy_(self):
        return {
            bstack1111_opy_ (u"ࠬࡻࡵࡪࡦࠪዎ"): self.bstack11l111l111_opy_(),
            **self.bstack11l11l1111_opy_(),
            **self.bstack11l111ll1l_opy_(),
            **self.bstack11l11l11ll_opy_()
        }
    def bstack11l1111ll1_opy_(self):
        data = {
            bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫዏ"): self.bstack111lllllll_opy_,
            bstack1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨዐ"): self.duration,
            bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨዑ"): self.result.result
        }
        if data[bstack1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩዒ")] == bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዓ"):
            data[bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪዔ")] = self.result.bstack1l11lll11l_opy_()
            data[bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ዕ")] = [{bstack1111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩዖ"): self.result.bstack1l11ll111l_opy_()}]
        return data
    def bstack111lllll1l_opy_(self):
        return {
            bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ዗"): self.bstack11l111l111_opy_(),
            **self.bstack11l11l1111_opy_(),
            **self.bstack11l111ll1l_opy_(),
            **self.bstack11l1111ll1_opy_(),
            **self.bstack11l11l11ll_opy_()
        }
    def bstack11l1111l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if event == bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩዘ"):
            return self.bstack111llllll1_opy_()
        elif event == bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫዙ"):
            return self.bstack111lllll1l_opy_()
    def bstack11l11111ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack111lllllll_opy_ = time if time else bstack1111111l1_opy_()
        self.duration = duration if duration else bstack1l11lll1ll_opy_(self.bstack11l11l11l1_opy_, self.bstack111lllllll_opy_)
        if result:
            self.result = result
class bstack11l111llll_opy_(bstack11l11l111l_opy_):
    def __init__(self, *args, hooks=[], **kwargs):
        self.hooks = hooks
        super().__init__(*args, **kwargs, bstack1ll1l1111l_opy_=bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࠨዚ"))
    @classmethod
    def bstack11l111lll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111_opy_ (u"ࠫ࡮ࡪࠧዛ"): id(step),
                bstack1111_opy_ (u"ࠬࡺࡥࡹࡶࠪዜ"): step.name,
                bstack1111_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧዝ"): step.keyword,
            })
        return bstack11l111llll_opy_(
            **kwargs,
            meta={
                bstack1111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨዞ"): {
                    bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ዟ"): feature.name,
                    bstack1111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧዠ"): feature.filename,
                    bstack1111_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨዡ"): feature.description
                },
                bstack1111_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ዢ"): {
                    bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪዣ"): scenario.name
                },
                bstack1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬዤ"): steps,
                bstack1111_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩዥ"): bstack11l1ll1111_opy_(test)
            }
        )
    def bstack11l111111l_opy_(self):
        return {
            bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧዦ"): self.hooks
        }
    def bstack111lllll1l_opy_(self):
        return {
            **super().bstack111lllll1l_opy_(),
            **self.bstack11l111111l_opy_()
        }
    def bstack11l11111ll_opy_(self):
        return bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫዧ")