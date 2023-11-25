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
from bstack_utils.constants import bstack1l1l1111l1_opy_, bstack1111ll1l1_opy_, bstack11l11111l_opy_, bstack1lllll11_opy_
from bstack_utils.messages import bstack1l1l111l1_opy_, bstack11l1l1l1l_opy_
from bstack_utils.proxy import bstack11lll1111_opy_, bstack11lllll1l_opy_
bstack1lll1l1111_opy_ = Config.get_instance()
def bstack1l1l1lllll_opy_(config):
    return config[bstack11lll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ࿗")]
def bstack1l1l11l1ll_opy_(config):
    return config[bstack11lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭࿘")]
def bstack1ll111l1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1l1111llll_opy_(obj):
    values = []
    bstack1l11ll1lll_opy_ = re.compile(bstack11lll1l_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣ࿙"), re.I)
    for key in obj.keys():
        if bstack1l11ll1lll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l11l11111_opy_(config):
    tags = []
    tags.extend(bstack1l1111llll_opy_(os.environ))
    tags.extend(bstack1l1111llll_opy_(config))
    return tags
def bstack1l11l111ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l11ll1ll1_opy_(bstack1l111ll11l_opy_):
    if not bstack1l111ll11l_opy_:
        return bstack11lll1l_opy_ (u"ࠬ࠭࿚")
    return bstack11lll1l_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢ࿛").format(bstack1l111ll11l_opy_.name, bstack1l111ll11l_opy_.email)
def bstack1l1l1ll1l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1l11l11lll_opy_ = repo.common_dir
        info = {
            bstack11lll1l_opy_ (u"ࠢࡴࡪࡤࠦ࿜"): repo.head.commit.hexsha,
            bstack11lll1l_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦ࿝"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11lll1l_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤ࿞"): repo.active_branch.name,
            bstack11lll1l_opy_ (u"ࠥࡸࡦ࡭ࠢ࿟"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11lll1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢ࿠"): bstack1l11ll1ll1_opy_(repo.head.commit.committer),
            bstack11lll1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨ࿡"): repo.head.commit.committed_datetime.isoformat(),
            bstack11lll1l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨ࿢"): bstack1l11ll1ll1_opy_(repo.head.commit.author),
            bstack11lll1l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧ࿣"): repo.head.commit.authored_datetime.isoformat(),
            bstack11lll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ࿤"): repo.head.commit.message,
            bstack11lll1l_opy_ (u"ࠤࡵࡳࡴࡺࠢ࿥"): repo.git.rev_parse(bstack11lll1l_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧ࿦")),
            bstack11lll1l_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ࿧"): bstack1l11l11lll_opy_,
            bstack11lll1l_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ࿨"): subprocess.check_output([bstack11lll1l_opy_ (u"ࠨࡧࡪࡶࠥ࿩"), bstack11lll1l_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥ࿪"), bstack11lll1l_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦ࿫")]).strip().decode(
                bstack11lll1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ࿬")),
            bstack11lll1l_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ࿭"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11lll1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ࿮"): repo.git.rev_list(
                bstack11lll1l_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧ࿯").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1l1111lll1_opy_ = []
        for remote in remotes:
            bstack1l111l11ll_opy_ = {
                bstack11lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ࿰"): remote.name,
                bstack11lll1l_opy_ (u"ࠢࡶࡴ࡯ࠦ࿱"): remote.url,
            }
            bstack1l1111lll1_opy_.append(bstack1l111l11ll_opy_)
        return {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ࿲"): bstack11lll1l_opy_ (u"ࠤࡪ࡭ࡹࠨ࿳"),
            **info,
            bstack11lll1l_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦ࿴"): bstack1l1111lll1_opy_
        }
    except Exception as err:
        print(bstack11lll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ࿵").format(err))
        return {}
def bstack1ll11111_opy_():
    env = os.environ
    if (bstack11lll1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ࿶") in env and len(env[bstack11lll1l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ࿷")]) > 0) or (
            bstack11lll1l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ࿸") in env and len(env[bstack11lll1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ࿹")]) > 0):
        return {
            bstack11lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿺"): bstack11lll1l_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦ࿻"),
            bstack11lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ࿼"): env.get(bstack11lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ࿽")),
            bstack11lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ࿾"): env.get(bstack11lll1l_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤ࿿")),
            bstack11lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢက"): env.get(bstack11lll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣခ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠥࡇࡎࠨဂ")) == bstack11lll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤဃ") and bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢင"))):
        return {
            bstack11lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦစ"): bstack11lll1l_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤဆ"),
            bstack11lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦဇ"): env.get(bstack11lll1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧဈ")),
            bstack11lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧဉ"): env.get(bstack11lll1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣည")),
            bstack11lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦဋ"): env.get(bstack11lll1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤဌ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠢࡄࡋࠥဍ")) == bstack11lll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨဎ") and bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤဏ"))):
        return {
            bstack11lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣတ"): bstack11lll1l_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢထ"),
            bstack11lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣဒ"): env.get(bstack11lll1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨဓ")),
            bstack11lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤန"): env.get(bstack11lll1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥပ")),
            bstack11lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣဖ"): env.get(bstack11lll1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤဗ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠦࡈࡏࠢဘ")) == bstack11lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥမ") and env.get(bstack11lll1l_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢယ")) == bstack11lll1l_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤရ"):
        return {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨလ"): bstack11lll1l_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦဝ"),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨသ"): None,
            bstack11lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨဟ"): None,
            bstack11lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦဠ"): None
        }
    if env.get(bstack11lll1l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤအ")) and env.get(bstack11lll1l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥဢ")):
        return {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨဣ"): bstack11lll1l_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧဤ"),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨဥ"): env.get(bstack11lll1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤဦ")),
            bstack11lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢဧ"): None,
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧဨ"): env.get(bstack11lll1l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤဩ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠣࡅࡌࠦဪ")) == bstack11lll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢါ") and bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤာ"))):
        return {
            bstack11lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤိ"): bstack11lll1l_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦီ"),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤု"): env.get(bstack11lll1l_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥူ")),
            bstack11lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥေ"): None,
            bstack11lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣဲ"): env.get(bstack11lll1l_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣဳ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠦࡈࡏࠢဴ")) == bstack11lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥဵ") and bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤံ"))):
        return {
            bstack11lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩ့ࠧ"): bstack11lll1l_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦး"),
            bstack11lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰ္ࠧ"): env.get(bstack11lll1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤ်")),
            bstack11lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨျ"): env.get(bstack11lll1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥြ")),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧွ"): env.get(bstack11lll1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥှ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠣࡅࡌࠦဿ")) == bstack11lll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ၀") and bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨ၁"))):
        return {
            bstack11lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ၂"): bstack11lll1l_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧ၃"),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ၄"): env.get(bstack11lll1l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦ၅")),
            bstack11lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ၆"): env.get(bstack11lll1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ၇")),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ၈"): env.get(bstack11lll1l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢ၉"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠧࡉࡉࠣ၊")) == bstack11lll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦ။") and bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥ၌"))):
        return {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ၍"): bstack11lll1l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧ၎"),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ၏"): env.get(bstack11lll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥၐ")),
            bstack11lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢၑ"): env.get(bstack11lll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣၒ")) or env.get(bstack11lll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥၓ")),
            bstack11lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢၔ"): env.get(bstack11lll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦၕ"))
        }
    if bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧၖ"))):
        return {
            bstack11lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤၗ"): bstack11lll1l_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧၘ"),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤၙ"): bstack11lll1l_opy_ (u"ࠢࡼࡿࡾࢁࠧၚ").format(env.get(bstack11lll1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫၛ")), env.get(bstack11lll1l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩၜ"))),
            bstack11lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧၝ"): env.get(bstack11lll1l_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥၞ")),
            bstack11lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦၟ"): env.get(bstack11lll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨၠ"))
        }
    if bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤၡ"))):
        return {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨၢ"): bstack11lll1l_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦၣ"),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨၤ"): bstack11lll1l_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥၥ").format(env.get(bstack11lll1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫၦ")), env.get(bstack11lll1l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧၧ")), env.get(bstack11lll1l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨၨ")), env.get(bstack11lll1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬၩ"))),
            bstack11lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦၪ"): env.get(bstack11lll1l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢၫ")),
            bstack11lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥၬ"): env.get(bstack11lll1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨၭ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢၮ")) and env.get(bstack11lll1l_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤၯ")):
        return {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨၰ"): bstack11lll1l_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦၱ"),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨၲ"): bstack11lll1l_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢၳ").format(env.get(bstack11lll1l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨၴ")), env.get(bstack11lll1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫၵ")), env.get(bstack11lll1l_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧၶ"))),
            bstack11lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥၷ"): env.get(bstack11lll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤၸ")),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤၹ"): env.get(bstack11lll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦၺ"))
        }
    if any([env.get(bstack11lll1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥၻ")), env.get(bstack11lll1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧၼ")), env.get(bstack11lll1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦၽ"))]):
        return {
            bstack11lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨၾ"): bstack11lll1l_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤၿ"),
            bstack11lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨႀ"): env.get(bstack11lll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥႁ")),
            bstack11lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢႂ"): env.get(bstack11lll1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦႃ")),
            bstack11lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨႄ"): env.get(bstack11lll1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨႅ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢႆ")):
        return {
            bstack11lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣႇ"): bstack11lll1l_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦႈ"),
            bstack11lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣႉ"): env.get(bstack11lll1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣႊ")),
            bstack11lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤႋ"): env.get(bstack11lll1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢႌ")),
            bstack11lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲႍࠣ"): env.get(bstack11lll1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣႎ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧႏ")) or env.get(bstack11lll1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ႐")):
        return {
            bstack11lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ႑"): bstack11lll1l_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣ႒"),
            bstack11lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ႓"): env.get(bstack11lll1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ႔")),
            bstack11lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ႕"): bstack11lll1l_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦ႖") if env.get(bstack11lll1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ႗")) else None,
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ႘"): env.get(bstack11lll1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧ႙"))
        }
    if any([env.get(bstack11lll1l_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨႚ")), env.get(bstack11lll1l_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥႛ")), env.get(bstack11lll1l_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥႜ"))]):
        return {
            bstack11lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤႝ"): bstack11lll1l_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦ႞"),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ႟"): None,
            bstack11lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤႠ"): env.get(bstack11lll1l_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧႡ")),
            bstack11lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣႢ"): env.get(bstack11lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧႣ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢႤ")):
        return {
            bstack11lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥႥ"): bstack11lll1l_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤႦ"),
            bstack11lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥႧ"): env.get(bstack11lll1l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢႨ")),
            bstack11lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦႩ"): bstack11lll1l_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦႪ").format(env.get(bstack11lll1l_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧႫ"))) if env.get(bstack11lll1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣႬ")) else None,
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧႭ"): env.get(bstack11lll1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤႮ"))
        }
    if bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤႯ"))):
        return {
            bstack11lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢႰ"): bstack11lll1l_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦႱ"),
            bstack11lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢႲ"): env.get(bstack11lll1l_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤႳ")),
            bstack11lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣႴ"): env.get(bstack11lll1l_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥႵ")),
            bstack11lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢႶ"): env.get(bstack11lll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦႷ"))
        }
    if bstack1l111lll1l_opy_(env.get(bstack11lll1l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦႸ"))):
        return {
            bstack11lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤႹ"): bstack11lll1l_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨႺ"),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤႻ"): bstack11lll1l_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣႼ").format(env.get(bstack11lll1l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬႽ")), env.get(bstack11lll1l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭Ⴞ")), env.get(bstack11lll1l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪႿ"))),
            bstack11lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨჀ"): env.get(bstack11lll1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢჁ")),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧჂ"): env.get(bstack11lll1l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢჃ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠣࡅࡌࠦჄ")) == bstack11lll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢჅ") and env.get(bstack11lll1l_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥ჆")) == bstack11lll1l_opy_ (u"ࠦ࠶ࠨჇ"):
        return {
            bstack11lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ჈"): bstack11lll1l_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨ჉"),
            bstack11lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ჊"): bstack11lll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦ჋").format(env.get(bstack11lll1l_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭჌"))),
            bstack11lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧჍ"): None,
            bstack11lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ჎"): None,
        }
    if env.get(bstack11lll1l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣ჏")):
        return {
            bstack11lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦა"): bstack11lll1l_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤბ"),
            bstack11lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦგ"): None,
            bstack11lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦდ"): env.get(bstack11lll1l_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦე")),
            bstack11lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥვ"): env.get(bstack11lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦზ"))
        }
    if any([env.get(bstack11lll1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤთ")), env.get(bstack11lll1l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢი")), env.get(bstack11lll1l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨკ")), env.get(bstack11lll1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥლ"))]):
        return {
            bstack11lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣმ"): bstack11lll1l_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢნ"),
            bstack11lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣო"): None,
            bstack11lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣპ"): env.get(bstack11lll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣჟ")) or None,
            bstack11lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢრ"): env.get(bstack11lll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦს"), 0)
        }
    if env.get(bstack11lll1l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣტ")):
        return {
            bstack11lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤუ"): bstack11lll1l_opy_ (u"ࠧࡍ࡯ࡄࡆࠥფ"),
            bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤქ"): None,
            bstack11lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤღ"): env.get(bstack11lll1l_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨყ")),
            bstack11lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣშ"): env.get(bstack11lll1l_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤჩ"))
        }
    if env.get(bstack11lll1l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤც")):
        return {
            bstack11lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥძ"): bstack11lll1l_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤწ"),
            bstack11lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥჭ"): env.get(bstack11lll1l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢხ")),
            bstack11lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦჯ"): env.get(bstack11lll1l_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨჰ")),
            bstack11lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥჱ"): env.get(bstack11lll1l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥჲ"))
        }
    return {bstack11lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧჳ"): None}
def get_host_info():
    return {
        bstack11lll1l_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤჴ"): platform.node(),
        bstack11lll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥჵ"): platform.system(),
        bstack11lll1l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢჶ"): platform.machine(),
        bstack11lll1l_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦჷ"): platform.version(),
        bstack11lll1l_opy_ (u"ࠦࡦࡸࡣࡩࠤჸ"): platform.architecture()[0]
    }
def bstack1l1l1llll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l1111l1ll_opy_():
    if bstack1lll1l1111_opy_.get_property(bstack11lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ჹ")):
        return bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬჺ")
    return bstack11lll1l_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭჻")
def bstack1l11l1llll_opy_(driver):
    info = {
        bstack11lll1l_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧჼ"): driver.capabilities,
        bstack11lll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ჽ"): driver.session_id,
        bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫჾ"): driver.capabilities.get(bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩჿ"), None),
        bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᄀ"): driver.capabilities.get(bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᄁ"), None),
        bstack11lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᄂ"): driver.capabilities.get(bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᄃ"), None),
    }
    if bstack1l1111l1ll_opy_() == bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᄄ"):
        info[bstack11lll1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᄅ")] = bstack11lll1l_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪᄆ") if bstack11l11l1ll_opy_() else bstack11lll1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᄇ")
    return info
def bstack11l11l1ll_opy_():
    if bstack1lll1l1111_opy_.get_property(bstack11lll1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᄈ")):
        return True
    if bstack1l111lll1l_opy_(os.environ.get(bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᄉ"), None)):
        return True
    return False
def bstack11l1l11l1_opy_(bstack1l111ll111_opy_, url, data, config):
    headers = config.get(bstack11lll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᄊ"), None)
    proxies = bstack11lll1111_opy_(config, url)
    auth = config.get(bstack11lll1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᄋ"), None)
    response = requests.request(
            bstack1l111ll111_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lll1l1l1l_opy_(bstack11111l1l_opy_, size):
    bstack1lll11lll_opy_ = []
    while len(bstack11111l1l_opy_) > size:
        bstack11111l11l_opy_ = bstack11111l1l_opy_[:size]
        bstack1lll11lll_opy_.append(bstack11111l11l_opy_)
        bstack11111l1l_opy_ = bstack11111l1l_opy_[size:]
    bstack1lll11lll_opy_.append(bstack11111l1l_opy_)
    return bstack1lll11lll_opy_
def bstack1l11ll111l_opy_(message, bstack1l11l1l1l1_opy_=False):
    os.write(1, bytes(message, bstack11lll1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᄌ")))
    os.write(1, bytes(bstack11lll1l_opy_ (u"ࠫࡡࡴࠧᄍ"), bstack11lll1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᄎ")))
    if bstack1l11l1l1l1_opy_:
        with open(bstack11lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᄏ") + os.environ[bstack11lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᄐ")] + bstack11lll1l_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ᄑ"), bstack11lll1l_opy_ (u"ࠩࡤࠫᄒ")) as f:
            f.write(message + bstack11lll1l_opy_ (u"ࠪࡠࡳ࠭ᄓ"))
def bstack1l11lll111_opy_():
    return os.environ[bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᄔ")].lower() == bstack11lll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᄕ")
def bstack1lllll11ll_opy_(bstack1l111l11l1_opy_):
    return bstack11lll1l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᄖ").format(bstack1l1l1111l1_opy_, bstack1l111l11l1_opy_)
def bstack11l1l1111_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11lll1l_opy_ (u"࡛ࠧࠩᄗ")
def bstack1l11l1ll11_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11lll1l_opy_ (u"ࠨ࡜ࠪᄘ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11lll1l_opy_ (u"ࠩ࡝ࠫᄙ")))).total_seconds() * 1000
def bstack1l111lll11_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11lll1l_opy_ (u"ࠪ࡞ࠬᄚ")
def bstack1l111l1lll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᄛ")
    else:
        return bstack11lll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᄜ")
def bstack1l111lll1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11lll1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᄝ")
def bstack1l1111ll1l_opy_(val):
    return val.__str__().lower() == bstack11lll1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᄞ")
def bstack1l1l1l1lll_opy_(bstack1l11l111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l11l111l1_opy_ as e:
                print(bstack11lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᄟ").format(func.__name__, bstack1l11l111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1l11lll1l1_opy_(bstack1l111l111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1l111l111l_opy_(cls, *args, **kwargs)
            except bstack1l11l111l1_opy_ as e:
                print(bstack11lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᄠ").format(bstack1l111l111l_opy_.__name__, bstack1l11l111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1l11lll1l1_opy_
    else:
        return decorator
def bstack1l1l11l1_opy_(bstack1l1ll11l1l_opy_):
    if bstack11lll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄡ") in bstack1l1ll11l1l_opy_ and bstack1l1111ll1l_opy_(bstack1l1ll11l1l_opy_[bstack11lll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᄢ")]):
        return False
    if bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᄣ") in bstack1l1ll11l1l_opy_ and bstack1l1111ll1l_opy_(bstack1l1ll11l1l_opy_[bstack11lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᄤ")]):
        return False
    return True
def bstack1ll1111111_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack111l11111_opy_(hub_url):
    if bstack1ll1ll11_opy_() <= version.parse(bstack11lll1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᄥ")):
        if hub_url != bstack11lll1l_opy_ (u"ࠨࠩᄦ"):
            return bstack11lll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᄧ") + hub_url + bstack11lll1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᄨ")
        return bstack11l11111l_opy_
    if hub_url != bstack11lll1l_opy_ (u"ࠫࠬᄩ"):
        return bstack11lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᄪ") + hub_url + bstack11lll1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᄫ")
    return bstack1lllll11_opy_
def bstack1l11l1ll1l_opy_():
    return isinstance(os.getenv(bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᄬ")), str)
def bstack1ll1111ll1_opy_(url):
    return urlparse(url).hostname
def bstack111lllll_opy_(hostname):
    for bstack1ll111l1ll_opy_ in bstack1111ll1l1_opy_:
        regex = re.compile(bstack1ll111l1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1l111lllll_opy_(bstack1l11ll1l1l_opy_, file_name, logger):
    bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠨࢀࠪᄭ")), bstack1l11ll1l1l_opy_)
    try:
        if not os.path.exists(bstack111ll1111_opy_):
            os.makedirs(bstack111ll1111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11lll1l_opy_ (u"ࠩࢁࠫᄮ")), bstack1l11ll1l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11lll1l_opy_ (u"ࠪࡻࠬᄯ")):
                pass
            with open(file_path, bstack11lll1l_opy_ (u"ࠦࡼ࠱ࠢᄰ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1l111l1_opy_.format(str(e)))
def bstack1l11ll11ll_opy_(file_name, key, value, logger):
    file_path = bstack1l111lllll_opy_(bstack11lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᄱ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1l1l11_opy_ = json.load(open(file_path, bstack11lll1l_opy_ (u"࠭ࡲࡣࠩᄲ")))
        else:
            bstack11l1l1l11_opy_ = {}
        bstack11l1l1l11_opy_[key] = value
        with open(file_path, bstack11lll1l_opy_ (u"ࠢࡸ࠭ࠥᄳ")) as outfile:
            json.dump(bstack11l1l1l11_opy_, outfile)
def bstack1l11l1ll_opy_(file_name, logger):
    file_path = bstack1l111lllll_opy_(bstack11lll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᄴ"), file_name, logger)
    bstack11l1l1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11lll1l_opy_ (u"ࠩࡵࠫᄵ")) as bstack1lll1lll11_opy_:
            bstack11l1l1l11_opy_ = json.load(bstack1lll1lll11_opy_)
    return bstack11l1l1l11_opy_
def bstack11l1111l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11lll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᄶ") + file_path + bstack11lll1l_opy_ (u"ࠫࠥ࠭ᄷ") + str(e))
def bstack1ll1ll11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11lll1l_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᄸ")
def bstack1l111l1l_opy_(config):
    if bstack11lll1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᄹ") in config:
        del (config[bstack11lll1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᄺ")])
        return False
    if bstack1ll1ll11_opy_() < version.parse(bstack11lll1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᄻ")):
        return False
    if bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᄼ")):
        return True
    if bstack11lll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᄽ") in config and config[bstack11lll1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᄾ")] is False:
        return False
    else:
        return True
def bstack1ll11ll1_opy_(args_list, bstack1l11ll1l11_opy_):
    index = -1
    for value in bstack1l11ll1l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11l1l111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11l1l111_opy_ = bstack1l11l1l111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11lll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᄿ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᅀ"), exception=exception)
    def bstack1l111l1ll1_opy_(self):
        if self.result != bstack11lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᅁ"):
            return None
        if bstack11lll1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᅂ") in self.exception_type:
            return bstack11lll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᅃ")
        return bstack11lll1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᅄ")
    def bstack1l1111l1l1_opy_(self):
        if self.result != bstack11lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᅅ"):
            return None
        if self.bstack1l11l1l111_opy_:
            return self.bstack1l11l1l111_opy_
        return bstack1l111l1l1l_opy_(self.exception)
def bstack1l111l1l1l_opy_(exc):
    return traceback.format_exception(exc)
def bstack1l11lll1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11lll111_opy_(object, key, default_value):
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lll111lll_opy_(config, logger):
    try:
        import playwright
        bstack1l11l1lll1_opy_ = playwright.__file__
        bstack1l11lll11l_opy_ = os.path.split(bstack1l11l1lll1_opy_)
        bstack1l11l1111l_opy_ = bstack1l11lll11l_opy_[0] + bstack11lll1l_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᅆ")
        os.environ[bstack11lll1l_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᅇ")] = bstack11lllll1l_opy_(config)
        with open(bstack1l11l1111l_opy_, bstack11lll1l_opy_ (u"ࠧࡳࠩᅈ")) as f:
            bstack1llll1l1l_opy_ = f.read()
            bstack1l111l1111_opy_ = bstack11lll1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᅉ")
            bstack1l11ll11l1_opy_ = bstack1llll1l1l_opy_.find(bstack1l111l1111_opy_)
            if bstack1l11ll11l1_opy_ == -1:
              process = subprocess.Popen(bstack11lll1l_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᅊ"), shell=True, cwd=bstack1l11lll11l_opy_[0])
              process.wait()
              bstack1l11l11l11_opy_ = bstack11lll1l_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᅋ")
              bstack1l111ll1l1_opy_ = bstack11lll1l_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᅌ")
              bstack1l111ll1ll_opy_ = bstack1llll1l1l_opy_.replace(bstack1l11l11l11_opy_, bstack1l111ll1l1_opy_)
              with open(bstack1l11l1111l_opy_, bstack11lll1l_opy_ (u"ࠬࡽࠧᅍ")) as f:
                f.write(bstack1l111ll1ll_opy_)
    except Exception as e:
        logger.error(bstack11l1l1l1l_opy_.format(str(e)))
def bstack111l11l1l_opy_():
  try:
    bstack1l11l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᅎ"))
    bstack1l1111ll11_opy_ = []
    if os.path.exists(bstack1l11l1l11l_opy_):
      with open(bstack1l11l1l11l_opy_) as f:
        bstack1l1111ll11_opy_ = json.load(f)
      os.remove(bstack1l11l1l11l_opy_)
    return bstack1l1111ll11_opy_
  except:
    pass
  return []
def bstack11llll11l_opy_(bstack1lll1lll1_opy_):
  try:
    bstack1l1111ll11_opy_ = []
    bstack1l11l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᅏ"))
    if os.path.exists(bstack1l11l1l11l_opy_):
      with open(bstack1l11l1l11l_opy_) as f:
        bstack1l1111ll11_opy_ = json.load(f)
    bstack1l1111ll11_opy_.append(bstack1lll1lll1_opy_)
    with open(bstack1l11l1l11l_opy_, bstack11lll1l_opy_ (u"ࠨࡹࠪᅐ")) as f:
        json.dump(bstack1l1111ll11_opy_, f)
  except:
    pass
def bstack1ll11llll_opy_(logger, bstack1l11l11l1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack11lll1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᅑ"), bstack11lll1l_opy_ (u"ࠪࠫᅒ"))
    if test_name == bstack11lll1l_opy_ (u"ࠫࠬᅓ"):
        test_name = threading.current_thread().__dict__.get(bstack11lll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᅔ"), bstack11lll1l_opy_ (u"࠭ࠧᅕ"))
    bstack1l111l1l11_opy_ = bstack11lll1l_opy_ (u"ࠧ࠭ࠢࠪᅖ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1l11l11l1l_opy_:
        bstack1ll11ll11l_opy_ = os.environ.get(bstack11lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᅗ"), bstack11lll1l_opy_ (u"ࠩ࠳ࠫᅘ"))
        bstack1ll11l111_opy_ = {bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᅙ"): test_name, bstack11lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᅚ"): bstack1l111l1l11_opy_, bstack11lll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᅛ"): bstack1ll11ll11l_opy_}
        bstack1l11l11ll1_opy_ = []
        bstack1l111llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᅜ"))
        if os.path.exists(bstack1l111llll1_opy_):
            with open(bstack1l111llll1_opy_) as f:
                bstack1l11l11ll1_opy_ = json.load(f)
        bstack1l11l11ll1_opy_.append(bstack1ll11l111_opy_)
        with open(bstack1l111llll1_opy_, bstack11lll1l_opy_ (u"ࠧࡸࠩᅝ")) as f:
            json.dump(bstack1l11l11ll1_opy_, f)
    else:
        bstack1ll11l111_opy_ = {bstack11lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᅞ"): test_name, bstack11lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᅟ"): bstack1l111l1l11_opy_, bstack11lll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᅠ"): str(multiprocessing.current_process().name)}
        if bstack11lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᅡ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11l111_opy_)
  except Exception as e:
      logger.warn(bstack11lll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᅢ").format(e))
def bstack1ll11l111l_opy_(error_message, test_name, index, logger):
  try:
    bstack1l11l1l1ll_opy_ = []
    bstack1ll11l111_opy_ = {bstack11lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᅣ"): test_name, bstack11lll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᅤ"): error_message, bstack11lll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᅥ"): index}
    bstack1l11ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᅦ"))
    if os.path.exists(bstack1l11ll1111_opy_):
        with open(bstack1l11ll1111_opy_) as f:
            bstack1l11l1l1ll_opy_ = json.load(f)
    bstack1l11l1l1ll_opy_.append(bstack1ll11l111_opy_)
    with open(bstack1l11ll1111_opy_, bstack11lll1l_opy_ (u"ࠪࡻࠬᅧ")) as f:
        json.dump(bstack1l11l1l1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack11lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᅨ").format(e))
def bstack1l1ll11l_opy_(bstack11l11l1l1_opy_, name, logger):
  try:
    bstack1ll11l111_opy_ = {bstack11lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᅩ"): name, bstack11lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᅪ"): bstack11l11l1l1_opy_, bstack11lll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᅫ"): str(threading.current_thread()._name)}
    return bstack1ll11l111_opy_
  except Exception as e:
    logger.warn(bstack11lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᅬ").format(e))
  return