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
from bstack_utils.constants import bstack1l111ll1l1_opy_, bstack1l1ll11l_opy_, bstack11ll1l1l1_opy_, bstack1ll11l1l_opy_
from bstack_utils.messages import bstack11lll1ll1_opy_, bstack1llll111_opy_
from bstack_utils.proxy import bstack1ll11ll111_opy_, bstack1l11111l_opy_
bstack1l11l1ll_opy_ = Config.get_instance()
def bstack1l11l1ll11_opy_(config):
    return config[bstack1l1ll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨံ")]
def bstack1l11l1lll1_opy_(config):
    return config[bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻ့ࠪ")]
def bstack1l11l1l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1l1111l111_opy_(obj):
    values = []
    bstack11lll1ll1l_opy_ = re.compile(bstack1l1ll1l_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧး"), re.I)
    for key in obj.keys():
        if bstack11lll1ll1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l11ll11l1_opy_(config):
    tags = []
    tags.extend(bstack1l1111l111_opy_(os.environ))
    tags.extend(bstack1l1111l111_opy_(config))
    return tags
def bstack1l111l111l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l111111ll_opy_(bstack11llll1ll1_opy_):
    if not bstack11llll1ll1_opy_:
        return bstack1l1ll1l_opy_ (u"္ࠩࠪ")
    return bstack1l1ll1l_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿ်ࠬࠦ").format(bstack11llll1ll1_opy_.name, bstack11llll1ll1_opy_.email)
def bstack1l11ll1l1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11lllll1ll_opy_ = repo.common_dir
        info = {
            bstack1l1ll1l_opy_ (u"ࠦࡸ࡮ࡡࠣျ"): repo.head.commit.hexsha,
            bstack1l1ll1l_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣြ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨွ"): repo.active_branch.name,
            bstack1l1ll1l_opy_ (u"ࠢࡵࡣࡪࠦှ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1ll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦဿ"): bstack1l111111ll_opy_(repo.head.commit.committer),
            bstack1l1ll1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥ၀"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1ll1l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥ၁"): bstack1l111111ll_opy_(repo.head.commit.author),
            bstack1l1ll1l_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤ၂"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1ll1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ၃"): repo.head.commit.message,
            bstack1l1ll1l_opy_ (u"ࠨࡲࡰࡱࡷࠦ၄"): repo.git.rev_parse(bstack1l1ll1l_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤ၅")),
            bstack1l1ll1l_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ၆"): bstack11lllll1ll_opy_,
            bstack1l1ll1l_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ၇"): subprocess.check_output([bstack1l1ll1l_opy_ (u"ࠥ࡫࡮ࡺࠢ၈"), bstack1l1ll1l_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢ၉"), bstack1l1ll1l_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣ၊")]).strip().decode(
                bstack1l1ll1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ။")),
            bstack1l1ll1l_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤ၌"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1ll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥ၍"): repo.git.rev_list(
                bstack1l1ll1l_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤ၎").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11llllll1l_opy_ = []
        for remote in remotes:
            bstack1l11111ll1_opy_ = {
                bstack1l1ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ၏"): remote.name,
                bstack1l1ll1l_opy_ (u"ࠦࡺࡸ࡬ࠣၐ"): remote.url,
            }
            bstack11llllll1l_opy_.append(bstack1l11111ll1_opy_)
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥၑ"): bstack1l1ll1l_opy_ (u"ࠨࡧࡪࡶࠥၒ"),
            **info,
            bstack1l1ll1l_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣၓ"): bstack11llllll1l_opy_
        }
    except Exception as err:
        print(bstack1l1ll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦၔ").format(err))
        return {}
def bstack1ll1l1l11_opy_():
    env = os.environ
    if (bstack1l1ll1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢၕ") in env and len(env[bstack1l1ll1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣၖ")]) > 0) or (
            bstack1l1ll1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥၗ") in env and len(env[bstack1l1ll1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦၘ")]) > 0):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦၙ"): bstack1l1ll1l_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣၚ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦၛ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧၜ")),
            bstack1l1ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧၝ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨၞ")),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦၟ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧၠ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠢࡄࡋࠥၡ")) == bstack1l1ll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨၢ") and bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦၣ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣၤ"): bstack1l1ll1l_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨၥ"),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣၦ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤၧ")),
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤၨ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧၩ")),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣၪ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨၫ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡏࠢၬ")) == bstack1l1ll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥၭ") and bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨၮ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧၯ"): bstack1l1ll1l_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦၰ"),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧၱ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥၲ")),
            bstack1l1ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨၳ"): env.get(bstack1l1ll1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢၴ")),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧၵ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨၶ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡌࠦၷ")) == bstack1l1ll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢၸ") and env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦၹ")) == bstack1l1ll1l_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨၺ"):
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥၻ"): bstack1l1ll1l_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣၼ"),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥၽ"): None,
            bstack1l1ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥၾ"): None,
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣၿ"): None
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨႀ")) and env.get(bstack1l1ll1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢႁ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥႂ"): bstack1l1ll1l_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤႃ"),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥႄ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨႅ")),
            bstack1l1ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦႆ"): None,
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤႇ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨႈ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡉࠣႉ")) == bstack1l1ll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦႊ") and bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨႋ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨႌ"): bstack1l1ll1l_opy_ (u"ࠤࡇࡶࡴࡴࡥႍࠣ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨႎ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢႏ")),
            bstack1l1ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ႐"): None,
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ႑"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ႒"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡌࠦ႓")) == bstack1l1ll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ႔") and bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨ႕"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ႖"): bstack1l1ll1l_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣ႗"),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ႘"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨ႙")),
            bstack1l1ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥႚ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢႛ")),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤႜ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢႝ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡉࠣ႞")) == bstack1l1ll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦ႟") and bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥႠ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨႡ"): bstack1l1ll1l_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤႢ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨႣ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣႤ")),
            bstack1l1ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢႥ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦႦ")),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨႧ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦႨ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡍࠧႩ")) == bstack1l1ll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣႪ") and bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢႫ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥႬ"): bstack1l1ll1l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤႭ"),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥႮ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢႯ")),
            bstack1l1ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦႰ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧႱ")) or env.get(bstack1l1ll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢႲ")),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦႳ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣႴ"))
        }
    if bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤႵ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨႶ"): bstack1l1ll1l_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤႷ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨႸ"): bstack1l1ll1l_opy_ (u"ࠦࢀࢃࡻࡾࠤႹ").format(env.get(bstack1l1ll1l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨႺ")), env.get(bstack1l1ll1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭Ⴛ"))),
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤႼ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢႽ")),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣႾ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥႿ"))
        }
    if bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨჀ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥჁ"): bstack1l1ll1l_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣჂ"),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥჃ"): bstack1l1ll1l_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢჄ").format(env.get(bstack1l1ll1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨჅ")), env.get(bstack1l1ll1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫ჆")), env.get(bstack1l1ll1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬჇ")), env.get(bstack1l1ll1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ჈"))),
            bstack1l1ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ჉"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ჊")),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ჋"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ჌"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦჍ")) and env.get(bstack1l1ll1l_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ჎")):
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ჏"): bstack1l1ll1l_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣა"),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥბ"): bstack1l1ll1l_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦგ").format(env.get(bstack1l1ll1l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬდ")), env.get(bstack1l1ll1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨე")), env.get(bstack1l1ll1l_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫვ"))),
            bstack1l1ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢზ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨთ")),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨი"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣკ"))
        }
    if any([env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢლ")), env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤმ")), env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣნ"))]):
        return {
            bstack1l1ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥო"): bstack1l1ll1l_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨპ"),
            bstack1l1ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥჟ"): env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢრ")),
            bstack1l1ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦს"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣტ")),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥუ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥფ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦქ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧღ"): bstack1l1ll1l_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣყ"),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧშ"): env.get(bstack1l1ll1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧჩ")),
            bstack1l1ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨც"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦძ")),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧწ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧჭ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤხ")) or env.get(bstack1l1ll1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦჯ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣჰ"): bstack1l1ll1l_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧჱ"),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣჲ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥჳ")),
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤჴ"): bstack1l1ll1l_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣჵ") if env.get(bstack1l1ll1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦჶ")) else None,
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤჷ"): env.get(bstack1l1ll1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤჸ"))
        }
    if any([env.get(bstack1l1ll1l_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥჹ")), env.get(bstack1l1ll1l_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢჺ")), env.get(bstack1l1ll1l_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ჻"))]):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨჼ"): bstack1l1ll1l_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣჽ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨჾ"): None,
            bstack1l1ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨჿ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤᄀ")),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᄁ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᄂ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦᄃ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄄ"): bstack1l1ll1l_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨᄅ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄆ"): env.get(bstack1l1ll1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᄇ")),
            bstack1l1ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄈ"): bstack1l1ll1l_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣᄉ").format(env.get(bstack1l1ll1l_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫᄊ"))) if env.get(bstack1l1ll1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧᄋ")) else None,
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᄌ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᄍ"))
        }
    if bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨᄎ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄏ"): bstack1l1ll1l_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣᄐ"),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᄑ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨᄒ")),
            bstack1l1ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᄓ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢᄔ")),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᄕ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᄖ"))
        }
    if bstack1l1l111ll1_opy_(env.get(bstack1l1ll1l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣᄗ"))):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᄘ"): bstack1l1ll1l_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥᄙ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᄚ"): bstack1l1ll1l_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧᄛ").format(env.get(bstack1l1ll1l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩᄜ")), env.get(bstack1l1ll1l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪᄝ")), env.get(bstack1l1ll1l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧᄞ"))),
            bstack1l1ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᄟ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦᄠ")),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᄡ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦᄢ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡉࠣᄣ")) == bstack1l1ll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᄤ") and env.get(bstack1l1ll1l_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢᄥ")) == bstack1l1ll1l_opy_ (u"ࠣ࠳ࠥᄦ"):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄧ"): bstack1l1ll1l_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥᄨ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄩ"): bstack1l1ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣᄪ").format(env.get(bstack1l1ll1l_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪᄫ"))),
            bstack1l1ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᄬ"): None,
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᄭ"): None,
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᄮ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᄯ"): bstack1l1ll1l_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨᄰ"),
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᄱ"): None,
            bstack1l1ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄲ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣᄳ")),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᄴ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᄵ"))
        }
    if any([env.get(bstack1l1ll1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨᄶ")), env.get(bstack1l1ll1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦᄷ")), env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥᄸ")), env.get(bstack1l1ll1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢᄹ"))]):
        return {
            bstack1l1ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᄺ"): bstack1l1ll1l_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦᄻ"),
            bstack1l1ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᄼ"): None,
            bstack1l1ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᄽ"): env.get(bstack1l1ll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᄾ")) or None,
            bstack1l1ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᄿ"): env.get(bstack1l1ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᅀ"), 0)
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᅁ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᅂ"): bstack1l1ll1l_opy_ (u"ࠤࡊࡳࡈࡊࠢᅃ"),
            bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅄ"): None,
            bstack1l1ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅅ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᅆ")),
            bstack1l1ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅇ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨᅈ"))
        }
    if env.get(bstack1l1ll1l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᅉ")):
        return {
            bstack1l1ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅊ"): bstack1l1ll1l_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨᅋ"),
            bstack1l1ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅌ"): env.get(bstack1l1ll1l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᅍ")),
            bstack1l1ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅎ"): env.get(bstack1l1ll1l_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᅏ")),
            bstack1l1ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅐ"): env.get(bstack1l1ll1l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᅑ"))
        }
    return {bstack1l1ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅒ"): None}
def get_host_info():
    return {
        bstack1l1ll1l_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨᅓ"): platform.node(),
        bstack1l1ll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢᅔ"): platform.system(),
        bstack1l1ll1l_opy_ (u"ࠨࡴࡺࡲࡨࠦᅕ"): platform.machine(),
        bstack1l1ll1l_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᅖ"): platform.version(),
        bstack1l1ll1l_opy_ (u"ࠣࡣࡵࡧ࡭ࠨᅗ"): platform.architecture()[0]
    }
def bstack1111ll11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l11l1l111_opy_():
    if bstack1l11l1ll_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪᅘ")):
        return bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᅙ")
    return bstack1l1ll1l_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪᅚ")
def bstack1l11l1l1l1_opy_(driver):
    info = {
        bstack1l1ll1l_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᅛ"): driver.capabilities,
        bstack1l1ll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪᅜ"): driver.session_id,
        bstack1l1ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᅝ"): driver.capabilities.get(bstack1l1ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᅞ"), None),
        bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᅟ"): driver.capabilities.get(bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᅠ"), None),
        bstack1l1ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭ᅡ"): driver.capabilities.get(bstack1l1ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᅢ"), None),
    }
    if bstack1l11l1l111_opy_() == bstack1l1ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᅣ"):
        info[bstack1l1ll1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᅤ")] = bstack1l1ll1l_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᅥ") if bstack1ll11111ll_opy_() else bstack1l1ll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᅦ")
    return info
def bstack1ll11111ll_opy_():
    if bstack1l11l1ll_opy_.get_property(bstack1l1ll1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᅧ")):
        return True
    if bstack1l1l111ll1_opy_(os.environ.get(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᅨ"), None)):
        return True
    return False
def bstack1111ll11l_opy_(bstack1l111111l1_opy_, url, data, config):
    headers = config.get(bstack1l1ll1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᅩ"), None)
    proxies = bstack1ll11ll111_opy_(config, url)
    auth = config.get(bstack1l1ll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᅪ"), None)
    response = requests.request(
            bstack1l111111l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack111lllll_opy_(bstack1111l11ll_opy_, size):
    bstack1lll111ll_opy_ = []
    while len(bstack1111l11ll_opy_) > size:
        bstack1ll1lll111_opy_ = bstack1111l11ll_opy_[:size]
        bstack1lll111ll_opy_.append(bstack1ll1lll111_opy_)
        bstack1111l11ll_opy_ = bstack1111l11ll_opy_[size:]
    bstack1lll111ll_opy_.append(bstack1111l11ll_opy_)
    return bstack1lll111ll_opy_
def bstack1l11ll1l11_opy_(message, bstack11llll11l1_opy_=False):
    os.write(1, bytes(message, bstack1l1ll1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᅫ")))
    os.write(1, bytes(bstack1l1ll1l_opy_ (u"ࠨ࡞ࡱࠫᅬ"), bstack1l1ll1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᅭ")))
    if bstack11llll11l1_opy_:
        with open(bstack1l1ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩᅮ") + os.environ[bstack1l1ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᅯ")] + bstack1l1ll1l_opy_ (u"ࠬ࠴࡬ࡰࡩࠪᅰ"), bstack1l1ll1l_opy_ (u"࠭ࡡࠨᅱ")) as f:
            f.write(message + bstack1l1ll1l_opy_ (u"ࠧ࡝ࡰࠪᅲ"))
def bstack11lllll11l_opy_():
    return os.environ[bstack1l1ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᅳ")].lower() == bstack1l1ll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᅴ")
def bstack1l1l1l11l_opy_(bstack1l11llll11_opy_):
    return bstack1l1ll1l_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᅵ").format(bstack1l111ll1l1_opy_, bstack1l11llll11_opy_)
def bstack111lll1l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1l1ll1l_opy_ (u"ࠫ࡟࠭ᅶ")
def bstack1l1l1l11ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1ll1l_opy_ (u"ࠬࡠࠧᅷ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1ll1l_opy_ (u"࡚࠭ࠨᅸ")))).total_seconds() * 1000
def bstack1l1111lll1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1l1ll1l_opy_ (u"࡛ࠧࠩᅹ")
def bstack1l11111l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᅺ")
    else:
        return bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᅻ")
def bstack1l1l111ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1ll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᅼ")
def bstack11lll1l1ll_opy_(val):
    return val.__str__().lower() == bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᅽ")
def bstack1l11lll1l1_opy_(bstack11llll111l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11llll111l_opy_ as e:
                print(bstack1l1ll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᅾ").format(func.__name__, bstack11llll111l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1l11111lll_opy_(bstack11llll1l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11llll1l11_opy_(cls, *args, **kwargs)
            except bstack11llll111l_opy_ as e:
                print(bstack1l1ll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᅿ").format(bstack11llll1l11_opy_.__name__, bstack11llll111l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1l11111lll_opy_
    else:
        return decorator
def bstack1ll1ll11l1_opy_(bstack1l1ll1llll_opy_):
    if bstack1l1ll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᆀ") in bstack1l1ll1llll_opy_ and bstack11lll1l1ll_opy_(bstack1l1ll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᆁ")]):
        return False
    if bstack1l1ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᆂ") in bstack1l1ll1llll_opy_ and bstack11lll1l1ll_opy_(bstack1l1ll1llll_opy_[bstack1l1ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᆃ")]):
        return False
    return True
def bstack1ll111l11_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1lllll1l1l_opy_(hub_url):
    if bstack111l111l_opy_() <= version.parse(bstack1l1ll1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫᆄ")):
        if hub_url != bstack1l1ll1l_opy_ (u"ࠬ࠭ᆅ"):
            return bstack1l1ll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᆆ") + hub_url + bstack1l1ll1l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᆇ")
        return bstack11ll1l1l1_opy_
    if hub_url != bstack1l1ll1l_opy_ (u"ࠨࠩᆈ"):
        return bstack1l1ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᆉ") + hub_url + bstack1l1ll1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᆊ")
    return bstack1ll11l1l_opy_
def bstack1l111l11l1_opy_():
    return isinstance(os.getenv(bstack1l1ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪᆋ")), str)
def bstack11l11l1l1_opy_(url):
    return urlparse(url).hostname
def bstack111l1lll1_opy_(hostname):
    for bstack11l1l1l11_opy_ in bstack1l1ll11l_opy_:
        regex = re.compile(bstack11l1l1l11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11lll1llll_opy_(bstack11llll11ll_opy_, file_name, logger):
    bstack1ll1111l11_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1l_opy_ (u"ࠬࢄࠧᆌ")), bstack11llll11ll_opy_)
    try:
        if not os.path.exists(bstack1ll1111l11_opy_):
            os.makedirs(bstack1ll1111l11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1ll1l_opy_ (u"࠭ࡾࠨᆍ")), bstack11llll11ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1ll1l_opy_ (u"ࠧࡸࠩᆎ")):
                pass
            with open(file_path, bstack1l1ll1l_opy_ (u"ࠣࡹ࠮ࠦᆏ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11lll1ll1_opy_.format(str(e)))
def bstack1l1111l1ll_opy_(file_name, key, value, logger):
    file_path = bstack11lll1llll_opy_(bstack1l1ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᆐ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l11lll1_opy_ = json.load(open(file_path, bstack1l1ll1l_opy_ (u"ࠪࡶࡧ࠭ᆑ")))
        else:
            bstack11l11lll1_opy_ = {}
        bstack11l11lll1_opy_[key] = value
        with open(file_path, bstack1l1ll1l_opy_ (u"ࠦࡼ࠱ࠢᆒ")) as outfile:
            json.dump(bstack11l11lll1_opy_, outfile)
def bstack1l11l1111_opy_(file_name, logger):
    file_path = bstack11lll1llll_opy_(bstack1l1ll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᆓ"), file_name, logger)
    bstack11l11lll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1ll1l_opy_ (u"࠭ࡲࠨᆔ")) as bstack1ll111l1_opy_:
            bstack11l11lll1_opy_ = json.load(bstack1ll111l1_opy_)
    return bstack11l11lll1_opy_
def bstack111l11l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1ll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫᆕ") + file_path + bstack1l1ll1l_opy_ (u"ࠨࠢࠪᆖ") + str(e))
def bstack111l111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1ll1l_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦᆗ")
def bstack11l1l1ll1_opy_(config):
    if bstack1l1ll1l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᆘ") in config:
        del (config[bstack1l1ll1l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᆙ")])
        return False
    if bstack111l111l_opy_() < version.parse(bstack1l1ll1l_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫᆚ")):
        return False
    if bstack111l111l_opy_() >= version.parse(bstack1l1ll1l_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬᆛ")):
        return True
    if bstack1l1ll1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᆜ") in config and config[bstack1l1ll1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᆝ")] is False:
        return False
    else:
        return True
def bstack1l1l1llll_opy_(args_list, bstack11llllllll_opy_):
    index = -1
    for value in bstack11llllllll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1111l1l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1111l1l1_opy_ = bstack1l1111l1l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᆞ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᆟ"), exception=exception)
    def bstack1l1l1l111l_opy_(self):
        if self.result != bstack1l1ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᆠ"):
            return None
        if bstack1l1ll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᆡ") in self.exception_type:
            return bstack1l1ll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᆢ")
        return bstack1l1ll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᆣ")
    def bstack1l1l11llll_opy_(self):
        if self.result != bstack1l1ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᆤ"):
            return None
        if self.bstack1l1111l1l1_opy_:
            return self.bstack1l1111l1l1_opy_
        return bstack11lll1ll11_opy_(self.exception)
def bstack11lll1ll11_opy_(exc):
    return traceback.format_exception(exc)
def bstack11llllll11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l1lll11_opy_(object, key, default_value):
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1111l11l1_opy_(config, logger):
    try:
        import playwright
        bstack1l1111l11l_opy_ = playwright.__file__
        bstack1l111l1111_opy_ = os.path.split(bstack1l1111l11l_opy_)
        bstack11llll1l1l_opy_ = bstack1l111l1111_opy_[0] + bstack1l1ll1l_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬᆥ")
        os.environ[bstack1l1ll1l_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ᆦ")] = bstack1l11111l_opy_(config)
        with open(bstack11llll1l1l_opy_, bstack1l1ll1l_opy_ (u"ࠫࡷ࠭ᆧ")) as f:
            bstack1lll111111_opy_ = f.read()
            bstack1l11111l1l_opy_ = bstack1l1ll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫᆨ")
            bstack11lll1lll1_opy_ = bstack1lll111111_opy_.find(bstack1l11111l1l_opy_)
            if bstack11lll1lll1_opy_ is -1:
              process = subprocess.Popen(bstack1l1ll1l_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥᆩ"), shell=True, cwd=bstack1l111l1111_opy_[0])
              process.wait()
              bstack11lllllll1_opy_ = bstack1l1ll1l_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧᆪ")
              bstack11lll1l1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧᆫ")
              bstack11lllll1l1_opy_ = bstack1lll111111_opy_.replace(bstack11lllllll1_opy_, bstack11lll1l1l1_opy_)
              with open(bstack11llll1l1l_opy_, bstack1l1ll1l_opy_ (u"ࠩࡺࠫᆬ")) as f:
                f.write(bstack11lllll1l1_opy_)
    except Exception as e:
        logger.error(bstack1llll111_opy_.format(str(e)))
def bstack1ll111l11l_opy_():
  try:
    bstack1l1111ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᆭ"))
    bstack1l11111111_opy_ = []
    if os.path.exists(bstack1l1111ll11_opy_):
      with open(bstack1l1111ll11_opy_) as f:
        bstack1l11111111_opy_ = json.load(f)
      os.remove(bstack1l1111ll11_opy_)
    return bstack1l11111111_opy_
  except:
    pass
  return []
def bstack1l11l111l_opy_(bstack1llllllll_opy_):
  try:
    bstack1l11111111_opy_ = []
    bstack1l1111ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᆮ"))
    if os.path.exists(bstack1l1111ll11_opy_):
      with open(bstack1l1111ll11_opy_) as f:
        bstack1l11111111_opy_ = json.load(f)
    bstack1l11111111_opy_.append(bstack1llllllll_opy_)
    with open(bstack1l1111ll11_opy_, bstack1l1ll1l_opy_ (u"ࠬࡽࠧᆯ")) as f:
        json.dump(bstack1l11111111_opy_, f)
  except:
    pass
def bstack1ll1l11lll_opy_(logger, bstack11llll1lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1ll1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᆰ"), bstack1l1ll1l_opy_ (u"ࠧࠨᆱ"))
    if test_name == bstack1l1ll1l_opy_ (u"ࠨࠩᆲ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1ll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨᆳ"), bstack1l1ll1l_opy_ (u"ࠪࠫᆴ"))
    bstack11lllll111_opy_ = bstack1l1ll1l_opy_ (u"ࠫ࠱ࠦࠧᆵ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11llll1lll_opy_:
        bstack1ll11lll11_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᆶ"), bstack1l1ll1l_opy_ (u"࠭࠰ࠨᆷ"))
        bstack1ll1l1l1l_opy_ = {bstack1l1ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᆸ"): test_name, bstack1l1ll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᆹ"): bstack11lllll111_opy_, bstack1l1ll1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᆺ"): bstack1ll11lll11_opy_}
        bstack1l1111ll1l_opy_ = []
        bstack1l1111llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᆻ"))
        if os.path.exists(bstack1l1111llll_opy_):
            with open(bstack1l1111llll_opy_) as f:
                bstack1l1111ll1l_opy_ = json.load(f)
        bstack1l1111ll1l_opy_.append(bstack1ll1l1l1l_opy_)
        with open(bstack1l1111llll_opy_, bstack1l1ll1l_opy_ (u"ࠫࡼ࠭ᆼ")) as f:
            json.dump(bstack1l1111ll1l_opy_, f)
    else:
        bstack1ll1l1l1l_opy_ = {bstack1l1ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᆽ"): test_name, bstack1l1ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᆾ"): bstack11lllll111_opy_, bstack1l1ll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᆿ"): str(multiprocessing.current_process().name)}
        if bstack1l1ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬᇀ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack1111llll1_opy_ = []
        multiprocessing.current_process().bstack1111llll1_opy_.append(bstack1ll1l1l1l_opy_)
  except Exception as e:
      logger.warn(bstack1l1ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᇁ").format(e))
def bstack1lll11ll_opy_(error_message, test_name, index, logger):
  try:
    bstack11llll1111_opy_ = []
    bstack1ll1l1l1l_opy_ = {bstack1l1ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᇂ"): test_name, bstack1l1ll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᇃ"): error_message, bstack1l1ll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᇄ"): index}
    bstack1l1111111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᇅ"))
    if os.path.exists(bstack1l1111111l_opy_):
        with open(bstack1l1111111l_opy_) as f:
            bstack11llll1111_opy_ = json.load(f)
    bstack11llll1111_opy_.append(bstack1ll1l1l1l_opy_)
    with open(bstack1l1111111l_opy_, bstack1l1ll1l_opy_ (u"ࠧࡸࠩᇆ")) as f:
        json.dump(bstack11llll1111_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1ll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᇇ").format(e))
def bstack1ll111l1ll_opy_(bstack1ll1lllll_opy_, name, logger):
  try:
    bstack1ll1l1l1l_opy_ = {bstack1l1ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᇈ"): name, bstack1l1ll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᇉ"): bstack1ll1lllll_opy_, bstack1l1ll1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᇊ"): str(threading.current_thread()._name)}
    return bstack1ll1l1l1l_opy_
  except Exception as e:
    logger.warn(bstack1l1ll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᇋ").format(e))
  return