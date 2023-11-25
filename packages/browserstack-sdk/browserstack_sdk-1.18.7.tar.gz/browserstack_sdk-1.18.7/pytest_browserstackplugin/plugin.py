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
import atexit
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack111l1l11_opy_, bstack1llll1111l_opy_, update, bstack1l11l1lll_opy_,
                                       bstack1111ll1l_opy_, bstack11ll11ll1_opy_, bstack1l1ll1l1_opy_, bstack111l1111l_opy_,
                                       bstack11ll11l1_opy_, bstack11111lll1_opy_, bstack1l1lll1lll_opy_, bstack1lll111111_opy_,
                                       bstack1ll111ll1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1l111ll1_opy_
from bstack_utils.constants import bstack1ll1111l_opy_, bstack1l1l1l1l_opy_, bstack1l1lll1l_opy_, bstack11llll111_opy_, \
    bstack1l1l11111_opy_
from bstack_utils.helper import bstack11lll111_opy_, bstack1l1l1llll_opy_, bstack1l11lll111_opy_, bstack11l1l1111_opy_, bstack1l111l1lll_opy_, \
    bstack1l11l111ll_opy_, bstack1ll1ll11_opy_, bstack111l11111_opy_, bstack1l11l1ll1l_opy_, bstack1ll1111111_opy_, Notset, \
    bstack1l111l1l_opy_, bstack1l11l1ll11_opy_, bstack1l111l1l1l_opy_, Result, bstack1l111lll11_opy_, bstack1l11lll1ll_opy_, bstack1l1l1l1lll_opy_, bstack11llll11l_opy_, bstack1ll11llll_opy_
from bstack_utils.bstack1l11111111_opy_ import bstack1l11111l11_opy_
from bstack_utils.messages import bstack11llll1l1_opy_, bstack1ll1l1ll1_opy_, bstack1ll11111l_opy_, bstack11l1l1lll_opy_, bstack1l1l11l1l_opy_, \
    bstack11l1l1l1l_opy_, bstack111l1ll11_opy_, bstack1llll111ll_opy_, bstack11111ll1l_opy_, bstack1llll11l1l_opy_, \
    bstack1ll111l111_opy_, bstack11ll1lll_opy_
from bstack_utils.proxy import bstack11lllll1l_opy_, bstack1ll11l1l1_opy_
from bstack_utils.bstack11lll11ll_opy_ import bstack11l1ll11l1_opy_, bstack11l1lll11l_opy_, bstack11l1ll1111_opy_, bstack11l1l1ll1l_opy_, \
    bstack11l1l1llll_opy_, bstack11l1l1ll11_opy_, bstack11l1lll111_opy_, bstack11l11l111_opy_, bstack11l1ll1l11_opy_
from bstack_utils.bstack11l11ll1ll_opy_ import bstack11l11lll11_opy_
from bstack_utils.bstack11l1ll1l1l_opy_ import bstack1llll1ll_opy_, bstack11l11ll11_opy_, bstack111ll1l1_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack11l111ll1l_opy_
from bstack_utils.bstack1ll1l1l11_opy_ import bstack111lll111_opy_
import bstack_utils.bstack1111llll1_opy_ as bstack1111l11ll_opy_
bstack11ll11ll_opy_ = None
bstack1111l111_opy_ = None
bstack1llll1ll1l_opy_ = None
bstack1ll1lll11l_opy_ = None
bstack1llll1l11_opy_ = None
bstack1ll1l11l1l_opy_ = None
bstack11ll1l11_opy_ = None
bstack1l1l1111_opy_ = None
bstack111ll1l11_opy_ = None
bstack1l1llll111_opy_ = None
bstack1lllll111l_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack11l11ll1_opy_ = bstack11lll1l_opy_ (u"ࠩࠪᎲ")
CONFIG = {}
bstack1l1lllll_opy_ = False
bstack1lll1l1l_opy_ = bstack11lll1l_opy_ (u"ࠪࠫᎳ")
bstack1l1ll11ll_opy_ = bstack11lll1l_opy_ (u"ࠫࠬᎴ")
bstack1l11llll1_opy_ = False
bstack1lll111ll_opy_ = []
bstack1ll11lll11_opy_ = bstack1l1l1l1l_opy_
bstack111l111l1l_opy_ = bstack11lll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᎵ")
bstack1111llll11_opy_ = False
bstack111l111l1_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll11lll11_opy_,
                    format=bstack11lll1l_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᎶ"),
                    datefmt=bstack11lll1l_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩᎷ"),
                    stream=sys.stdout)
store = {
    bstack11lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᎸ"): []
}
def bstack11lll1l11_opy_():
    global CONFIG
    global bstack1ll11lll11_opy_
    if bstack11lll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᎹ") in CONFIG:
        bstack1ll11lll11_opy_ = bstack1ll1111l_opy_[CONFIG[bstack11lll1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᎺ")]]
        logging.getLogger().setLevel(bstack1ll11lll11_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l1ll1l1_opy_ = {}
current_test_uuid = None
def bstack1l111llll_opy_(page, bstack11ll1111_opy_):
    try:
        page.evaluate(bstack11lll1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᎻ"),
                      bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᎼ") + json.dumps(
                          bstack11ll1111_opy_) + bstack11lll1l_opy_ (u"ࠨࡽࡾࠤᎽ"))
    except Exception as e:
        print(bstack11lll1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᎾ"), e)
def bstack11l111l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack11lll1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᎿ"), bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧᏀ") + json.dumps(
            message) + bstack11lll1l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭Ꮑ") + json.dumps(level) + bstack11lll1l_opy_ (u"ࠫࢂࢃࠧᏂ"))
    except Exception as e:
        print(bstack11lll1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣᏃ"), e)
def bstack11l1l1ll_opy_(page, status, message=bstack11lll1l_opy_ (u"ࠨࠢᏄ")):
    try:
        if (status == bstack11lll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᏅ")):
            page.evaluate(bstack11lll1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᏆ"),
                          bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠪᏇ") + json.dumps(
                              bstack11lll1l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࠧᏈ") + str(message)) + bstack11lll1l_opy_ (u"ࠫ࠱ࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨᏉ") + json.dumps(status) + bstack11lll1l_opy_ (u"ࠧࢃࡽࠣᏊ"))
        else:
            page.evaluate(bstack11lll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᏋ"),
                          bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨᏌ") + json.dumps(
                              status) + bstack11lll1l_opy_ (u"ࠣࡿࢀࠦᏍ"))
    except Exception as e:
        print(bstack11lll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨᏎ"), e)
def pytest_configure(config):
    config.args = bstack111lll111_opy_.bstack111l1lllll_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack111l11lll1_opy_ = item.config.getoption(bstack11lll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᏏ"))
    plugins = item.config.getoption(bstack11lll1l_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᏐ"))
    report = outcome.get_result()
    bstack111l1111l1_opy_(item, call, report)
    if bstack11lll1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᏑ") not in plugins or bstack1ll1111111_opy_():
        return
    summary = []
    driver = getattr(item, bstack11lll1l_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᏒ"), None)
    page = getattr(item, bstack11lll1l_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᏓ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack111l11ll11_opy_(item, report, summary, bstack111l11lll1_opy_)
    if (page is not None):
        bstack111l1ll1ll_opy_(item, report, summary, bstack111l11lll1_opy_)
def bstack111l11ll11_opy_(item, report, summary, bstack111l11lll1_opy_):
    if report.when in [bstack11lll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᏔ"), bstack11lll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᏕ")]:
        return
    if not bstack1l11lll111_opy_():
        return
    try:
        if (str(bstack111l11lll1_opy_).lower() != bstack11lll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᏖ")):
            item._driver.execute_script(
                bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩᏗ") + json.dumps(
                    report.nodeid) + bstack11lll1l_opy_ (u"ࠬࢃࡽࠨᏘ"))
        os.environ[bstack11lll1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᏙ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11lll1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢᏚ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lll1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᏛ")))
    bstack1lll11l11_opy_ = bstack11lll1l_opy_ (u"ࠤࠥᏜ")
    bstack11l1ll1l11_opy_(report)
    if not passed:
        try:
            bstack1lll11l11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11lll1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᏝ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll11l11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11lll1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᏞ")))
        bstack1lll11l11_opy_ = bstack11lll1l_opy_ (u"ࠧࠨᏟ")
        if not passed:
            try:
                bstack1lll11l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lll1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᏠ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll11l11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᏡ")
                    + json.dumps(bstack11lll1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤᏢ"))
                    + bstack11lll1l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᏣ")
                )
            else:
                item._driver.execute_script(
                    bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨᏤ")
                    + json.dumps(str(bstack1lll11l11_opy_))
                    + bstack11lll1l_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᏥ")
                )
        except Exception as e:
            summary.append(bstack11lll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥᏦ").format(e))
def bstack111l1l1111_opy_(test_name, error_message):
    try:
        bstack111l11l11l_opy_ = []
        bstack1ll11ll11l_opy_ = os.environ.get(bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮷ"), bstack11lll1l_opy_ (u"ࠧ࠱ࠩᏨ"))
        bstack1ll11l111_opy_ = {bstack11lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ꮹ"): test_name, bstack11lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᏪ"): error_message, bstack11lll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᏫ"): bstack1ll11ll11l_opy_}
        bstack111l1l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᏬ"))
        if os.path.exists(bstack111l1l111l_opy_):
            with open(bstack111l1l111l_opy_) as f:
                bstack111l11l11l_opy_ = json.load(f)
        bstack111l11l11l_opy_.append(bstack1ll11l111_opy_)
        with open(bstack111l1l111l_opy_, bstack11lll1l_opy_ (u"ࠬࡽࠧᏭ")) as f:
            json.dump(bstack111l11l11l_opy_, f)
    except Exception as e:
        logger.debug(bstack11lll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫᏮ") + str(e))
def bstack111l1ll1ll_opy_(item, report, summary, bstack111l11lll1_opy_):
    if report.when in [bstack11lll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᏯ"), bstack11lll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᏰ")]:
        return
    if (str(bstack111l11lll1_opy_).lower() != bstack11lll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᏱ")):
        bstack1l111llll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lll1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᏲ")))
    bstack1lll11l11_opy_ = bstack11lll1l_opy_ (u"ࠦࠧᏳ")
    bstack11l1ll1l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll11l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᏴ").format(e)
                )
        try:
            if passed:
                bstack11l1l1ll_opy_(item._page, bstack11lll1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᏵ"))
            else:
                error_message = bstack11lll1l_opy_ (u"ࠧࠨ᏶")
                if bstack1lll11l11_opy_:
                    bstack11l111l1l_opy_(item._page, str(bstack1lll11l11_opy_), bstack11lll1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ᏷"))
                    bstack11l1l1ll_opy_(item._page, bstack11lll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᏸ"), str(bstack1lll11l11_opy_))
                    error_message = str(bstack1lll11l11_opy_)
                else:
                    bstack11l1l1ll_opy_(item._page, bstack11lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᏹ"))
                bstack111l1l1111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11lll1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀ࠶ࡽࠣᏺ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11lll1l_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᏻ"), default=bstack11lll1l_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᏼ"), help=bstack11lll1l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᏽ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11lll1l_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥ᏾"), action=bstack11lll1l_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣ᏿"), default=bstack11lll1l_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥ᐀"),
                         help=bstack11lll1l_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᐁ"))
def bstack111l11l111_opy_(log):
    if not (log[bstack11lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᐂ")] and log[bstack11lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᐃ")].strip()):
        return
    active = bstack111l1lll1l_opy_()
    log = {
        bstack11lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᐄ"): log[bstack11lll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᐅ")],
        bstack11lll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᐆ"): datetime.datetime.utcnow().isoformat() + bstack11lll1l_opy_ (u"ࠪ࡞ࠬᐇ"),
        bstack11lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐈ"): log[bstack11lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᐉ")],
    }
    if active:
        if active[bstack11lll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᐊ")] == bstack11lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᐋ"):
            log[bstack11lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᐌ")] = active[bstack11lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᐍ")]
        elif active[bstack11lll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᐎ")] == bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᐏ"):
            log[bstack11lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᐐ")] = active[bstack11lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᐑ")]
    bstack111lll111_opy_.bstack111ll1l111_opy_([log])
def bstack111l1lll1l_opy_():
    if len(store[bstack11lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᐒ")]) > 0 and store[bstack11lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᐓ")][-1]:
        return {
            bstack11lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᐔ"): bstack11lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᐕ"),
            bstack11lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᐖ"): store[bstack11lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᐗ")][-1]
        }
    if store.get(bstack11lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᐘ"), None):
        return {
            bstack11lll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᐙ"): bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᐚ"),
            bstack11lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᐛ"): store[bstack11lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᐜ")]
        }
    return None
bstack111l1l1l1l_opy_ = bstack1l1l111ll1_opy_(bstack111l11l111_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1111llll11_opy_
        if bstack1111llll11_opy_:
            driver = getattr(item, bstack11lll1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᐝ"), None)
            bstack11l11ll1l_opy_ = bstack1111l11ll_opy_.bstack1lll11l1l_opy_(CONFIG, bstack1l11l111ll_opy_(item.own_markers))
            item._a11y_started = bstack1111l11ll_opy_.bstack1lll1lll1l_opy_(driver, bstack11l11ll1l_opy_)
        if not bstack111lll111_opy_.on() or bstack111l111l1l_opy_ != bstack11lll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᐞ"):
            return
        global current_test_uuid, bstack111l1l1l1l_opy_
        bstack111l1l1l1l_opy_.start()
        bstack1111ll1ll1_opy_ = {
            bstack11lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᐟ"): uuid4().__str__(),
            bstack11lll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᐠ"): datetime.datetime.utcnow().isoformat() + bstack11lll1l_opy_ (u"ࠨ࡜ࠪᐡ")
        }
        current_test_uuid = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᐢ")]
        store[bstack11lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᐣ")] = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᐤ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l1ll1l1_opy_[item.nodeid] = {**_111l1ll1l1_opy_[item.nodeid], **bstack1111ll1ll1_opy_}
        bstack1111llll1l_opy_(item, _111l1ll1l1_opy_[item.nodeid], bstack11lll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᐥ"))
    except Exception as err:
        print(bstack11lll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨᐦ"), str(err))
def pytest_runtest_setup(item):
    if bstack1l11l1ll1l_opy_():
        atexit.register(bstack111l1111_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11l1ll11l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᐧ")
    try:
        if not bstack111lll111_opy_.on():
            return
        bstack111l1l1l1l_opy_.start()
        uuid = uuid4().__str__()
        bstack1111ll1ll1_opy_ = {
            bstack11lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᐨ"): uuid,
            bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᐩ"): datetime.datetime.utcnow().isoformat() + bstack11lll1l_opy_ (u"ࠪ࡞ࠬᐪ"),
            bstack11lll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᐫ"): bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᐬ"),
            bstack11lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᐭ"): bstack11lll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᐮ"),
            bstack11lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᐯ"): bstack11lll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᐰ")
        }
        threading.current_thread().bstack111l1ll11l_opy_ = uuid
        store[bstack11lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᐱ")] = item
        store[bstack11lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᐲ")] = [uuid]
        if not _111l1ll1l1_opy_.get(item.nodeid, None):
            _111l1ll1l1_opy_[item.nodeid] = {bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᐳ"): [], bstack11lll1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᐴ"): []}
        _111l1ll1l1_opy_[item.nodeid][bstack11lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᐵ")].append(bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᐶ")])
        _111l1ll1l1_opy_[item.nodeid + bstack11lll1l_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩᐷ")] = bstack1111ll1ll1_opy_
        bstack111l111lll_opy_(item, bstack1111ll1ll1_opy_, bstack11lll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᐸ"))
    except Exception as err:
        print(bstack11lll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᐹ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack111l111l1_opy_
        if getattr(item, bstack11lll1l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᐺ"), False):
            logger.info(bstack11lll1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨᐻ"))
            driver = getattr(item, bstack11lll1l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᐼ"), None)
            bstack1l1l1ll1ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1111l11ll_opy_.bstack11lll11l1_opy_(driver, bstack1l1l1ll1ll_opy_, item.name, item.module.__name__, item.path, bstack111l111l1_opy_)
        if not bstack111lll111_opy_.on():
            return
        bstack1111ll1ll1_opy_ = {
            bstack11lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᐽ"): uuid4().__str__(),
            bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᐾ"): datetime.datetime.utcnow().isoformat() + bstack11lll1l_opy_ (u"ࠪ࡞ࠬᐿ"),
            bstack11lll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᑀ"): bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᑁ"),
            bstack11lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᑂ"): bstack11lll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᑃ"),
            bstack11lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᑄ"): bstack11lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᑅ")
        }
        _111l1ll1l1_opy_[item.nodeid + bstack11lll1l_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᑆ")] = bstack1111ll1ll1_opy_
        bstack111l111lll_opy_(item, bstack1111ll1ll1_opy_, bstack11lll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᑇ"))
    except Exception as err:
        print(bstack11lll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫᑈ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack111lll111_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack11l1l1ll1l_opy_(fixturedef.argname):
        store[bstack11lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᑉ")] = request.node
    elif bstack11l1l1llll_opy_(fixturedef.argname):
        store[bstack11lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᑊ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑋ"): fixturedef.argname,
            bstack11lll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᑌ"): bstack1l111l1lll_opy_(outcome),
            bstack11lll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᑍ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack111l11ll1l_opy_ = store[bstack11lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᑎ")]
        if not _111l1ll1l1_opy_.get(bstack111l11ll1l_opy_.nodeid, None):
            _111l1ll1l1_opy_[bstack111l11ll1l_opy_.nodeid] = {bstack11lll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᑏ"): []}
        _111l1ll1l1_opy_[bstack111l11ll1l_opy_.nodeid][bstack11lll1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᑐ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᑑ"), str(err))
if bstack1ll1111111_opy_() and bstack111lll111_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _111l1ll1l1_opy_[request.node.nodeid][bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᑒ")].bstack11l1111l1l_opy_(id(step))
        except Exception as err:
            print(bstack11lll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᑓ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _111l1ll1l1_opy_[request.node.nodeid][bstack11lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᑔ")].bstack11l111lll1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11lll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᑕ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack111lllll1l_opy_: bstack11l111ll1l_opy_ = _111l1ll1l1_opy_[request.node.nodeid][bstack11lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᑖ")]
            bstack111lllll1l_opy_.bstack11l111lll1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11lll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᑗ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111l111l1l_opy_
        try:
            if not bstack111lll111_opy_.on() or bstack111l111l1l_opy_ != bstack11lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᑘ"):
                return
            global bstack111l1l1l1l_opy_
            bstack111l1l1l1l_opy_.start()
            if not _111l1ll1l1_opy_.get(request.node.nodeid, None):
                _111l1ll1l1_opy_[request.node.nodeid] = {}
            bstack111lllll1l_opy_ = bstack11l111ll1l_opy_.bstack11l111l1l1_opy_(
                scenario, feature, request.node,
                name=bstack11l1l1ll11_opy_(request.node, scenario),
                bstack11l11l11l1_opy_=bstack11l1l1111_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11lll1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᑙ"),
                tags=bstack11l1lll111_opy_(feature, scenario)
            )
            _111l1ll1l1_opy_[request.node.nodeid][bstack11lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᑚ")] = bstack111lllll1l_opy_
            bstack111l111ll1_opy_(bstack111lllll1l_opy_.uuid)
            bstack111lll111_opy_.bstack111ll1lll1_opy_(bstack11lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑛ"), bstack111lllll1l_opy_)
        except Exception as err:
            print(bstack11lll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᑜ"), str(err))
def bstack111l1l1ll1_opy_(bstack111l1l11l1_opy_):
    if bstack111l1l11l1_opy_ in store[bstack11lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᑝ")]:
        store[bstack11lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᑞ")].remove(bstack111l1l11l1_opy_)
def bstack111l111ll1_opy_(bstack111l1l1lll_opy_):
    store[bstack11lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᑟ")] = bstack111l1l1lll_opy_
    threading.current_thread().current_test_uuid = bstack111l1l1lll_opy_
@bstack111lll111_opy_.bstack111lll1lll_opy_
def bstack111l1111l1_opy_(item, call, report):
    global bstack111l111l1l_opy_
    try:
        if report.when == bstack11lll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᑠ"):
            bstack111l1l1l1l_opy_.reset()
        if report.when == bstack11lll1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᑡ"):
            if bstack111l111l1l_opy_ == bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᑢ"):
                _111l1ll1l1_opy_[item.nodeid][bstack11lll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᑣ")] = bstack1l111lll11_opy_(report.stop)
                bstack1111llll1l_opy_(item, _111l1ll1l1_opy_[item.nodeid], bstack11lll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᑤ"), report, call)
                store[bstack11lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᑥ")] = None
            elif bstack111l111l1l_opy_ == bstack11lll1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᑦ"):
                bstack111lllll1l_opy_ = _111l1ll1l1_opy_[item.nodeid][bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᑧ")]
                bstack111lllll1l_opy_.set(hooks=_111l1ll1l1_opy_[item.nodeid].get(bstack11lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᑨ"), []))
                exception, bstack1l11l1l111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11l1l111_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack111lllll1l_opy_.stop(time=bstack1l111lll11_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l11l1l111_opy_=bstack1l11l1l111_opy_))
                bstack111lll111_opy_.bstack111ll1lll1_opy_(bstack11lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᑩ"), _111l1ll1l1_opy_[item.nodeid][bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᑪ")])
        elif report.when in [bstack11lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᑫ"), bstack11lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᑬ")]:
            bstack1111lllll1_opy_ = item.nodeid + bstack11lll1l_opy_ (u"ࠧ࠮ࠩᑭ") + report.when
            if report.skipped:
                hook_type = bstack11lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᑮ") if report.when == bstack11lll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᑯ") else bstack11lll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑰ")
                _111l1ll1l1_opy_[bstack1111lllll1_opy_] = {
                    bstack11lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᑱ"): uuid4().__str__(),
                    bstack11lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᑲ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack11lll1l_opy_ (u"࡚࠭ࠨᑳ"),
                    bstack11lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᑴ"): hook_type
                }
            _111l1ll1l1_opy_[bstack1111lllll1_opy_][bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᑵ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack11lll1l_opy_ (u"ࠩ࡝ࠫᑶ")
            bstack111l1l1ll1_opy_(_111l1ll1l1_opy_[bstack1111lllll1_opy_][bstack11lll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᑷ")])
            bstack111l111lll_opy_(item, _111l1ll1l1_opy_[bstack1111lllll1_opy_], bstack11lll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᑸ"), report, call)
            if report.when == bstack11lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᑹ"):
                if report.outcome == bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑺ"):
                    bstack1111ll1ll1_opy_ = {
                        bstack11lll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᑻ"): uuid4().__str__(),
                        bstack11lll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᑼ"): bstack11l1l1111_opy_(),
                        bstack11lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᑽ"): bstack11l1l1111_opy_()
                    }
                    _111l1ll1l1_opy_[item.nodeid] = {**_111l1ll1l1_opy_[item.nodeid], **bstack1111ll1ll1_opy_}
                    bstack1111llll1l_opy_(item, _111l1ll1l1_opy_[item.nodeid], bstack11lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑾ"))
                    bstack1111llll1l_opy_(item, _111l1ll1l1_opy_[item.nodeid], bstack11lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᑿ"), report, call)
    except Exception as err:
        print(bstack11lll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪᒀ"), str(err))
def bstack1111lll1l1_opy_(test, bstack1111ll1ll1_opy_, result=None, call=None, bstack111ll111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lllll1l_opy_ = {
        bstack11lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᒁ"): bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᒂ")],
        bstack11lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᒃ"): bstack11lll1l_opy_ (u"ࠩࡷࡩࡸࡺࠧᒄ"),
        bstack11lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᒅ"): test.name,
        bstack11lll1l_opy_ (u"ࠫࡧࡵࡤࡺࠩᒆ"): {
            bstack11lll1l_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᒇ"): bstack11lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᒈ"),
            bstack11lll1l_opy_ (u"ࠧࡤࡱࡧࡩࠬᒉ"): inspect.getsource(test.obj)
        },
        bstack11lll1l_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᒊ"): test.name,
        bstack11lll1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᒋ"): test.name,
        bstack11lll1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᒌ"): bstack111lll111_opy_.bstack111lll11l1_opy_(test),
        bstack11lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᒍ"): file_path,
        bstack11lll1l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᒎ"): file_path,
        bstack11lll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᒏ"): bstack11lll1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᒐ"),
        bstack11lll1l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᒑ"): file_path,
        bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᒒ"): bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᒓ")],
        bstack11lll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᒔ"): bstack11lll1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᒕ"),
        bstack11lll1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᒖ"): {
            bstack11lll1l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᒗ"): test.nodeid
        },
        bstack11lll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᒘ"): bstack1l11l111ll_opy_(test.own_markers)
    }
    if bstack111ll111_opy_ in [bstack11lll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᒙ"), bstack11lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᒚ")]:
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᒛ")] = {
            bstack11lll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᒜ"): bstack1111ll1ll1_opy_.get(bstack11lll1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᒝ"), [])
        }
    if bstack111ll111_opy_ == bstack11lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᒞ"):
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᒟ")] = bstack11lll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᒠ")
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᒡ")] = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᒢ")]
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᒣ")] = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᒤ")]
    if result:
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᒥ")] = result.outcome
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᒦ")] = result.duration * 1000
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᒧ")] = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᒨ")]
        if result.failed:
            bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᒩ")] = bstack111lll111_opy_.bstack1l111l1ll1_opy_(call.excinfo.typename)
            bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᒪ")] = bstack111lll111_opy_.bstack111ll111ll_opy_(call.excinfo, result)
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᒫ")] = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᒬ")]
    if outcome:
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᒭ")] = bstack1l111l1lll_opy_(outcome)
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᒮ")] = 0
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᒯ")] = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᒰ")]
        if bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᒱ")] == bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒲ"):
            bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᒳ")] = bstack11lll1l_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩᒴ")  # bstack111l1ll111_opy_
            bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᒵ")] = [{bstack11lll1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᒶ"): [bstack11lll1l_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨᒷ")]}]
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᒸ")] = bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᒹ")]
    return bstack111lllll1l_opy_
def bstack111l111111_opy_(test, bstack111l11l1l1_opy_, bstack111ll111_opy_, result, call, outcome, bstack111l11l1ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᒺ")]
    hook_name = bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᒻ")]
    hook_data = {
        bstack11lll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᒼ"): bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᒽ")],
        bstack11lll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᒾ"): bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᒿ"),
        bstack11lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᓀ"): bstack11lll1l_opy_ (u"ࠧࡼࡿࠪᓁ").format(bstack11l1lll11l_opy_(hook_name)),
        bstack11lll1l_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᓂ"): {
            bstack11lll1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᓃ"): bstack11lll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᓄ"),
            bstack11lll1l_opy_ (u"ࠫࡨࡵࡤࡦࠩᓅ"): None
        },
        bstack11lll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᓆ"): test.name,
        bstack11lll1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᓇ"): bstack111lll111_opy_.bstack111lll11l1_opy_(test, hook_name),
        bstack11lll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᓈ"): file_path,
        bstack11lll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᓉ"): file_path,
        bstack11lll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᓊ"): bstack11lll1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᓋ"),
        bstack11lll1l_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᓌ"): file_path,
        bstack11lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᓍ"): bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᓎ")],
        bstack11lll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᓏ"): bstack11lll1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᓐ") if bstack111l111l1l_opy_ == bstack11lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᓑ") else bstack11lll1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᓒ"),
        bstack11lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᓓ"): hook_type
    }
    bstack111l1l1l11_opy_ = bstack111l1lll11_opy_(_111l1ll1l1_opy_.get(test.nodeid, None))
    if bstack111l1l1l11_opy_:
        hook_data[bstack11lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪᓔ")] = bstack111l1l1l11_opy_
    if result:
        hook_data[bstack11lll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᓕ")] = result.outcome
        hook_data[bstack11lll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᓖ")] = result.duration * 1000
        hook_data[bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓗ")] = bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᓘ")]
        if result.failed:
            hook_data[bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᓙ")] = bstack111lll111_opy_.bstack1l111l1ll1_opy_(call.excinfo.typename)
            hook_data[bstack11lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᓚ")] = bstack111lll111_opy_.bstack111ll111ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11lll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓛ")] = bstack1l111l1lll_opy_(outcome)
        hook_data[bstack11lll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᓜ")] = 100
        hook_data[bstack11lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᓝ")] = bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓞ")]
        if hook_data[bstack11lll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᓟ")] == bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᓠ"):
            hook_data[bstack11lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᓡ")] = bstack11lll1l_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᓢ")  # bstack111l1ll111_opy_
            hook_data[bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᓣ")] = [{bstack11lll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᓤ"): [bstack11lll1l_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᓥ")]}]
    if bstack111l11l1ll_opy_:
        hook_data[bstack11lll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᓦ")] = bstack111l11l1ll_opy_.result
        hook_data[bstack11lll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᓧ")] = bstack1l11l1ll11_opy_(bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᓨ")], bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᓩ")])
        hook_data[bstack11lll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᓪ")] = bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᓫ")]
        if hook_data[bstack11lll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᓬ")] == bstack11lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᓭ"):
            hook_data[bstack11lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᓮ")] = bstack111lll111_opy_.bstack1l111l1ll1_opy_(bstack111l11l1ll_opy_.exception_type)
            hook_data[bstack11lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᓯ")] = [{bstack11lll1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᓰ"): bstack1l111l1l1l_opy_(bstack111l11l1ll_opy_.exception)}]
    return hook_data
def bstack1111llll1l_opy_(test, bstack1111ll1ll1_opy_, bstack111ll111_opy_, result=None, call=None, outcome=None):
    bstack111lllll1l_opy_ = bstack1111lll1l1_opy_(test, bstack1111ll1ll1_opy_, result, call, bstack111ll111_opy_, outcome)
    driver = getattr(test, bstack11lll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᓱ"), None)
    if bstack111ll111_opy_ == bstack11lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᓲ") and driver:
        bstack111lllll1l_opy_[bstack11lll1l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᓳ")] = bstack111lll111_opy_.bstack111lll1l1l_opy_(driver)
    if bstack111ll111_opy_ == bstack11lll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᓴ"):
        bstack111ll111_opy_ = bstack11lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᓵ")
    bstack111ll1llll_opy_ = {
        bstack11lll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᓶ"): bstack111ll111_opy_,
        bstack11lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᓷ"): bstack111lllll1l_opy_
    }
    bstack111lll111_opy_.bstack111ll11lll_opy_(bstack111ll1llll_opy_)
def bstack111l111lll_opy_(test, bstack1111ll1ll1_opy_, bstack111ll111_opy_, result=None, call=None, outcome=None, bstack111l11l1ll_opy_=None):
    hook_data = bstack111l111111_opy_(test, bstack1111ll1ll1_opy_, bstack111ll111_opy_, result, call, outcome, bstack111l11l1ll_opy_)
    bstack111ll1llll_opy_ = {
        bstack11lll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᓸ"): bstack111ll111_opy_,
        bstack11lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᓹ"): hook_data
    }
    bstack111lll111_opy_.bstack111ll11lll_opy_(bstack111ll1llll_opy_)
def bstack111l1lll11_opy_(bstack1111ll1ll1_opy_):
    if not bstack1111ll1ll1_opy_:
        return None
    if bstack1111ll1ll1_opy_.get(bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᓺ"), None):
        return getattr(bstack1111ll1ll1_opy_[bstack11lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᓻ")], bstack11lll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᓼ"), None)
    return bstack1111ll1ll1_opy_.get(bstack11lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᓽ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack111lll111_opy_.on():
            return
        places = [bstack11lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᓾ"), bstack11lll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᓿ"), bstack11lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᔀ")]
        bstack111ll1ll11_opy_ = []
        for bstack111l11111l_opy_ in places:
            records = caplog.get_records(bstack111l11111l_opy_)
            bstack1111lll11l_opy_ = bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔁ") if bstack111l11111l_opy_ == bstack11lll1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᔂ") else bstack11lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔃ")
            bstack111l1l11ll_opy_ = request.node.nodeid + (bstack11lll1l_opy_ (u"ࠫࠬᔄ") if bstack111l11111l_opy_ == bstack11lll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᔅ") else bstack11lll1l_opy_ (u"࠭࠭ࠨᔆ") + bstack111l11111l_opy_)
            bstack111l1l1lll_opy_ = bstack111l1lll11_opy_(_111l1ll1l1_opy_.get(bstack111l1l11ll_opy_, None))
            if not bstack111l1l1lll_opy_:
                continue
            for record in records:
                if bstack1l11lll1ll_opy_(record.message):
                    continue
                bstack111ll1ll11_opy_.append({
                    bstack11lll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᔇ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11lll1l_opy_ (u"ࠨ࡜ࠪᔈ"),
                    bstack11lll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᔉ"): record.levelname,
                    bstack11lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔊ"): record.message,
                    bstack1111lll11l_opy_: bstack111l1l1lll_opy_
                })
        if len(bstack111ll1ll11_opy_) > 0:
            bstack111lll111_opy_.bstack111ll1l111_opy_(bstack111ll1ll11_opy_)
    except Exception as err:
        print(bstack11lll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨᔋ"), str(err))
def bstack111l1111ll_opy_(driver_command, response):
    if driver_command == bstack11lll1l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩᔌ"):
        bstack111lll111_opy_.bstack111llll111_opy_({
            bstack11lll1l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᔍ"): response[bstack11lll1l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᔎ")],
            bstack11lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔏ"): store[bstack11lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᔐ")]
        })
def bstack111l1111_opy_():
    global bstack1lll111ll_opy_
    bstack111lll111_opy_.bstack111lll111l_opy_()
    for driver in bstack1lll111ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1lllll_opy_(self, *args, **kwargs):
    bstack1lll1l1lll_opy_ = bstack11ll11ll_opy_(self, *args, **kwargs)
    bstack111lll111_opy_.bstack1111111l1_opy_(self)
    return bstack1lll1l1lll_opy_
def bstack1ll1lll1ll_opy_(framework_name):
    global bstack11l11ll1_opy_
    global bstack1ll111l11_opy_
    bstack11l11ll1_opy_ = framework_name
    logger.info(bstack11ll1lll_opy_.format(bstack11l11ll1_opy_.split(bstack11lll1l_opy_ (u"ࠪ࠱ࠬᔑ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l11lll111_opy_():
            Service.start = bstack1l1ll1l1_opy_
            Service.stop = bstack111l1111l_opy_
            webdriver.Remote.__init__ = bstack111lll11l_opy_
            webdriver.Remote.get = bstack111ll11l_opy_
            if not isinstance(os.getenv(bstack11lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬᔒ")), str):
                return
            WebDriver.close = bstack11ll11l1_opy_
            WebDriver.quit = bstack1l1llll11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1111lll1_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack11l11111_opy_ = getAccessibilityResultsSummary
        if not bstack1l11lll111_opy_() and bstack111lll111_opy_.on():
            webdriver.Remote.__init__ = bstack1lll1lllll_opy_
        bstack1ll111l11_opy_ = True
    except Exception as e:
        pass
    bstack1ll1lllll1_opy_()
    if os.environ.get(bstack11lll1l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᔓ")):
        bstack1ll111l11_opy_ = eval(os.environ.get(bstack11lll1l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᔔ")))
    if not bstack1ll111l11_opy_:
        bstack1l1lll1lll_opy_(bstack11lll1l_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤᔕ"), bstack1ll111l111_opy_)
    if bstack1lll1ll11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l11l1l1l_opy_
        except Exception as e:
            logger.error(bstack11l1l1l1l_opy_.format(str(e)))
    if bstack11lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᔖ") in str(framework_name).lower():
        if not bstack1l11lll111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1111ll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll11ll1_opy_
            Config.getoption = bstack11l1l111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack111ll11ll_opy_
        except Exception as e:
            pass
def bstack1l1llll11_opy_(self):
    global bstack11l11ll1_opy_
    global bstack11ll1ll1_opy_
    global bstack1111l111_opy_
    try:
        if bstack11lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᔗ") in bstack11l11ll1_opy_ and self.session_id != None and bstack11lll111_opy_(threading.current_thread(), bstack11lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᔘ"), bstack11lll1l_opy_ (u"ࠫࠬᔙ")) != bstack11lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᔚ"):
            bstack111l11lll_opy_ = bstack11lll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᔛ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᔜ")
            bstack1lll111l11_opy_ = bstack1llll1ll_opy_(bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᔝ"), bstack11lll1l_opy_ (u"ࠩࠪᔞ"), bstack111l11lll_opy_, bstack11lll1l_opy_ (u"ࠪ࠰ࠥ࠭ᔟ").join(
                threading.current_thread().bstackTestErrorMessages), bstack11lll1l_opy_ (u"ࠫࠬᔠ"), bstack11lll1l_opy_ (u"ࠬ࠭ᔡ"))
            bstack1ll11llll_opy_(logger, True)
            if self != None:
                self.execute_script(bstack1lll111l11_opy_)
    except Exception as e:
        logger.debug(bstack11lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢᔢ") + str(e))
    bstack1111l111_opy_(self)
    self.session_id = None
def bstack111lll11l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll1ll1_opy_
    global bstack11l1ll11l_opy_
    global bstack1l11llll1_opy_
    global bstack11l11ll1_opy_
    global bstack11ll11ll_opy_
    global bstack1lll111ll_opy_
    global bstack1lll1l1l_opy_
    global bstack1l1ll11ll_opy_
    global bstack1111llll11_opy_
    global bstack111l111l1_opy_
    CONFIG[bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᔣ")] = str(bstack11l11ll1_opy_) + str(__version__)
    command_executor = bstack111l11111_opy_(bstack1lll1l1l_opy_)
    logger.debug(bstack11l1l1lll_opy_.format(command_executor))
    proxy = bstack1ll111ll1l_opy_(CONFIG, proxy)
    bstack1ll11ll11l_opy_ = 0
    try:
        if bstack1l11llll1_opy_ is True:
            bstack1ll11ll11l_opy_ = int(os.environ.get(bstack11lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᔤ")))
    except:
        bstack1ll11ll11l_opy_ = 0
    bstack1111lllll_opy_ = bstack111l1l11_opy_(CONFIG, bstack1ll11ll11l_opy_)
    logger.debug(bstack1llll111ll_opy_.format(str(bstack1111lllll_opy_)))
    bstack111l111l1_opy_ = CONFIG.get(bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᔥ"))[bstack1ll11ll11l_opy_]
    if bstack11lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᔦ") in CONFIG and CONFIG[bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᔧ")]:
        bstack111ll1l1_opy_(bstack1111lllll_opy_, bstack1l1ll11ll_opy_)
    if desired_capabilities:
        bstack1l111ll1_opy_ = bstack1llll1111l_opy_(desired_capabilities)
        bstack1l111ll1_opy_[bstack11lll1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᔨ")] = bstack1l111l1l_opy_(CONFIG)
        bstack1ll11lll_opy_ = bstack111l1l11_opy_(bstack1l111ll1_opy_)
        if bstack1ll11lll_opy_:
            bstack1111lllll_opy_ = update(bstack1ll11lll_opy_, bstack1111lllll_opy_)
        desired_capabilities = None
    if options:
        bstack11111lll1_opy_(options, bstack1111lllll_opy_)
    if not options:
        options = bstack1l11l1lll_opy_(bstack1111lllll_opy_)
    if bstack1111l11ll_opy_.bstack1l11111ll_opy_(CONFIG, bstack1ll11ll11l_opy_) and bstack1111l11ll_opy_.bstack1ll11ll11_opy_(bstack1111lllll_opy_, options):
        bstack1111llll11_opy_ = True
        bstack1111l11ll_opy_.set_capabilities(bstack1111lllll_opy_, CONFIG)
    if proxy and bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᔩ")):
        options.proxy(proxy)
    if options and bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᔪ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1ll11_opy_() < version.parse(bstack11lll1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᔫ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1111lllll_opy_)
    logger.info(bstack1ll11111l_opy_)
    if bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᔬ")):
        bstack11ll11ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᔭ")):
        bstack11ll11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᔮ")):
        bstack11ll11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11ll11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1lll1lll1_opy_ = bstack11lll1l_opy_ (u"ࠬ࠭ᔯ")
        if bstack1ll1ll11_opy_() >= version.parse(bstack11lll1l_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧᔰ")):
            bstack1lll1lll1_opy_ = self.caps.get(bstack11lll1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᔱ"))
        else:
            bstack1lll1lll1_opy_ = self.capabilities.get(bstack11lll1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᔲ"))
        if bstack1lll1lll1_opy_:
            bstack11llll11l_opy_(bstack1lll1lll1_opy_)
            if bstack1ll1ll11_opy_() <= version.parse(bstack11lll1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᔳ")):
                self.command_executor._url = bstack11lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᔴ") + bstack1lll1l1l_opy_ + bstack11lll1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᔵ")
            else:
                self.command_executor._url = bstack11lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᔶ") + bstack1lll1lll1_opy_ + bstack11lll1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᔷ")
            logger.debug(bstack1ll1l1ll1_opy_.format(bstack1lll1lll1_opy_))
        else:
            logger.debug(bstack11llll1l1_opy_.format(bstack11lll1l_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᔸ")))
    except Exception as e:
        logger.debug(bstack11llll1l1_opy_.format(e))
    bstack11ll1ll1_opy_ = self.session_id
    if bstack11lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᔹ") in bstack11l11ll1_opy_:
        threading.current_thread().bstack11lllllll_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack111lll111_opy_.bstack1111111l1_opy_(self)
    bstack1lll111ll_opy_.append(self)
    if bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᔺ") in CONFIG and bstack11lll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᔻ") in CONFIG[bstack11lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᔼ")][bstack1ll11ll11l_opy_]:
        bstack11l1ll11l_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᔽ")][bstack1ll11ll11l_opy_][bstack11lll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᔾ")]
    logger.debug(bstack1llll11l1l_opy_.format(bstack11ll1ll1_opy_))
def bstack111ll11l_opy_(self, url):
    global bstack111ll1l11_opy_
    global CONFIG
    try:
        bstack11l11ll11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11111ll1l_opy_.format(str(err)))
    try:
        bstack111ll1l11_opy_(self, url)
    except Exception as e:
        try:
            bstack11l1ll1l1_opy_ = str(e)
            if any(err_msg in bstack11l1ll1l1_opy_ for err_msg in bstack11llll111_opy_):
                bstack11l11ll11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11111ll1l_opy_.format(str(err)))
        raise e
def bstack111llll1l_opy_(item, when):
    global bstack1ll1ll1l1_opy_
    try:
        bstack1ll1ll1l1_opy_(item, when)
    except Exception as e:
        pass
def bstack111ll11ll_opy_(item, call, rep):
    global bstack1ll1l1l1ll_opy_
    global bstack1lll111ll_opy_
    name = bstack11lll1l_opy_ (u"ࠧࠨᔿ")
    try:
        if rep.when == bstack11lll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᕀ"):
            bstack11ll1ll1_opy_ = threading.current_thread().bstack11lllllll_opy_
            bstack111l11lll1_opy_ = item.config.getoption(bstack11lll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᕁ"))
            try:
                if (str(bstack111l11lll1_opy_).lower() != bstack11lll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᕂ")):
                    name = str(rep.nodeid)
                    bstack1lll111l11_opy_ = bstack1llll1ll_opy_(bstack11lll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᕃ"), name, bstack11lll1l_opy_ (u"ࠬ࠭ᕄ"), bstack11lll1l_opy_ (u"࠭ࠧᕅ"), bstack11lll1l_opy_ (u"ࠧࠨᕆ"), bstack11lll1l_opy_ (u"ࠨࠩᕇ"))
                    os.environ[bstack11lll1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᕈ")] = name
                    for driver in bstack1lll111ll_opy_:
                        if bstack11ll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll111l11_opy_)
            except Exception as e:
                logger.debug(bstack11lll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᕉ").format(str(e)))
            try:
                bstack11l11l111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᕊ"):
                    status = bstack11lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᕋ") if rep.outcome.lower() == bstack11lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᕌ") else bstack11lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᕍ")
                    reason = bstack11lll1l_opy_ (u"ࠨࠩᕎ")
                    if status == bstack11lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᕏ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11lll1l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᕐ") if status == bstack11lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᕑ") else bstack11lll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᕒ")
                    data = name + bstack11lll1l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨᕓ") if status == bstack11lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᕔ") else name + bstack11lll1l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫᕕ") + reason
                    bstack11111l1l1_opy_ = bstack1llll1ll_opy_(bstack11lll1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᕖ"), bstack11lll1l_opy_ (u"ࠪࠫᕗ"), bstack11lll1l_opy_ (u"ࠫࠬᕘ"), bstack11lll1l_opy_ (u"ࠬ࠭ᕙ"), level, data)
                    for driver in bstack1lll111ll_opy_:
                        if bstack11ll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11111l1l1_opy_)
            except Exception as e:
                logger.debug(bstack11lll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᕚ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11lll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫᕛ").format(str(e)))
    bstack1ll1l1l1ll_opy_(item, call, rep)
notset = Notset()
def bstack11l1l111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lllll111l_opy_
    if str(name).lower() == bstack11lll1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᕜ"):
        return bstack11lll1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᕝ")
    else:
        return bstack1lllll111l_opy_(self, name, default, skip)
def bstack1l11l1l1l_opy_(self):
    global CONFIG
    global bstack11ll1l11_opy_
    try:
        proxy = bstack11lllll1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11lll1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᕞ")):
                proxies = bstack1ll11l1l1_opy_(proxy, bstack111l11111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1llllll_opy_ = proxies.popitem()
                    if bstack11lll1l_opy_ (u"ࠦ࠿࠵࠯ࠣᕟ") in bstack1l1llllll_opy_:
                        return bstack1l1llllll_opy_
                    else:
                        return bstack11lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᕠ") + bstack1l1llllll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥᕡ").format(str(e)))
    return bstack11ll1l11_opy_(self)
def bstack1lll1ll11_opy_():
    return (bstack11lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᕢ") in CONFIG or bstack11lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᕣ") in CONFIG) and bstack1l1l1llll_opy_() and bstack1ll1ll11_opy_() >= version.parse(
        bstack1l1lll1l_opy_)
def bstack11l11l11l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11l1ll11l_opy_
    global bstack1l11llll1_opy_
    global bstack11l11ll1_opy_
    CONFIG[bstack11lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᕤ")] = str(bstack11l11ll1_opy_) + str(__version__)
    bstack1ll11ll11l_opy_ = 0
    try:
        if bstack1l11llll1_opy_ is True:
            bstack1ll11ll11l_opy_ = int(os.environ.get(bstack11lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᕥ")))
    except:
        bstack1ll11ll11l_opy_ = 0
    CONFIG[bstack11lll1l_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᕦ")] = True
    bstack1111lllll_opy_ = bstack111l1l11_opy_(CONFIG, bstack1ll11ll11l_opy_)
    logger.debug(bstack1llll111ll_opy_.format(str(bstack1111lllll_opy_)))
    if CONFIG.get(bstack11lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᕧ")):
        bstack111ll1l1_opy_(bstack1111lllll_opy_, bstack1l1ll11ll_opy_)
    if bstack11lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᕨ") in CONFIG and bstack11lll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᕩ") in CONFIG[bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᕪ")][bstack1ll11ll11l_opy_]:
        bstack11l1ll11l_opy_ = CONFIG[bstack11lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᕫ")][bstack1ll11ll11l_opy_][bstack11lll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᕬ")]
    import urllib
    import json
    bstack1l1111l1_opy_ = bstack11lll1l_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ᕭ") + urllib.parse.quote(json.dumps(bstack1111lllll_opy_))
    browser = self.connect(bstack1l1111l1_opy_)
    return browser
def bstack1ll1lllll1_opy_():
    global bstack1ll111l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11l11l_opy_
        bstack1ll111l11_opy_ = True
    except Exception as e:
        pass
def bstack1111ll1lll_opy_():
    global CONFIG
    global bstack1l1lllll_opy_
    global bstack1lll1l1l_opy_
    global bstack1l1ll11ll_opy_
    global bstack1l11llll1_opy_
    CONFIG = json.loads(os.environ.get(bstack11lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫᕮ")))
    bstack1l1lllll_opy_ = eval(os.environ.get(bstack11lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᕯ")))
    bstack1lll1l1l_opy_ = os.environ.get(bstack11lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧᕰ"))
    bstack1lll111111_opy_(CONFIG, bstack1l1lllll_opy_)
    bstack11lll1l11_opy_()
    global bstack11ll11ll_opy_
    global bstack1111l111_opy_
    global bstack1llll1ll1l_opy_
    global bstack1ll1lll11l_opy_
    global bstack1llll1l11_opy_
    global bstack1ll1l11l1l_opy_
    global bstack1l1l1111_opy_
    global bstack111ll1l11_opy_
    global bstack11ll1l11_opy_
    global bstack1lllll111l_opy_
    global bstack1ll1ll1l1_opy_
    global bstack1ll1l1l1ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11ll11ll_opy_ = webdriver.Remote.__init__
        bstack1111l111_opy_ = WebDriver.quit
        bstack1l1l1111_opy_ = WebDriver.close
        bstack111ll1l11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᕱ") in CONFIG or bstack11lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᕲ") in CONFIG) and bstack1l1l1llll_opy_():
        if bstack1ll1ll11_opy_() < version.parse(bstack1l1lll1l_opy_):
            logger.error(bstack111l1ll11_opy_.format(bstack1ll1ll11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11ll1l11_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack11l1l1l1l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lllll111l_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll1ll1l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1l11l1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll1l1l1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11lll1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫᕳ"))
    bstack1l1ll11ll_opy_ = CONFIG.get(bstack11lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᕴ"), {}).get(bstack11lll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᕵ"))
    bstack1l11llll1_opy_ = True
    bstack1ll1lll1ll_opy_(bstack1l1l11111_opy_)
if (bstack1l11l1ll1l_opy_()):
    bstack1111ll1lll_opy_()
@bstack1l1l1l1lll_opy_(class_method=False)
def bstack111l111l11_opy_(hook_name, event, bstack1111lll111_opy_=None):
    if hook_name not in [bstack11lll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᕶ"), bstack11lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᕷ"), bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᕸ"), bstack11lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᕹ"), bstack11lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᕺ"), bstack11lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᕻ"), bstack11lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᕼ"), bstack11lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᕽ")]:
        return
    node = store[bstack11lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᕾ")]
    if hook_name in [bstack11lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᕿ"), bstack11lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᖀ")]:
        node = store[bstack11lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᖁ")]
    elif hook_name in [bstack11lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᖂ"), bstack11lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᖃ")]:
        node = store[bstack11lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᖄ")]
    if event == bstack11lll1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᖅ"):
        hook_type = bstack11l1ll1111_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack111l11l1l1_opy_ = {
            bstack11lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖆ"): uuid,
            bstack11lll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖇ"): bstack11l1l1111_opy_(),
            bstack11lll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᖈ"): bstack11lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᖉ"),
            bstack11lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᖊ"): hook_type,
            bstack11lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᖋ"): hook_name
        }
        store[bstack11lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖌ")].append(uuid)
        bstack111l11llll_opy_ = node.nodeid
        if hook_type == bstack11lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᖍ"):
            if not _111l1ll1l1_opy_.get(bstack111l11llll_opy_, None):
                _111l1ll1l1_opy_[bstack111l11llll_opy_] = {bstack11lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᖎ"): []}
            _111l1ll1l1_opy_[bstack111l11llll_opy_][bstack11lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᖏ")].append(bstack111l11l1l1_opy_[bstack11lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᖐ")])
        _111l1ll1l1_opy_[bstack111l11llll_opy_ + bstack11lll1l_opy_ (u"ࠬ࠳ࠧᖑ") + hook_name] = bstack111l11l1l1_opy_
        bstack111l111lll_opy_(node, bstack111l11l1l1_opy_, bstack11lll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᖒ"))
    elif event == bstack11lll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᖓ"):
        bstack1111lllll1_opy_ = node.nodeid + bstack11lll1l_opy_ (u"ࠨ࠯ࠪᖔ") + hook_name
        _111l1ll1l1_opy_[bstack1111lllll1_opy_][bstack11lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᖕ")] = bstack11l1l1111_opy_()
        bstack111l1l1ll1_opy_(_111l1ll1l1_opy_[bstack1111lllll1_opy_][bstack11lll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖖ")])
        bstack111l111lll_opy_(node, _111l1ll1l1_opy_[bstack1111lllll1_opy_], bstack11lll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᖗ"), bstack111l11l1ll_opy_=bstack1111lll111_opy_)
def bstack1111llllll_opy_():
    global bstack111l111l1l_opy_
    if bstack1ll1111111_opy_():
        bstack111l111l1l_opy_ = bstack11lll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᖘ")
    else:
        bstack111l111l1l_opy_ = bstack11lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᖙ")
@bstack111lll111_opy_.bstack111lll1lll_opy_
def bstack1111lll1ll_opy_():
    bstack1111llllll_opy_()
    if bstack1l1l1llll_opy_():
        bstack11l11lll11_opy_(bstack111l1111ll_opy_)
    bstack1l11111111_opy_ = bstack1l11111l11_opy_(bstack111l111l11_opy_)
bstack1111lll1ll_opy_()