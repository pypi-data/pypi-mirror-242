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
import os
from uuid import uuid4
from bstack_utils.helper import bstack11l1l1111_opy_, bstack1l11l1ll11_opy_
from bstack_utils.bstack11lll11ll_opy_ import bstack11l1l1lll1_opy_
class bstack11l111llll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11l11l11l1_opy_=None, framework=None, tags=[], scope=[], bstack11l11l111l_opy_=None, bstack111llllll1_opy_=True, bstack11l1111111_opy_=None, bstack111ll111_opy_=None, result=None, duration=None, meta={}):
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111llllll1_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11l11l11l1_opy_ = bstack11l11l11l1_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11l11l111l_opy_ = bstack11l11l111l_opy_
        self.bstack11l1111111_opy_ = bstack11l1111111_opy_
        self.bstack111ll111_opy_ = bstack111ll111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11l1111l11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l11111ll_opy_(self):
        bstack11l111111l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11lll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩኳ"): bstack11l111111l_opy_,
            bstack11lll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩኴ"): bstack11l111111l_opy_,
            bstack11lll1l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ኵ"): bstack11l111111l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11lll1l_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ኶") + key)
            setattr(self, key, val)
    def bstack11l11l1111_opy_(self):
        return {
            bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ኷"): self.name,
            bstack11lll1l_opy_ (u"ࠫࡧࡵࡤࡺࠩኸ"): {
                bstack11lll1l_opy_ (u"ࠬࡲࡡ࡯ࡩࠪኹ"): bstack11lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ኺ"),
                bstack11lll1l_opy_ (u"ࠧࡤࡱࡧࡩࠬኻ"): self.code
            },
            bstack11lll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨኼ"): self.scope,
            bstack11lll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧኽ"): self.tags,
            bstack11lll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ኾ"): self.framework,
            bstack11lll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ኿"): self.bstack11l11l11l1_opy_
        }
    def bstack11l111l11l_opy_(self):
        return {
         bstack11lll1l_opy_ (u"ࠬࡳࡥࡵࡣࠪዀ"): self.meta
        }
    def bstack11l111l1ll_opy_(self):
        return {
            bstack11lll1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ዁"): {
                bstack11lll1l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫዂ"): self.bstack11l11l111l_opy_
            }
        }
    def bstack11l111ll11_opy_(self, bstack11l1111ll1_opy_, details):
        step = next(filter(lambda st: st[bstack11lll1l_opy_ (u"ࠨ࡫ࡧࠫዃ")] == bstack11l1111ll1_opy_, self.meta[bstack11lll1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨዄ")]), None)
        step.update(details)
    def bstack11l1111l1l_opy_(self, bstack11l1111ll1_opy_):
        step = next(filter(lambda st: st[bstack11lll1l_opy_ (u"ࠪ࡭ࡩ࠭ዅ")] == bstack11l1111ll1_opy_, self.meta[bstack11lll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ዆")]), None)
        step.update({
            bstack11lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ዇"): bstack11l1l1111_opy_()
        })
    def bstack11l111lll1_opy_(self, bstack11l1111ll1_opy_, result):
        bstack11l1111111_opy_ = bstack11l1l1111_opy_()
        step = next(filter(lambda st: st[bstack11lll1l_opy_ (u"࠭ࡩࡥࠩወ")] == bstack11l1111ll1_opy_, self.meta[bstack11lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ዉ")]), None)
        step.update({
            bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ዊ"): bstack11l1111111_opy_,
            bstack11lll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫዋ"): bstack1l11l1ll11_opy_(step[bstack11lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧዌ")], bstack11l1111111_opy_),
            bstack11lll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫው"): result.result,
            bstack11lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ዎ"): str(result.exception) if result.exception else None
        })
    def bstack11l11111l1_opy_(self):
        return {
            bstack11lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫዏ"): self.bstack11l1111l11_opy_(),
            **self.bstack11l11l1111_opy_(),
            **self.bstack11l11111ll_opy_(),
            **self.bstack11l111l11l_opy_()
        }
    def bstack111lllll11_opy_(self):
        data = {
            bstack11lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬዐ"): self.bstack11l1111111_opy_,
            bstack11lll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩዑ"): self.duration,
            bstack11lll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩዒ"): self.result.result
        }
        if data[bstack11lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪዓ")] == bstack11lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫዔ"):
            data[bstack11lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫዕ")] = self.result.bstack1l111l1ll1_opy_()
            data[bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧዖ")] = [{bstack11lll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ዗"): self.result.bstack1l1111l1l1_opy_()}]
        return data
    def bstack11l11l11ll_opy_(self):
        return {
            bstack11lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ዘ"): self.bstack11l1111l11_opy_(),
            **self.bstack11l11l1111_opy_(),
            **self.bstack11l11111ll_opy_(),
            **self.bstack111lllll11_opy_(),
            **self.bstack11l111l11l_opy_()
        }
    def bstack11l111l111_opy_(self, event, result=None):
        if result:
            self.result = result
        if event == bstack11lll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪዙ"):
            return self.bstack11l11111l1_opy_()
        elif event == bstack11lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬዚ"):
            return self.bstack11l11l11ll_opy_()
    def bstack111lllllll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11l1111111_opy_ = time if time else bstack11l1l1111_opy_()
        self.duration = duration if duration else bstack1l11l1ll11_opy_(self.bstack11l11l11l1_opy_, self.bstack11l1111111_opy_)
        if result:
            self.result = result
class bstack11l111ll1l_opy_(bstack11l111llll_opy_):
    def __init__(self, *args, hooks=[], **kwargs):
        self.hooks = hooks
        super().__init__(*args, **kwargs, bstack111ll111_opy_=bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩዛ"))
    @classmethod
    def bstack11l111l1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lll1l_opy_ (u"ࠬ࡯ࡤࠨዜ"): id(step),
                bstack11lll1l_opy_ (u"࠭ࡴࡦࡺࡷࠫዝ"): step.name,
                bstack11lll1l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨዞ"): step.keyword,
            })
        return bstack11l111ll1l_opy_(
            **kwargs,
            meta={
                bstack11lll1l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩዟ"): {
                    bstack11lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧዠ"): feature.name,
                    bstack11lll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨዡ"): feature.filename,
                    bstack11lll1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩዢ"): feature.description
                },
                bstack11lll1l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧዣ"): {
                    bstack11lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫዤ"): scenario.name
                },
                bstack11lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ዥ"): steps,
                bstack11lll1l_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪዦ"): bstack11l1l1lll1_opy_(test)
            }
        )
    def bstack11l1111lll_opy_(self):
        return {
            bstack11lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨዧ"): self.hooks
        }
    def bstack11l11l11ll_opy_(self):
        return {
            **super().bstack11l11l11ll_opy_(),
            **self.bstack11l1111lll_opy_()
        }
    def bstack111lllllll_opy_(self):
        return bstack11lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬየ")