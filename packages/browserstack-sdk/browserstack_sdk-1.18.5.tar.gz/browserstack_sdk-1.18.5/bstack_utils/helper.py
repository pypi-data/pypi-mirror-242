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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack1l1l11111l_opy_, bstack1l1111111_opy_, bstack111lll111_opy_, bstack1lll1ll11l_opy_
from bstack_utils.messages import bstack1lllll1lll_opy_, bstack1ll111ll11_opy_
from bstack_utils.proxy import bstack1l1llll11_opy_, bstack111ll1111_opy_
bstack1llll1l1ll_opy_ = Config.get_instance()
def bstack1l1l1l1111_opy_(config):
    return config[bstack1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ࿖")]
def bstack1l1l11lll1_opy_(config):
    return config[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ࿗")]
def bstack1l11llll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1l11l1111l_opy_(obj):
    values = []
    bstack1l111l1111_opy_ = re.compile(bstack1111_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢ࿘"), re.I)
    for key in obj.keys():
        if bstack1l111l1111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l111lllll_opy_(config):
    tags = []
    tags.extend(bstack1l11l1111l_opy_(os.environ))
    tags.extend(bstack1l11l1111l_opy_(config))
    return tags
def bstack1l11l11l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l111lll1l_opy_(bstack1l11ll11l1_opy_):
    if not bstack1l11ll11l1_opy_:
        return bstack1111_opy_ (u"ࠫࠬ࿙")
    return bstack1111_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨ࿚").format(bstack1l11ll11l1_opy_.name, bstack1l11ll11l1_opy_.email)
def bstack1l1l1lll1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1l111lll11_opy_ = repo.common_dir
        info = {
            bstack1111_opy_ (u"ࠨࡳࡩࡣࠥ࿛"): repo.head.commit.hexsha,
            bstack1111_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥ࿜"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣ࿝"): repo.active_branch.name,
            bstack1111_opy_ (u"ࠤࡷࡥ࡬ࠨ࿞"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨ࿟"): bstack1l111lll1l_opy_(repo.head.commit.committer),
            bstack1111_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧ࿠"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧ࿡"): bstack1l111lll1l_opy_(repo.head.commit.author),
            bstack1111_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦ࿢"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ࿣"): repo.head.commit.message,
            bstack1111_opy_ (u"ࠣࡴࡲࡳࡹࠨ࿤"): repo.git.rev_parse(bstack1111_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦ࿥")),
            bstack1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦ࿦"): bstack1l111lll11_opy_,
            bstack1111_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ࿧"): subprocess.check_output([bstack1111_opy_ (u"ࠧ࡭ࡩࡵࠤ࿨"), bstack1111_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤ࿩"), bstack1111_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥ࿪")]).strip().decode(
                bstack1111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ࿫")),
            bstack1111_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦ࿬"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ࿭"): repo.git.rev_list(
                bstack1111_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦ࿮").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1l11l1llll_opy_ = []
        for remote in remotes:
            bstack1l1111ll11_opy_ = {
                bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ࿯"): remote.name,
                bstack1111_opy_ (u"ࠨࡵࡳ࡮ࠥ࿰"): remote.url,
            }
            bstack1l11l1llll_opy_.append(bstack1l1111ll11_opy_)
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ࿱"): bstack1111_opy_ (u"ࠣࡩ࡬ࡸࠧ࿲"),
            **info,
            bstack1111_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥ࿳"): bstack1l11l1llll_opy_
        }
    except Exception as err:
        print(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ࿴").format(err))
        return {}
def bstack1111lll11_opy_():
    env = os.environ
    if (bstack1111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤ࿵") in env and len(env[bstack1111_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ࿶")]) > 0) or (
            bstack1111_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧ࿷") in env and len(env[bstack1111_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ࿸")]) > 0):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨ࿹"): bstack1111_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥ࿺"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ࿻"): env.get(bstack1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ࿼")),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ࿽"): env.get(bstack1111_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣ࿾")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ࿿"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢက"))
        }
    if env.get(bstack1111_opy_ (u"ࠤࡆࡍࠧခ")) == bstack1111_opy_ (u"ࠥࡸࡷࡻࡥࠣဂ") and bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨဃ"))):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥင"): bstack1111_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣစ"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥဆ"): env.get(bstack1111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦဇ")),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦဈ"): env.get(bstack1111_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢဉ")),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥည"): env.get(bstack1111_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣဋ"))
        }
    if env.get(bstack1111_opy_ (u"ࠨࡃࡊࠤဌ")) == bstack1111_opy_ (u"ࠢࡵࡴࡸࡩࠧဍ") and bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣဎ"))):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢဏ"): bstack1111_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨတ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢထ"): env.get(bstack1111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧဒ")),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣဓ"): env.get(bstack1111_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤန")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢပ"): env.get(bstack1111_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣဖ"))
        }
    if env.get(bstack1111_opy_ (u"ࠥࡇࡎࠨဗ")) == bstack1111_opy_ (u"ࠦࡹࡸࡵࡦࠤဘ") and env.get(bstack1111_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨမ")) == bstack1111_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣယ"):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧရ"): bstack1111_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥလ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧဝ"): None,
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧသ"): None,
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥဟ"): None
        }
    if env.get(bstack1111_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣဠ")) and env.get(bstack1111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤအ")):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧဢ"): bstack1111_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦဣ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧဤ"): env.get(bstack1111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣဥ")),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨဦ"): None,
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦဧ"): env.get(bstack1111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣဨ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡄࡋࠥဩ")) == bstack1111_opy_ (u"ࠣࡶࡵࡹࡪࠨဪ") and bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣါ"))):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣာ"): bstack1111_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥိ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣီ"): env.get(bstack1111_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤု")),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤူ"): None,
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢေ"): env.get(bstack1111_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢဲ"))
        }
    if env.get(bstack1111_opy_ (u"ࠥࡇࡎࠨဳ")) == bstack1111_opy_ (u"ࠦࡹࡸࡵࡦࠤဴ") and bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣဵ"))):
        return {
            bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦံ"): bstack1111_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧ့ࠥ"),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦး"): env.get(bstack1111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌ္ࠣ")),
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩ်ࠧ"): env.get(bstack1111_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤျ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦြ"): env.get(bstack1111_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤွ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡄࡋࠥှ")) == bstack1111_opy_ (u"ࠣࡶࡵࡹࡪࠨဿ") and bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧ၀"))):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ၁"): bstack1111_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦ၂"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ၃"): env.get(bstack1111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥ၄")),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ၅"): env.get(bstack1111_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ၆")),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ၇"): env.get(bstack1111_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨ၈"))
        }
    if env.get(bstack1111_opy_ (u"ࠦࡈࡏࠢ၉")) == bstack1111_opy_ (u"ࠧࡺࡲࡶࡧࠥ၊") and bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤ။"))):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ၌"): bstack1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ၍"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ၎"): env.get(bstack1111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ၏")),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨၐ"): env.get(bstack1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢၑ")) or env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤၒ")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨၓ"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥၔ"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦၕ"))):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣၖ"): bstack1111_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦၗ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣၘ"): bstack1111_opy_ (u"ࠨࡻࡾࡽࢀࠦၙ").format(env.get(bstack1111_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪၚ")), env.get(bstack1111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨၛ"))),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦၜ"): env.get(bstack1111_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤၝ")),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥၞ"): env.get(bstack1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧၟ"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣၠ"))):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧၡ"): bstack1111_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥၢ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧၣ"): bstack1111_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤၤ").format(env.get(bstack1111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪၥ")), env.get(bstack1111_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ၦ")), env.get(bstack1111_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧၧ")), env.get(bstack1111_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫၨ"))),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥၩ"): env.get(bstack1111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨၪ")),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤၫ"): env.get(bstack1111_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧၬ"))
        }
    if env.get(bstack1111_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨၭ")) and env.get(bstack1111_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣၮ")):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧၯ"): bstack1111_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥၰ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧၱ"): bstack1111_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨၲ").format(env.get(bstack1111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧၳ")), env.get(bstack1111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪၴ")), env.get(bstack1111_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ၵ"))),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤၶ"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣၷ")),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣၸ"): env.get(bstack1111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥၹ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤၺ")), env.get(bstack1111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦၻ")), env.get(bstack1111_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥၼ"))]):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧၽ"): bstack1111_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣၾ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧၿ"): env.get(bstack1111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤႀ")),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨႁ"): env.get(bstack1111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥႂ")),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧႃ"): env.get(bstack1111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧႄ"))
        }
    if env.get(bstack1111_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨႅ")):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢႆ"): bstack1111_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥႇ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢႈ"): env.get(bstack1111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢႉ")),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣႊ"): env.get(bstack1111_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨႋ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢႌ"): env.get(bstack1111_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸႍࠢ"))
        }
    if env.get(bstack1111_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦႎ")) or env.get(bstack1111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨႏ")):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ႐"): bstack1111_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢ႑"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ႒"): env.get(bstack1111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ႓")),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ႔"): bstack1111_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥ႕") if env.get(bstack1111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ႖")) else None,
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ႗"): env.get(bstack1111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦ႘"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧ႙")), env.get(bstack1111_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤႚ")), env.get(bstack1111_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤႛ"))]):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣႜ"): bstack1111_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥႝ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ႞"): None,
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ႟"): env.get(bstack1111_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦႠ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢႡ"): env.get(bstack1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦႢ"))
        }
    if env.get(bstack1111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨႣ")):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤႤ"): bstack1111_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣႥ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤႦ"): env.get(bstack1111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨႧ")),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥႨ"): bstack1111_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥႩ").format(env.get(bstack1111_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭Ⴊ"))) if env.get(bstack1111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢႫ")) else None,
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦႬ"): env.get(bstack1111_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣႭ"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣႮ"))):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨႯ"): bstack1111_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥႰ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨႱ"): env.get(bstack1111_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣႲ")),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢႳ"): env.get(bstack1111_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤႴ")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨႵ"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥႶ"))
        }
    if bstack1l11l1ll11_opy_(env.get(bstack1111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥႷ"))):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣႸ"): bstack1111_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧႹ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣႺ"): bstack1111_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢႻ").format(env.get(bstack1111_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫႼ")), env.get(bstack1111_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬႽ")), env.get(bstack1111_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩႾ"))),
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧႿ"): env.get(bstack1111_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨჀ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦჁ"): env.get(bstack1111_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨჂ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡄࡋࠥჃ")) == bstack1111_opy_ (u"ࠣࡶࡵࡹࡪࠨჄ") and env.get(bstack1111_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤჅ")) == bstack1111_opy_ (u"ࠥ࠵ࠧ჆"):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤჇ"): bstack1111_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧ჈"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ჉"): bstack1111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥ჊").format(env.get(bstack1111_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬ჋"))),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ჌"): None,
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤჍ"): None,
        }
    if env.get(bstack1111_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢ჎")):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ჏"): bstack1111_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣა"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥბ"): None,
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥგ"): env.get(bstack1111_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥდ")),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤე"): env.get(bstack1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥვ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣზ")), env.get(bstack1111_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨთ")), env.get(bstack1111_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧი")), env.get(bstack1111_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤკ"))]):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢლ"): bstack1111_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨმ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢნ"): None,
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢო"): env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢპ")) or None,
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨჟ"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥრ"), 0)
        }
    if env.get(bstack1111_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢს")):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣტ"): bstack1111_opy_ (u"ࠦࡌࡵࡃࡅࠤუ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣფ"): None,
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣქ"): env.get(bstack1111_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧღ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢყ"): env.get(bstack1111_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣშ"))
        }
    if env.get(bstack1111_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣჩ")):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤც"): bstack1111_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣძ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤწ"): env.get(bstack1111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨჭ")),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥხ"): env.get(bstack1111_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧჯ")),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤჰ"): env.get(bstack1111_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤჱ"))
        }
    return {bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦჲ"): None}
def get_host_info():
    return {
        bstack1111_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣჳ"): platform.node(),
        bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤჴ"): platform.system(),
        bstack1111_opy_ (u"ࠣࡶࡼࡴࡪࠨჵ"): platform.machine(),
        bstack1111_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥჶ"): platform.version(),
        bstack1111_opy_ (u"ࠥࡥࡷࡩࡨࠣჷ"): platform.architecture()[0]
    }
def bstack1111ll111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l11lll111_opy_():
    if bstack1llll1l1ll_opy_.get_property(bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬჸ")):
        return bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫჹ")
    return bstack1111_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬჺ")
def bstack1l111l1ll1_opy_(driver):
    info = {
        bstack1111_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭჻"): driver.capabilities,
        bstack1111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬჼ"): driver.session_id,
        bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪჽ"): driver.capabilities.get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨჾ"), None),
        bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ჿ"): driver.capabilities.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᄀ"), None),
        bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᄁ"): driver.capabilities.get(bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᄂ"), None),
    }
    if bstack1l11lll111_opy_() == bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᄃ"):
        info[bstack1111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᄄ")] = bstack1111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩᄅ") if bstack1l1ll11l1_opy_() else bstack1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᄆ")
    return info
def bstack1l1ll11l1_opy_():
    if bstack1llll1l1ll_opy_.get_property(bstack1111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᄇ")):
        return True
    if bstack1l11l1ll11_opy_(os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᄈ"), None)):
        return True
    return False
def bstack1ll1111l_opy_(bstack1l111l1lll_opy_, url, data, config):
    headers = config.get(bstack1111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᄉ"), None)
    proxies = bstack1l1llll11_opy_(config, url)
    auth = config.get(bstack1111_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᄊ"), None)
    response = requests.request(
            bstack1l111l1lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1lll1ll1_opy_(bstack1lll11lll1_opy_, size):
    bstack1llll1l1l1_opy_ = []
    while len(bstack1lll11lll1_opy_) > size:
        bstack11l1l1ll_opy_ = bstack1lll11lll1_opy_[:size]
        bstack1llll1l1l1_opy_.append(bstack11l1l1ll_opy_)
        bstack1lll11lll1_opy_ = bstack1lll11lll1_opy_[size:]
    bstack1llll1l1l1_opy_.append(bstack1lll11lll1_opy_)
    return bstack1llll1l1l1_opy_
def bstack1l111llll1_opy_(message, bstack1l111ll1ll_opy_=False):
    os.write(1, bytes(message, bstack1111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᄋ")))
    os.write(1, bytes(bstack1111_opy_ (u"ࠪࡠࡳ࠭ᄌ"), bstack1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᄍ")))
    if bstack1l111ll1ll_opy_:
        with open(bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫᄎ") + os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᄏ")] + bstack1111_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬᄐ"), bstack1111_opy_ (u"ࠨࡣࠪᄑ")) as f:
            f.write(message + bstack1111_opy_ (u"ࠩ࡟ࡲࠬᄒ"))
def bstack1l111l1l11_opy_():
    return os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᄓ")].lower() == bstack1111_opy_ (u"ࠫࡹࡸࡵࡦࠩᄔ")
def bstack1ll11l11_opy_(bstack1l111l1l1l_opy_):
    return bstack1111_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᄕ").format(bstack1l1l11111l_opy_, bstack1l111l1l1l_opy_)
def bstack1111111l1_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1111_opy_ (u"࡚࠭ࠨᄖ")
def bstack1l11lll1ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1111_opy_ (u"࡛ࠧࠩᄗ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1111_opy_ (u"ࠨ࡜ࠪᄘ")))).total_seconds() * 1000
def bstack1l11l1l1ll_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫᄙ")
def bstack1l11lll1l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᄚ")
    else:
        return bstack1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᄛ")
def bstack1l11l1ll11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1111_opy_ (u"ࠬࡺࡲࡶࡧࠪᄜ")
def bstack1l11l111l1_opy_(val):
    return val.__str__().lower() == bstack1111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᄝ")
def bstack1l1l1ll1ll_opy_(bstack1l1111l1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l1111l1l1_opy_ as e:
                print(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᄞ").format(func.__name__, bstack1l1111l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1l11l11lll_opy_(bstack1l11ll1l1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1l11ll1l1l_opy_(cls, *args, **kwargs)
            except bstack1l1111l1l1_opy_ as e:
                print(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᄟ").format(bstack1l11ll1l1l_opy_.__name__, bstack1l1111l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1l11l11lll_opy_
    else:
        return decorator
def bstack1l111lll1_opy_(bstack1l1ll11lll_opy_):
    if bstack1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᄠ") in bstack1l1ll11lll_opy_ and bstack1l11l111l1_opy_(bstack1l1ll11lll_opy_[bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄡ")]):
        return False
    if bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᄢ") in bstack1l1ll11lll_opy_ and bstack1l11l111l1_opy_(bstack1l1ll11lll_opy_[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄣ")]):
        return False
    return True
def bstack111l1ll11_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l1111ll_opy_(hub_url):
    if bstack1llll1ll1_opy_() <= version.parse(bstack1111_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ᄤ")):
        if hub_url != bstack1111_opy_ (u"ࠧࠨᄥ"):
            return bstack1111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᄦ") + hub_url + bstack1111_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᄧ")
        return bstack111lll111_opy_
    if hub_url != bstack1111_opy_ (u"ࠪࠫᄨ"):
        return bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᄩ") + hub_url + bstack1111_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨᄪ")
    return bstack1lll1ll11l_opy_
def bstack1l11l1lll1_opy_():
    return isinstance(os.getenv(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬᄫ")), str)
def bstack1lll1l1ll1_opy_(url):
    return urlparse(url).hostname
def bstack1l1lllll1_opy_(hostname):
    for bstack111ll1ll_opy_ in bstack1l1111111_opy_:
        regex = re.compile(bstack111ll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1l111l11ll_opy_(bstack1l11l11ll1_opy_, file_name, logger):
    bstack11ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠧࡿࠩᄬ")), bstack1l11l11ll1_opy_)
    try:
        if not os.path.exists(bstack11ll1ll1_opy_):
            os.makedirs(bstack11ll1ll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠨࢀࠪᄭ")), bstack1l11l11ll1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111_opy_ (u"ࠩࡺࠫᄮ")):
                pass
            with open(file_path, bstack1111_opy_ (u"ࠥࡻ࠰ࠨᄯ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lllll1lll_opy_.format(str(e)))
def bstack1l11ll1l11_opy_(file_name, key, value, logger):
    file_path = bstack1l111l11ll_opy_(bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᄰ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11llll1l_opy_ = json.load(open(file_path, bstack1111_opy_ (u"ࠬࡸࡢࠨᄱ")))
        else:
            bstack11llll1l_opy_ = {}
        bstack11llll1l_opy_[key] = value
        with open(file_path, bstack1111_opy_ (u"ࠨࡷࠬࠤᄲ")) as outfile:
            json.dump(bstack11llll1l_opy_, outfile)
def bstack1ll111l1l_opy_(file_name, logger):
    file_path = bstack1l111l11ll_opy_(bstack1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᄳ"), file_name, logger)
    bstack11llll1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111_opy_ (u"ࠨࡴࠪᄴ")) as bstack11ll1l1l1_opy_:
            bstack11llll1l_opy_ = json.load(bstack11ll1l1l1_opy_)
    return bstack11llll1l_opy_
def bstack111ll11ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ᄵ") + file_path + bstack1111_opy_ (u"ࠪࠤࠬᄶ") + str(e))
def bstack1llll1ll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨᄷ")
def bstack1lll11l1_opy_(config):
    if bstack1111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᄸ") in config:
        del (config[bstack1111_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᄹ")])
        return False
    if bstack1llll1ll1_opy_() < version.parse(bstack1111_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭ᄺ")):
        return False
    if bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧᄻ")):
        return True
    if bstack1111_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᄼ") in config and config[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᄽ")] is False:
        return False
    else:
        return True
def bstack1ll1l1l11_opy_(args_list, bstack1l11ll1lll_opy_):
    index = -1
    for value in bstack1l11ll1lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11ll1111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11ll1111_opy_ = bstack1l11ll1111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᄾ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᄿ"), exception=exception)
    def bstack1l11lll11l_opy_(self):
        if self.result != bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᅀ"):
            return None
        if bstack1111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᅁ") in self.exception_type:
            return bstack1111_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᅂ")
        return bstack1111_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᅃ")
    def bstack1l11ll111l_opy_(self):
        if self.result != bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᅄ"):
            return None
        if self.bstack1l11ll1111_opy_:
            return self.bstack1l11ll1111_opy_
        return bstack1l11l11111_opy_(self.exception)
def bstack1l11l11111_opy_(exc):
    return traceback.format_exception(exc)
def bstack1l111ll111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll111l111_opy_(object, key, default_value):
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l1l111_opy_(config, logger):
    try:
        import playwright
        bstack1l111l11l1_opy_ = playwright.__file__
        bstack1l1111llll_opy_ = os.path.split(bstack1l111l11l1_opy_)
        bstack1l11ll1ll1_opy_ = bstack1l1111llll_opy_[0] + bstack1111_opy_ (u"ࠫ࠴ࡪࡲࡪࡸࡨࡶ࠴ࡶࡡࡤ࡭ࡤ࡫ࡪ࠵࡬ࡪࡤ࠲ࡧࡱ࡯࠯ࡤ࡮࡬࠲࡯ࡹࠧᅅ")
        os.environ[bstack1111_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠨᅆ")] = bstack111ll1111_opy_(config)
        with open(bstack1l11ll1ll1_opy_, bstack1111_opy_ (u"࠭ࡲࠨᅇ")) as f:
            bstack1111l11ll_opy_ = f.read()
            bstack1l1111ll1l_opy_ = bstack1111_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ᅈ")
            bstack1l11l1ll1l_opy_ = bstack1111l11ll_opy_.find(bstack1l1111ll1l_opy_)
            if bstack1l11l1ll1l_opy_ is -1:
              process = subprocess.Popen(bstack1111_opy_ (u"ࠣࡰࡳࡱࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠧᅉ"), shell=True, cwd=bstack1l1111llll_opy_[0])
              process.wait()
              bstack1l11l111ll_opy_ = bstack1111_opy_ (u"ࠩࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺࠢ࠼ࠩᅊ")
              bstack1l11l11l1l_opy_ = bstack1111_opy_ (u"ࠥࠦࠧࠦ࡜ࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࡡࠨ࠻ࠡࡥࡲࡲࡸࡺࠠࡼࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴࠥࢃࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ࠭ࡀࠦࡩࡧࠢࠫࡴࡷࡵࡣࡦࡵࡶ࠲ࡪࡴࡶ࠯ࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜࠭ࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠩࠫ࠾ࠤࠧࠨࠢᅋ")
              bstack1l11l1l111_opy_ = bstack1111l11ll_opy_.replace(bstack1l11l111ll_opy_, bstack1l11l11l1l_opy_)
              with open(bstack1l11ll1ll1_opy_, bstack1111_opy_ (u"ࠫࡼ࠭ᅌ")) as f:
                f.write(bstack1l11l1l111_opy_)
    except Exception as e:
        logger.error(bstack1ll111ll11_opy_.format(str(e)))
def bstack1llll1l1_opy_():
  try:
    bstack1l11l1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᅍ"))
    bstack1l1111l1ll_opy_ = []
    if os.path.exists(bstack1l11l1l1l1_opy_):
      with open(bstack1l11l1l1l1_opy_) as f:
        bstack1l1111l1ll_opy_ = json.load(f)
      os.remove(bstack1l11l1l1l1_opy_)
    return bstack1l1111l1ll_opy_
  except:
    pass
  return []
def bstack1l11ll111_opy_(bstack11l1l111l_opy_):
  try:
    bstack1l1111l1ll_opy_ = []
    bstack1l11l1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᅎ"))
    if os.path.exists(bstack1l11l1l1l1_opy_):
      with open(bstack1l11l1l1l1_opy_) as f:
        bstack1l1111l1ll_opy_ = json.load(f)
    bstack1l1111l1ll_opy_.append(bstack11l1l111l_opy_)
    with open(bstack1l11l1l1l1_opy_, bstack1111_opy_ (u"ࠧࡸࠩᅏ")) as f:
        json.dump(bstack1l1111l1ll_opy_, f)
  except:
    pass
def bstack11l1ll11l_opy_(logger, bstack1l1111lll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᅐ"), bstack1111_opy_ (u"ࠩࠪᅑ"))
    if test_name == bstack1111_opy_ (u"ࠪࠫᅒ"):
        test_name = threading.current_thread().__dict__.get(bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡆࡩࡪ࡟ࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠪᅓ"), bstack1111_opy_ (u"ࠬ࠭ᅔ"))
    bstack1l11l1l11l_opy_ = bstack1111_opy_ (u"࠭ࠬࠡࠩᅕ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1l1111lll1_opy_:
        bstack1ll111ll1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᅖ"), bstack1111_opy_ (u"ࠨ࠲ࠪᅗ"))
        bstack1llllll11_opy_ = {bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᅘ"): test_name, bstack1111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᅙ"): bstack1l11l1l11l_opy_, bstack1111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᅚ"): bstack1ll111ll1_opy_}
        bstack1l111ll1l1_opy_ = []
        bstack1l11ll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᅛ"))
        if os.path.exists(bstack1l11ll11ll_opy_):
            with open(bstack1l11ll11ll_opy_) as f:
                bstack1l111ll1l1_opy_ = json.load(f)
        bstack1l111ll1l1_opy_.append(bstack1llllll11_opy_)
        with open(bstack1l11ll11ll_opy_, bstack1111_opy_ (u"࠭ࡷࠨᅜ")) as f:
            json.dump(bstack1l111ll1l1_opy_, f)
    else:
        bstack1llllll11_opy_ = {bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᅝ"): test_name, bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᅞ"): bstack1l11l1l11l_opy_, bstack1111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᅟ"): str(multiprocessing.current_process().name)}
        if bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧᅠ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack1l1lll1l1_opy_ = []
        multiprocessing.current_process().bstack1l1lll1l1_opy_.append(bstack1llllll11_opy_)
  except Exception as e:
      logger.warn(bstack1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡰࡺࡶࡨࡷࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᅡ").format(e))
def bstack1l11l111_opy_(error_message, test_name, index, logger):
  try:
    bstack1l111ll11l_opy_ = []
    bstack1llllll11_opy_ = {bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᅢ"): test_name, bstack1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᅣ"): error_message, bstack1111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᅤ"): index}
    bstack1l111l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᅥ"))
    if os.path.exists(bstack1l111l111l_opy_):
        with open(bstack1l111l111l_opy_) as f:
            bstack1l111ll11l_opy_ = json.load(f)
    bstack1l111ll11l_opy_.append(bstack1llllll11_opy_)
    with open(bstack1l111l111l_opy_, bstack1111_opy_ (u"ࠩࡺࠫᅦ")) as f:
        json.dump(bstack1l111ll11l_opy_, f)
  except Exception as e:
    logger.warn(bstack1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᅧ").format(e))
def bstack1l111l11l_opy_(bstack1l1l1l1l1_opy_, name, logger):
  try:
    bstack1llllll11_opy_ = {bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᅨ"): name, bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᅩ"): bstack1l1l1l1l1_opy_, bstack1111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᅪ"): str(threading.current_thread()._name)}
    return bstack1llllll11_opy_
  except Exception as e:
    logger.warn(bstack1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᅫ").format(e))
  return