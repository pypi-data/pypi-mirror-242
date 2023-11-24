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
import os
from uuid import uuid4
from bstack_utils.helper import bstack111lll1l_opy_, bstack1l1l1l11ll_opy_
from bstack_utils.bstack111ll1l11_opy_ import bstack1l1l11l1l1_opy_
class bstack1l1l1llll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l1l11ll11_opy_=None, framework=None, tags=[], scope=[], bstack1l1l11l111_opy_=None, bstack1l1l1lll1l_opy_=True, bstack1l1l1l11l1_opy_=None, bstack1llll111ll_opy_=None, result=None, duration=None, meta={}):
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1l1l1lll1l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l1l11ll11_opy_ = bstack1l1l11ll11_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1l1l11l111_opy_ = bstack1l1l11l111_opy_
        self.bstack1l1l1l11l1_opy_ = bstack1l1l1l11l1_opy_
        self.bstack1llll111ll_opy_ = bstack1llll111ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l1ll1111l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1l1l1l1l1l_opy_(self):
        bstack1l1l1ll111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1ll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ೵"): bstack1l1l1ll111_opy_,
            bstack1l1ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ೶"): bstack1l1l1ll111_opy_,
            bstack1l1ll1l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭೷"): bstack1l1l1ll111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1ll1l_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ೸") + key)
            setattr(self, key, val)
    def bstack1l1ll111ll_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ೹"): self.name,
            bstack1l1ll1l_opy_ (u"ࠫࡧࡵࡤࡺࠩ೺"): {
                bstack1l1ll1l_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ೻"): bstack1l1ll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭೼"),
                bstack1l1ll1l_opy_ (u"ࠧࡤࡱࡧࡩࠬ೽"): self.code
            },
            bstack1l1ll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ೾"): self.scope,
            bstack1l1ll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ೿"): self.tags,
            bstack1l1ll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഀ"): self.framework,
            bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨഁ"): self.bstack1l1l11ll11_opy_
        }
    def bstack1l1l1ll11l_opy_(self):
        return {
         bstack1l1ll1l_opy_ (u"ࠬࡳࡥࡵࡣࠪം"): self.meta
        }
    def bstack1l1ll11111_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩഃ"): {
                bstack1l1ll1l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫഄ"): self.bstack1l1l11l111_opy_
            }
        }
    def bstack1l1l11l11l_opy_(self, bstack1l1l1l1111_opy_, details):
        step = next(filter(lambda st: st[bstack1l1ll1l_opy_ (u"ࠨ࡫ࡧࠫഅ")] == bstack1l1l1l1111_opy_, self.meta[bstack1l1ll1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨആ")]), None)
        step.update(details)
    def bstack1l1l1l1ll1_opy_(self, bstack1l1l1l1111_opy_):
        step = next(filter(lambda st: st[bstack1l1ll1l_opy_ (u"ࠪ࡭ࡩ࠭ഇ")] == bstack1l1l1l1111_opy_, self.meta[bstack1l1ll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪഈ")]), None)
        step.update({
            bstack1l1ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩഉ"): bstack111lll1l_opy_()
        })
    def bstack1l1l11l1ll_opy_(self, bstack1l1l1l1111_opy_, result):
        bstack1l1l1l11l1_opy_ = bstack111lll1l_opy_()
        step = next(filter(lambda st: st[bstack1l1ll1l_opy_ (u"࠭ࡩࡥࠩഊ")] == bstack1l1l1l1111_opy_, self.meta[bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ഋ")]), None)
        step.update({
            bstack1l1ll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ഌ"): bstack1l1l1l11l1_opy_,
            bstack1l1ll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ഍"): bstack1l1l1l11ll_opy_(step[bstack1l1ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧഎ")], bstack1l1l1l11l1_opy_),
            bstack1l1ll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫഏ"): result.result,
            bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ഐ"): str(result.exception) if result.exception else None
        })
    def bstack1l1l1lll11_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ഑"): self.bstack1l1ll1111l_opy_(),
            **self.bstack1l1ll111ll_opy_(),
            **self.bstack1l1l1l1l1l_opy_(),
            **self.bstack1l1l1ll11l_opy_()
        }
    def bstack1l1l1ll1l1_opy_(self):
        data = {
            bstack1l1ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬഒ"): self.bstack1l1l1l11l1_opy_,
            bstack1l1ll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩഓ"): self.duration,
            bstack1l1ll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩഔ"): self.result.result
        }
        if data[bstack1l1ll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪക")] == bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഖ"):
            data[bstack1l1ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫഗ")] = self.result.bstack1l1l1l111l_opy_()
            data[bstack1l1ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧഘ")] = [{bstack1l1ll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪങ"): self.result.bstack1l1l11llll_opy_()}]
        return data
    def bstack1l1l11ll1l_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ച"): self.bstack1l1ll1111l_opy_(),
            **self.bstack1l1ll111ll_opy_(),
            **self.bstack1l1l1l1l1l_opy_(),
            **self.bstack1l1l1ll1l1_opy_(),
            **self.bstack1l1l1ll11l_opy_()
        }
    def bstack1l1l11lll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if event == bstack1l1ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪഛ"):
            return self.bstack1l1l1lll11_opy_()
        elif event == bstack1l1ll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬജ"):
            return self.bstack1l1l11ll1l_opy_()
    def bstack1l1l1ll1ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1l1l11l1_opy_ = time if time else bstack111lll1l_opy_()
        self.duration = duration if duration else bstack1l1l1l11ll_opy_(self.bstack1l1l11ll11_opy_, self.bstack1l1l1l11l1_opy_)
        if result:
            self.result = result
class bstack1l1l1lllll_opy_(bstack1l1l1llll1_opy_):
    def __init__(self, *args, hooks=[], **kwargs):
        self.hooks = hooks
        super().__init__(*args, **kwargs, bstack1llll111ll_opy_=bstack1l1ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩഝ"))
    @classmethod
    def bstack1l1l1l1lll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1ll1l_opy_ (u"ࠬ࡯ࡤࠨഞ"): id(step),
                bstack1l1ll1l_opy_ (u"࠭ࡴࡦࡺࡷࠫട"): step.name,
                bstack1l1ll1l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨഠ"): step.keyword,
            })
        return bstack1l1l1lllll_opy_(
            **kwargs,
            meta={
                bstack1l1ll1l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩഡ"): {
                    bstack1l1ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧഢ"): feature.name,
                    bstack1l1ll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨണ"): feature.filename,
                    bstack1l1ll1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩത"): feature.description
                },
                bstack1l1ll1l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഥ"): {
                    bstack1l1ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫദ"): scenario.name
                },
                bstack1l1ll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ധ"): steps,
                bstack1l1ll1l_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪന"): bstack1l1l11l1l1_opy_(test)
            }
        )
    def bstack1l1ll111l1_opy_(self):
        return {
            bstack1l1ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨഩ"): self.hooks
        }
    def bstack1l1l11ll1l_opy_(self):
        return {
            **super().bstack1l1l11ll1l_opy_(),
            **self.bstack1l1ll111l1_opy_()
        }
    def bstack1l1l1ll1ll_opy_(self):
        return bstack1l1ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬപ")