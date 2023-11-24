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
from browserstack_sdk.__init__ import (bstack1ll1ll1lll_opy_, bstack11lllll1_opy_, update, bstack111l1lll1_opy_,
                                       bstack1ll11111ll_opy_, bstack1ll1l11lll_opy_, bstack11l1ll11_opy_, bstack11l11111l_opy_,
                                       bstack1l1l111l1_opy_, bstack1l1111lll_opy_, bstack1ll1l1l111_opy_, bstack11l1lllll_opy_,
                                       bstack1ll1llll_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1l111l1l_opy_
from bstack_utils.constants import bstack1ll1l1l11l_opy_, bstack11l111l1l_opy_, bstack111111111_opy_, bstack1ll111l11_opy_, \
    bstack1l11l11ll_opy_
from bstack_utils.helper import bstack1ll111l111_opy_, bstack1111ll111_opy_, bstack1l111l1l11_opy_, bstack1111111l1_opy_, bstack1l11lll1l1_opy_, \
    bstack1l11l11l11_opy_, bstack1llll1ll1_opy_, bstack1l1111ll_opy_, bstack1l11l1lll1_opy_, bstack111l1ll11_opy_, Notset, \
    bstack1lll11l1_opy_, bstack1l11lll1ll_opy_, bstack1l11l11111_opy_, Result, bstack1l11l1l1ll_opy_, bstack1l111ll111_opy_, bstack1l1l1ll1ll_opy_, bstack1l11ll111_opy_, bstack11l1ll11l_opy_
from bstack_utils.bstack11lllllll1_opy_ import bstack1l111111ll_opy_
from bstack_utils.messages import bstack1ll1l1lll_opy_, bstack111ll1ll1_opy_, bstack1l1l1ll1l_opy_, bstack111l1111l_opy_, bstack111lllll_opy_, \
    bstack1ll111ll11_opy_, bstack1l1ll1l1l_opy_, bstack111l1ll1_opy_, bstack1l111l111_opy_, bstack1ll1lllll1_opy_, \
    bstack1l1llll1l_opy_, bstack11lll1l11_opy_
from bstack_utils.proxy import bstack111ll1111_opy_, bstack111llllll_opy_
from bstack_utils.bstack1l1llllll1_opy_ import bstack11l1l1ll1l_opy_, bstack11l1lll111_opy_, bstack11l1ll1ll1_opy_, bstack11l1l1l1ll_opy_, \
    bstack11l1ll111l_opy_, bstack11l1ll11l1_opy_, bstack11l1l1lll1_opy_, bstack111l11ll1_opy_, bstack11l1ll11ll_opy_
from bstack_utils.bstack11l11lll1l_opy_ import bstack11l11ll1l1_opy_
from bstack_utils.bstack11l1l1ll11_opy_ import bstack1llll1lll1_opy_, bstack1ll111lll1_opy_, bstack1lll1l1111_opy_
from bstack_utils.bstack11l1111l1l_opy_ import bstack11l111llll_opy_
from bstack_utils.bstack11l11ll1_opy_ import bstack1l1lll11l_opy_
import bstack_utils.bstack1l1ll1l1_opy_ as bstack111ll1l1l_opy_
bstack1l1ll1l11_opy_ = None
bstack1ll1l1l1l_opy_ = None
bstack1lll11lll_opy_ = None
bstack1ll11ll111_opy_ = None
bstack11llll1l1_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack1ll11l1ll_opy_ = None
bstack11l1111l1_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack1l1l1111_opy_ = None
bstack1111l11l_opy_ = None
bstack111llll11_opy_ = None
bstack11111l11_opy_ = None
bstack1lll1l1ll_opy_ = bstack1111_opy_ (u"ࠨࠩᎱ")
CONFIG = {}
bstack11llll11_opy_ = False
bstack11l11l11l_opy_ = bstack1111_opy_ (u"ࠩࠪᎲ")
bstack1ll1ll1l11_opy_ = bstack1111_opy_ (u"ࠪࠫᎳ")
bstack1lll1l1l1_opy_ = False
bstack11lll1111_opy_ = []
bstack1lll11l11_opy_ = bstack11l111l1l_opy_
bstack111l11llll_opy_ = bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᎴ")
bstack111l1111ll_opy_ = False
bstack111l1lll11_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lll11l11_opy_,
                    format=bstack1111_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᎵ"),
                    datefmt=bstack1111_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨᎶ"),
                    stream=sys.stdout)
store = {
    bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᎷ"): []
}
def bstack111l111ll_opy_():
    global CONFIG
    global bstack1lll11l11_opy_
    if bstack1111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᎸ") in CONFIG:
        bstack1lll11l11_opy_ = bstack1ll1l1l11l_opy_[CONFIG[bstack1111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᎹ")]]
        logging.getLogger().setLevel(bstack1lll11l11_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l11lll1_opy_ = {}
current_test_uuid = None
def bstack111ll111l_opy_(page, bstack11111l111_opy_):
    try:
        page.evaluate(bstack1111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᎺ"),
                      bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨᎻ") + json.dumps(
                          bstack11111l111_opy_) + bstack1111_opy_ (u"ࠧࢃࡽࠣᎼ"))
    except Exception as e:
        print(bstack1111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦᎽ"), e)
def bstack1l1lll1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᎾ"), bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭Ꮏ") + json.dumps(
            message) + bstack1111_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬᏀ") + json.dumps(level) + bstack1111_opy_ (u"ࠪࢁࢂ࠭Ꮑ"))
    except Exception as e:
        print(bstack1111_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢᏂ"), e)
def bstack1l1ll1lll_opy_(page, status, message=bstack1111_opy_ (u"ࠧࠨᏃ")):
    try:
        if (status == bstack1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᏄ")):
            page.evaluate(bstack1111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᏅ"),
                          bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠩᏆ") + json.dumps(
                              bstack1111_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࠦᏇ") + str(message)) + bstack1111_opy_ (u"ࠪ࠰ࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧᏈ") + json.dumps(status) + bstack1111_opy_ (u"ࠦࢂࢃࠢᏉ"))
        else:
            page.evaluate(bstack1111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᏊ"),
                          bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧᏋ") + json.dumps(
                              status) + bstack1111_opy_ (u"ࠢࡾࡿࠥᏌ"))
    except Exception as e:
        print(bstack1111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧᏍ"), e)
def pytest_configure(config):
    config.args = bstack1l1lll11l_opy_.bstack111lll11ll_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack111l111111_opy_ = item.config.getoption(bstack1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᏎ"))
    plugins = item.config.getoption(bstack1111_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦᏏ"))
    report = outcome.get_result()
    bstack111l1111l1_opy_(item, call, report)
    if bstack1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤᏐ") not in plugins or bstack111l1ll11_opy_():
        return
    summary = []
    driver = getattr(item, bstack1111_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨᏑ"), None)
    page = getattr(item, bstack1111_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧᏒ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1111lll1l1_opy_(item, report, summary, bstack111l111111_opy_)
    if (page is not None):
        bstack1111llll11_opy_(item, report, summary, bstack111l111111_opy_)
def bstack1111lll1l1_opy_(item, report, summary, bstack111l111111_opy_):
    if report.when in [bstack1111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᏓ"), bstack1111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᏔ")]:
        return
    if not bstack1l111l1l11_opy_():
        return
    try:
        if (str(bstack111l111111_opy_).lower() != bstack1111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᏕ")):
            item._driver.execute_script(
                bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨᏖ") + json.dumps(
                    report.nodeid) + bstack1111_opy_ (u"ࠫࢂࢃࠧᏗ"))
        os.environ[bstack1111_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᏘ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1111_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨᏙ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᏚ")))
    bstack11l111ll1_opy_ = bstack1111_opy_ (u"ࠣࠤᏛ")
    bstack11l1ll11ll_opy_(report)
    if not passed:
        try:
            bstack11l111ll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᏜ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111ll1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᏝ")))
        bstack11l111ll1_opy_ = bstack1111_opy_ (u"ࠦࠧᏞ")
        if not passed:
            try:
                bstack11l111ll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᏟ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111ll1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᏠ")
                    + json.dumps(bstack1111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣᏡ"))
                    + bstack1111_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᏢ")
                )
            else:
                item._driver.execute_script(
                    bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᏣ")
                    + json.dumps(str(bstack11l111ll1_opy_))
                    + bstack1111_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᏤ")
                )
        except Exception as e:
            summary.append(bstack1111_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤᏥ").format(e))
def bstack111l1lll1l_opy_(test_name, error_message):
    try:
        bstack1111lll11l_opy_ = []
        bstack1ll111ll1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᏦ"), bstack1111_opy_ (u"࠭࠰ࠨᏧ"))
        bstack1llllll11_opy_ = {bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏨ"): test_name, bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᏩ"): error_message, bstack1111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᏪ"): bstack1ll111ll1_opy_}
        bstack111l11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᏫ"))
        if os.path.exists(bstack111l11l1ll_opy_):
            with open(bstack111l11l1ll_opy_) as f:
                bstack1111lll11l_opy_ = json.load(f)
        bstack1111lll11l_opy_.append(bstack1llllll11_opy_)
        with open(bstack111l11l1ll_opy_, bstack1111_opy_ (u"ࠫࡼ࠭Ꮼ")) as f:
            json.dump(bstack1111lll11l_opy_, f)
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪᏭ") + str(e))
def bstack1111llll11_opy_(item, report, summary, bstack111l111111_opy_):
    if report.when in [bstack1111_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᏮ"), bstack1111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᏯ")]:
        return
    if (str(bstack111l111111_opy_).lower() != bstack1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ᏸ")):
        bstack111ll111l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᏱ")))
    bstack11l111ll1_opy_ = bstack1111_opy_ (u"ࠥࠦᏲ")
    bstack11l1ll11ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l111ll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᏳ").format(e)
                )
        try:
            if passed:
                bstack1l1ll1lll_opy_(item._page, bstack1111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᏴ"))
            else:
                error_message = bstack1111_opy_ (u"࠭ࠧᏵ")
                if bstack11l111ll1_opy_:
                    bstack1l1lll1l_opy_(item._page, str(bstack11l111ll1_opy_), bstack1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ᏶"))
                    bstack1l1ll1lll_opy_(item._page, bstack1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ᏷"), str(bstack11l111ll1_opy_))
                    error_message = str(bstack11l111ll1_opy_)
                else:
                    bstack1l1ll1lll_opy_(item._page, bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᏸ"))
                bstack111l1lll1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1111_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢᏹ").format(e))
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
    parser.addoption(bstack1111_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᏺ"), default=bstack1111_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᏻ"), help=bstack1111_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᏼ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1111_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤᏽ"), action=bstack1111_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢ᏾"), default=bstack1111_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤ᏿"),
                         help=bstack1111_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤ᐀"))
def bstack111l11l11l_opy_(log):
    if not (log[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐁ")] and log[bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᐂ")].strip()):
        return
    active = bstack1111llllll_opy_()
    log = {
        bstack1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᐃ"): log[bstack1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᐄ")],
        bstack1111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᐅ"): datetime.datetime.utcnow().isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫᐆ"),
        bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᐇ"): log[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐈ")],
    }
    if active:
        if active[bstack1111_opy_ (u"ࠬࡺࡹࡱࡧࠪᐉ")] == bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᐊ"):
            log[bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᐋ")] = active[bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᐌ")]
        elif active[bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᐍ")] == bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࠨᐎ"):
            log[bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᐏ")] = active[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᐐ")]
    bstack1l1lll11l_opy_.bstack111ll1l111_opy_([log])
def bstack1111llllll_opy_():
    if len(store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᐑ")]) > 0 and store[bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᐒ")][-1]:
        return {
            bstack1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᐓ"): bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᐔ"),
            bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᐕ"): store[bstack1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᐖ")][-1]
        }
    if store.get(bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᐗ"), None):
        return {
            bstack1111_opy_ (u"࠭ࡴࡺࡲࡨࠫᐘ"): bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࠬᐙ"),
            bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᐚ"): store[bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᐛ")]
        }
    return None
bstack1111ll1ll1_opy_ = bstack1l1l111l1l_opy_(bstack111l11l11l_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack111l1111ll_opy_
        if bstack111l1111ll_opy_:
            driver = getattr(item, bstack1111_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᐜ"), None)
            bstack1lll11l1ll_opy_ = bstack111ll1l1l_opy_.bstack11lll11l_opy_(CONFIG, bstack1l11l11l11_opy_(item.own_markers))
            item._a11y_started = bstack111ll1l1l_opy_.bstack111lll1l1_opy_(driver, bstack1lll11l1ll_opy_)
        if not bstack1l1lll11l_opy_.on() or bstack111l11llll_opy_ != bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᐝ"):
            return
        global current_test_uuid, bstack1111ll1ll1_opy_
        bstack1111ll1ll1_opy_.start()
        bstack111l1l1l11_opy_ = {
            bstack1111_opy_ (u"ࠬࡻࡵࡪࡦࠪᐞ"): uuid4().__str__(),
            bstack1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᐟ"): datetime.datetime.utcnow().isoformat() + bstack1111_opy_ (u"࡛ࠧࠩᐠ")
        }
        current_test_uuid = bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᐡ")]
        store[bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᐢ")] = bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᐣ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11lll1_opy_[item.nodeid] = {**_111l11lll1_opy_[item.nodeid], **bstack111l1l1l11_opy_}
        bstack111l1l111l_opy_(item, _111l11lll1_opy_[item.nodeid], bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᐤ"))
    except Exception as err:
        print(bstack1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧᐥ"), str(err))
def pytest_runtest_setup(item):
    if bstack1l11l1lll1_opy_():
        atexit.register(bstack1llllll111_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11l1l1ll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᐦ")
    try:
        if not bstack1l1lll11l_opy_.on():
            return
        bstack1111ll1ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack111l1l1l11_opy_ = {
            bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᐧ"): uuid,
            bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᐨ"): datetime.datetime.utcnow().isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫᐩ"),
            bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨᐪ"): bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᐫ"),
            bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᐬ"): bstack1111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᐭ"),
            bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᐮ"): bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᐯ")
        }
        threading.current_thread().bstack111l11ll11_opy_ = uuid
        store[bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᐰ")] = item
        store[bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᐱ")] = [uuid]
        if not _111l11lll1_opy_.get(item.nodeid, None):
            _111l11lll1_opy_[item.nodeid] = {bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᐲ"): [], bstack1111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᐳ"): []}
        _111l11lll1_opy_[item.nodeid][bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᐴ")].append(bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᐵ")])
        _111l11lll1_opy_[item.nodeid + bstack1111_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨᐶ")] = bstack111l1l1l11_opy_
        bstack1111ll1lll_opy_(item, bstack111l1l1l11_opy_, bstack1111_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᐷ"))
    except Exception as err:
        print(bstack1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᐸ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack111l1lll11_opy_
        if getattr(item, bstack1111_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫᐹ"), False):
            logger.info(bstack1111_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧᐺ"))
            driver = getattr(item, bstack1111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᐻ"), None)
            bstack1l1l1l111l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack111ll1l1l_opy_.bstack1ll1llll1l_opy_(driver, bstack1l1l1l111l_opy_, item.name, item.module.__name__, item.path, bstack111l1lll11_opy_)
        if not bstack1l1lll11l_opy_.on():
            return
        bstack111l1l1l11_opy_ = {
            bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᐼ"): uuid4().__str__(),
            bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᐽ"): datetime.datetime.utcnow().isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫᐾ"),
            bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨᐿ"): bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᑀ"),
            bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᑁ"): bstack1111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᑂ"),
            bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᑃ"): bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑄ")
        }
        _111l11lll1_opy_[item.nodeid + bstack1111_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬᑅ")] = bstack111l1l1l11_opy_
        bstack1111ll1lll_opy_(item, bstack111l1l1l11_opy_, bstack1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑆ"))
    except Exception as err:
        print(bstack1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᑇ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l1lll11l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack11l1l1l1ll_opy_(fixturedef.argname):
        store[bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᑈ")] = request.node
    elif bstack11l1ll111l_opy_(fixturedef.argname):
        store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᑉ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᑊ"): fixturedef.argname,
            bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᑋ"): bstack1l11lll1l1_opy_(outcome),
            bstack1111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᑌ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack111l1l1l1l_opy_ = store[bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᑍ")]
        if not _111l11lll1_opy_.get(bstack111l1l1l1l_opy_.nodeid, None):
            _111l11lll1_opy_[bstack111l1l1l1l_opy_.nodeid] = {bstack1111_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᑎ"): []}
        _111l11lll1_opy_[bstack111l1l1l1l_opy_.nodeid][bstack1111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᑏ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᑐ"), str(err))
if bstack111l1ll11_opy_() and bstack1l1lll11l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _111l11lll1_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᑑ")].bstack111lllll11_opy_(id(step))
        except Exception as err:
            print(bstack1111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ᑒ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _111l11lll1_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᑓ")].bstack11l1111111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᑔ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11l1111l1l_opy_: bstack11l111llll_opy_ = _111l11lll1_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᑕ")]
            bstack11l1111l1l_opy_.bstack11l1111111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᑖ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111l11llll_opy_
        try:
            if not bstack1l1lll11l_opy_.on() or bstack111l11llll_opy_ != bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᑗ"):
                return
            global bstack1111ll1ll1_opy_
            bstack1111ll1ll1_opy_.start()
            if not _111l11lll1_opy_.get(request.node.nodeid, None):
                _111l11lll1_opy_[request.node.nodeid] = {}
            bstack11l1111l1l_opy_ = bstack11l111llll_opy_.bstack11l111lll1_opy_(
                scenario, feature, request.node,
                name=bstack11l1ll11l1_opy_(request.node, scenario),
                bstack11l11l11l1_opy_=bstack1111111l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᑘ"),
                tags=bstack11l1l1lll1_opy_(feature, scenario)
            )
            _111l11lll1_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᑙ")] = bstack11l1111l1l_opy_
            bstack111l111lll_opy_(bstack11l1111l1l_opy_.uuid)
            bstack1l1lll11l_opy_.bstack111llll11l_opy_(bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑚ"), bstack11l1111l1l_opy_)
        except Exception as err:
            print(bstack1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬᑛ"), str(err))
def bstack111l1l1ll1_opy_(bstack111l111ll1_opy_):
    if bstack111l111ll1_opy_ in store[bstack1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᑜ")]:
        store[bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᑝ")].remove(bstack111l111ll1_opy_)
def bstack111l111lll_opy_(bstack111l111l1l_opy_):
    store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᑞ")] = bstack111l111l1l_opy_
    threading.current_thread().current_test_uuid = bstack111l111l1l_opy_
@bstack1l1lll11l_opy_.bstack111ll111ll_opy_
def bstack111l1111l1_opy_(item, call, report):
    global bstack111l11llll_opy_
    try:
        if report.when == bstack1111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᑟ"):
            bstack1111ll1ll1_opy_.reset()
        if report.when == bstack1111_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᑠ"):
            if bstack111l11llll_opy_ == bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᑡ"):
                _111l11lll1_opy_[item.nodeid][bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᑢ")] = bstack1l11l1l1ll_opy_(report.stop)
                bstack111l1l111l_opy_(item, _111l11lll1_opy_[item.nodeid], bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᑣ"), report, call)
                store[bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᑤ")] = None
            elif bstack111l11llll_opy_ == bstack1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᑥ"):
                bstack11l1111l1l_opy_ = _111l11lll1_opy_[item.nodeid][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᑦ")]
                bstack11l1111l1l_opy_.set(hooks=_111l11lll1_opy_[item.nodeid].get(bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᑧ"), []))
                exception, bstack1l11ll1111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11ll1111_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack11l1111l1l_opy_.stop(time=bstack1l11l1l1ll_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l11ll1111_opy_=bstack1l11ll1111_opy_))
                bstack1l1lll11l_opy_.bstack111llll11l_opy_(bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᑨ"), _111l11lll1_opy_[item.nodeid][bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᑩ")])
        elif report.when in [bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᑪ"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᑫ")]:
            bstack1111lll111_opy_ = item.nodeid + bstack1111_opy_ (u"࠭࠭ࠨᑬ") + report.when
            if report.skipped:
                hook_type = bstack1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᑭ") if report.when == bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᑮ") else bstack1111_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᑯ")
                _111l11lll1_opy_[bstack1111lll111_opy_] = {
                    bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᑰ"): uuid4().__str__(),
                    bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᑱ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1111_opy_ (u"ࠬࡠࠧᑲ"),
                    bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᑳ"): hook_type
                }
            _111l11lll1_opy_[bstack1111lll111_opy_][bstack1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᑴ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1111_opy_ (u"ࠨ࡜ࠪᑵ")
            bstack111l1l1ll1_opy_(_111l11lll1_opy_[bstack1111lll111_opy_][bstack1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᑶ")])
            bstack1111ll1lll_opy_(item, _111l11lll1_opy_[bstack1111lll111_opy_], bstack1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᑷ"), report, call)
            if report.when == bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᑸ"):
                if report.outcome == bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑹ"):
                    bstack111l1l1l11_opy_ = {
                        bstack1111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᑺ"): uuid4().__str__(),
                        bstack1111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᑻ"): bstack1111111l1_opy_(),
                        bstack1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᑼ"): bstack1111111l1_opy_()
                    }
                    _111l11lll1_opy_[item.nodeid] = {**_111l11lll1_opy_[item.nodeid], **bstack111l1l1l11_opy_}
                    bstack111l1l111l_opy_(item, _111l11lll1_opy_[item.nodeid], bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑽ"))
                    bstack111l1l111l_opy_(item, _111l11lll1_opy_[item.nodeid], bstack1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᑾ"), report, call)
    except Exception as err:
        print(bstack1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩᑿ"), str(err))
def bstack111l11ll1l_opy_(test, bstack111l1l1l11_opy_, result=None, call=None, bstack1ll1l1111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l1111l1l_opy_ = {
        bstack1111_opy_ (u"ࠬࡻࡵࡪࡦࠪᒀ"): bstack111l1l1l11_opy_[bstack1111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᒁ")],
        bstack1111_opy_ (u"ࠧࡵࡻࡳࡩࠬᒂ"): bstack1111_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᒃ"),
        bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒄ"): test.name,
        bstack1111_opy_ (u"ࠪࡦࡴࡪࡹࠨᒅ"): {
            bstack1111_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᒆ"): bstack1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᒇ"),
            bstack1111_opy_ (u"࠭ࡣࡰࡦࡨࠫᒈ"): inspect.getsource(test.obj)
        },
        bstack1111_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᒉ"): test.name,
        bstack1111_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧᒊ"): test.name,
        bstack1111_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᒋ"): bstack1l1lll11l_opy_.bstack111llll1ll_opy_(test),
        bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᒌ"): file_path,
        bstack1111_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᒍ"): file_path,
        bstack1111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᒎ"): bstack1111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᒏ"),
        bstack1111_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᒐ"): file_path,
        bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᒑ"): bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᒒ")],
        bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᒓ"): bstack1111_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᒔ"),
        bstack1111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᒕ"): {
            bstack1111_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᒖ"): test.nodeid
        },
        bstack1111_opy_ (u"ࠧࡵࡣࡪࡷࠬᒗ"): bstack1l11l11l11_opy_(test.own_markers)
    }
    if bstack1ll1l1111l_opy_ in [bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᒘ"), bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᒙ")]:
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠪࡱࡪࡺࡡࠨᒚ")] = {
            bstack1111_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᒛ"): bstack111l1l1l11_opy_.get(bstack1111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᒜ"), [])
        }
    if bstack1ll1l1111l_opy_ == bstack1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᒝ"):
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᒞ")] = bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᒟ")
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᒠ")] = bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᒡ")]
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᒢ")] = bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᒣ")]
    if result:
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᒤ")] = result.outcome
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᒥ")] = result.duration * 1000
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᒦ")] = bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᒧ")]
        if result.failed:
            bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᒨ")] = bstack1l1lll11l_opy_.bstack1l11lll11l_opy_(call.excinfo.typename)
            bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᒩ")] = bstack1l1lll11l_opy_.bstack111ll1ll11_opy_(call.excinfo, result)
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᒪ")] = bstack111l1l1l11_opy_[bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᒫ")]
    if outcome:
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᒬ")] = bstack1l11lll1l1_opy_(outcome)
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᒭ")] = 0
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᒮ")] = bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᒯ")]
        if bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᒰ")] == bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᒱ"):
            bstack11l1111l1l_opy_[bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᒲ")] = bstack1111_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᒳ")  # bstack111l11l111_opy_
            bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᒴ")] = [{bstack1111_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᒵ"): [bstack1111_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᒶ")]}]
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᒷ")] = bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᒸ")]
    return bstack11l1111l1l_opy_
def bstack111l11l1l1_opy_(test, bstack111l1l1lll_opy_, bstack1ll1l1111l_opy_, result, call, outcome, bstack111l1ll11l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l1lll_opy_[bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᒹ")]
    hook_name = bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᒺ")]
    hook_data = {
        bstack1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᒻ"): bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᒼ")],
        bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨᒽ"): bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᒾ"),
        bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᒿ"): bstack1111_opy_ (u"࠭ࡻࡾࠩᓀ").format(bstack11l1lll111_opy_(hook_name)),
        bstack1111_opy_ (u"ࠧࡣࡱࡧࡽࠬᓁ"): {
            bstack1111_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᓂ"): bstack1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᓃ"),
            bstack1111_opy_ (u"ࠪࡧࡴࡪࡥࠨᓄ"): None
        },
        bstack1111_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᓅ"): test.name,
        bstack1111_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᓆ"): bstack1l1lll11l_opy_.bstack111llll1ll_opy_(test, hook_name),
        bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᓇ"): file_path,
        bstack1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᓈ"): file_path,
        bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᓉ"): bstack1111_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᓊ"),
        bstack1111_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᓋ"): file_path,
        bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᓌ"): bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᓍ")],
        bstack1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᓎ"): bstack1111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᓏ") if bstack111l11llll_opy_ == bstack1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᓐ") else bstack1111_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᓑ"),
        bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᓒ"): hook_type
    }
    bstack111l1l1111_opy_ = bstack1111lll1ll_opy_(_111l11lll1_opy_.get(test.nodeid, None))
    if bstack111l1l1111_opy_:
        hook_data[bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᓓ")] = bstack111l1l1111_opy_
    if result:
        hook_data[bstack1111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓔ")] = result.outcome
        hook_data[bstack1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᓕ")] = result.duration * 1000
        hook_data[bstack1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᓖ")] = bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓗ")]
        if result.failed:
            hook_data[bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᓘ")] = bstack1l1lll11l_opy_.bstack1l11lll11l_opy_(call.excinfo.typename)
            hook_data[bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᓙ")] = bstack1l1lll11l_opy_.bstack111ll1ll11_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᓚ")] = bstack1l11lll1l1_opy_(outcome)
        hook_data[bstack1111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᓛ")] = 100
        hook_data[bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᓜ")] = bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᓝ")]
        if hook_data[bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᓞ")] == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᓟ"):
            hook_data[bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᓠ")] = bstack1111_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬᓡ")  # bstack111l11l111_opy_
            hook_data[bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᓢ")] = [{bstack1111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᓣ"): [bstack1111_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫᓤ")]}]
    if bstack111l1ll11l_opy_:
        hook_data[bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᓥ")] = bstack111l1ll11l_opy_.result
        hook_data[bstack1111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᓦ")] = bstack1l11lll1ll_opy_(bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᓧ")], bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᓨ")])
        hook_data[bstack1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᓩ")] = bstack111l1l1lll_opy_[bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᓪ")]
        if hook_data[bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᓫ")] == bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᓬ"):
            hook_data[bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᓭ")] = bstack1l1lll11l_opy_.bstack1l11lll11l_opy_(bstack111l1ll11l_opy_.exception_type)
            hook_data[bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᓮ")] = [{bstack1111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᓯ"): bstack1l11l11111_opy_(bstack111l1ll11l_opy_.exception)}]
    return hook_data
def bstack111l1l111l_opy_(test, bstack111l1l1l11_opy_, bstack1ll1l1111l_opy_, result=None, call=None, outcome=None):
    bstack11l1111l1l_opy_ = bstack111l11ll1l_opy_(test, bstack111l1l1l11_opy_, result, call, bstack1ll1l1111l_opy_, outcome)
    driver = getattr(test, bstack1111_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᓰ"), None)
    if bstack1ll1l1111l_opy_ == bstack1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᓱ") and driver:
        bstack11l1111l1l_opy_[bstack1111_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᓲ")] = bstack1l1lll11l_opy_.bstack111l1lllll_opy_(driver)
    if bstack1ll1l1111l_opy_ == bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᓳ"):
        bstack1ll1l1111l_opy_ = bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᓴ")
    bstack111llll1l1_opy_ = {
        bstack1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᓵ"): bstack1ll1l1111l_opy_,
        bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᓶ"): bstack11l1111l1l_opy_
    }
    bstack1l1lll11l_opy_.bstack111l1llll1_opy_(bstack111llll1l1_opy_)
def bstack1111ll1lll_opy_(test, bstack111l1l1l11_opy_, bstack1ll1l1111l_opy_, result=None, call=None, outcome=None, bstack111l1ll11l_opy_=None):
    hook_data = bstack111l11l1l1_opy_(test, bstack111l1l1l11_opy_, bstack1ll1l1111l_opy_, result, call, outcome, bstack111l1ll11l_opy_)
    bstack111llll1l1_opy_ = {
        bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᓷ"): bstack1ll1l1111l_opy_,
        bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨᓸ"): hook_data
    }
    bstack1l1lll11l_opy_.bstack111l1llll1_opy_(bstack111llll1l1_opy_)
def bstack1111lll1ll_opy_(bstack111l1l1l11_opy_):
    if not bstack111l1l1l11_opy_:
        return None
    if bstack111l1l1l11_opy_.get(bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᓹ"), None):
        return getattr(bstack111l1l1l11_opy_[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᓺ")], bstack1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓻ"), None)
    return bstack111l1l1l11_opy_.get(bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᓼ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l1lll11l_opy_.on():
            return
        places = [bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᓽ"), bstack1111_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᓾ"), bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᓿ")]
        bstack111ll1llll_opy_ = []
        for bstack111l11111l_opy_ in places:
            records = caplog.get_records(bstack111l11111l_opy_)
            bstack111l1ll111_opy_ = bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔀ") if bstack111l11111l_opy_ == bstack1111_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᔁ") else bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔂ")
            bstack111l111l11_opy_ = request.node.nodeid + (bstack1111_opy_ (u"ࠪࠫᔃ") if bstack111l11111l_opy_ == bstack1111_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᔄ") else bstack1111_opy_ (u"ࠬ࠳ࠧᔅ") + bstack111l11111l_opy_)
            bstack111l111l1l_opy_ = bstack1111lll1ll_opy_(_111l11lll1_opy_.get(bstack111l111l11_opy_, None))
            if not bstack111l111l1l_opy_:
                continue
            for record in records:
                if bstack1l111ll111_opy_(record.message):
                    continue
                bstack111ll1llll_opy_.append({
                    bstack1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᔆ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1111_opy_ (u"࡛ࠧࠩᔇ"),
                    bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᔈ"): record.levelname,
                    bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔉ"): record.message,
                    bstack111l1ll111_opy_: bstack111l111l1l_opy_
                })
        if len(bstack111ll1llll_opy_) > 0:
            bstack1l1lll11l_opy_.bstack111ll1l111_opy_(bstack111ll1llll_opy_)
    except Exception as err:
        print(bstack1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧᔊ"), str(err))
def bstack111l1l11l1_opy_(driver_command, response):
    if driver_command == bstack1111_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᔋ"):
        bstack1l1lll11l_opy_.bstack111ll11ll1_opy_({
            bstack1111_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᔌ"): response[bstack1111_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᔍ")],
            bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔎ"): store[bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᔏ")]
        })
def bstack1llllll111_opy_():
    global bstack11lll1111_opy_
    bstack1l1lll11l_opy_.bstack111ll1l11l_opy_()
    for driver in bstack11lll1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l11l1l_opy_(self, *args, **kwargs):
    bstack11l1ll1l_opy_ = bstack1l1ll1l11_opy_(self, *args, **kwargs)
    bstack1l1lll11l_opy_.bstack1ll11l111_opy_(self)
    return bstack11l1ll1l_opy_
def bstack1ll1lll1l1_opy_(framework_name):
    global bstack1lll1l1ll_opy_
    global bstack1lll111l1l_opy_
    bstack1lll1l1ll_opy_ = framework_name
    logger.info(bstack11lll1l11_opy_.format(bstack1lll1l1ll_opy_.split(bstack1111_opy_ (u"ࠩ࠰ࠫᔐ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l111l1l11_opy_():
            Service.start = bstack11l1ll11_opy_
            Service.stop = bstack11l11111l_opy_
            webdriver.Remote.__init__ = bstack11111l11l_opy_
            webdriver.Remote.get = bstack111111l1l_opy_
            if not isinstance(os.getenv(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫᔑ")), str):
                return
            WebDriver.close = bstack1l1l111l1_opy_
            WebDriver.quit = bstack1l1ll11ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1lll111ll_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1l1l11111_opy_ = getAccessibilityResultsSummary
        if not bstack1l111l1l11_opy_() and bstack1l1lll11l_opy_.on():
            webdriver.Remote.__init__ = bstack1l1l11l1l_opy_
        bstack1lll111l1l_opy_ = True
    except Exception as e:
        pass
    bstack1l1llll111_opy_()
    if os.environ.get(bstack1111_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᔒ")):
        bstack1lll111l1l_opy_ = eval(os.environ.get(bstack1111_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᔓ")))
    if not bstack1lll111l1l_opy_:
        bstack1ll1l1l111_opy_(bstack1111_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣᔔ"), bstack1l1llll1l_opy_)
    if bstack1lllll11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack111l11l1_opy_
        except Exception as e:
            logger.error(bstack1ll111ll11_opy_.format(str(e)))
    if bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᔕ") in str(framework_name).lower():
        if not bstack1l111l1l11_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll11111ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1l11lll_opy_
            Config.getoption = bstack111lll11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l11l1l11_opy_
        except Exception as e:
            pass
def bstack1l1ll11ll_opy_(self):
    global bstack1lll1l1ll_opy_
    global bstack1lll1ll1_opy_
    global bstack1ll1l1l1l_opy_
    try:
        if bstack1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᔖ") in bstack1lll1l1ll_opy_ and self.session_id != None and bstack1ll111l111_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᔗ"), bstack1111_opy_ (u"ࠪࠫᔘ")) != bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᔙ"):
            bstack111111ll1_opy_ = bstack1111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᔚ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᔛ")
            bstack11l11l11_opy_ = bstack1llll1lll1_opy_(bstack1111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᔜ"), bstack1111_opy_ (u"ࠨࠩᔝ"), bstack111111ll1_opy_, bstack1111_opy_ (u"ࠩ࠯ࠤࠬᔞ").join(
                threading.current_thread().bstackTestErrorMessages), bstack1111_opy_ (u"ࠪࠫᔟ"), bstack1111_opy_ (u"ࠫࠬᔠ"))
            bstack11l1ll11l_opy_(logger, True)
            if self != None:
                self.execute_script(bstack11l11l11_opy_)
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨᔡ") + str(e))
    bstack1ll1l1l1l_opy_(self)
    self.session_id = None
def bstack11111l11l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll1ll1_opy_
    global bstack1ll111lll_opy_
    global bstack1lll1l1l1_opy_
    global bstack1lll1l1ll_opy_
    global bstack1l1ll1l11_opy_
    global bstack11lll1111_opy_
    global bstack11l11l11l_opy_
    global bstack1ll1ll1l11_opy_
    global bstack111l1111ll_opy_
    global bstack111l1lll11_opy_
    CONFIG[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᔢ")] = str(bstack1lll1l1ll_opy_) + str(__version__)
    command_executor = bstack1l1111ll_opy_(bstack11l11l11l_opy_)
    logger.debug(bstack111l1111l_opy_.format(command_executor))
    proxy = bstack1ll1llll_opy_(CONFIG, proxy)
    bstack1ll111ll1_opy_ = 0
    try:
        if bstack1lll1l1l1_opy_ is True:
            bstack1ll111ll1_opy_ = int(os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᔣ")))
    except:
        bstack1ll111ll1_opy_ = 0
    bstack1ll11llll_opy_ = bstack1ll1ll1lll_opy_(CONFIG, bstack1ll111ll1_opy_)
    logger.debug(bstack111l1ll1_opy_.format(str(bstack1ll11llll_opy_)))
    bstack111l1lll11_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᔤ"))[bstack1ll111ll1_opy_]
    if bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᔥ") in CONFIG and CONFIG[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᔦ")]:
        bstack1lll1l1111_opy_(bstack1ll11llll_opy_, bstack1ll1ll1l11_opy_)
    if desired_capabilities:
        bstack1ll1l11111_opy_ = bstack11lllll1_opy_(desired_capabilities)
        bstack1ll1l11111_opy_[bstack1111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᔧ")] = bstack1lll11l1_opy_(CONFIG)
        bstack1111l1ll_opy_ = bstack1ll1ll1lll_opy_(bstack1ll1l11111_opy_)
        if bstack1111l1ll_opy_:
            bstack1ll11llll_opy_ = update(bstack1111l1ll_opy_, bstack1ll11llll_opy_)
        desired_capabilities = None
    if options:
        bstack1l1111lll_opy_(options, bstack1ll11llll_opy_)
    if not options:
        options = bstack111l1lll1_opy_(bstack1ll11llll_opy_)
    if bstack111ll1l1l_opy_.bstack1llll11l11_opy_(CONFIG, bstack1ll111ll1_opy_) and bstack111ll1l1l_opy_.bstack1lll11l111_opy_(bstack1ll11llll_opy_, options):
        bstack111l1111ll_opy_ = True
        bstack111ll1l1l_opy_.set_capabilities(bstack1ll11llll_opy_, CONFIG)
    if proxy and bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᔨ")):
        options.proxy(proxy)
    if options and bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᔩ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1llll1ll1_opy_() < version.parse(bstack1111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᔪ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll11llll_opy_)
    logger.info(bstack1l1l1ll1l_opy_)
    if bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᔫ")):
        bstack1l1ll1l11_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᔬ")):
        bstack1l1ll1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᔭ")):
        bstack1l1ll1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1ll1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11l1l111l_opy_ = bstack1111_opy_ (u"ࠫࠬᔮ")
        if bstack1llll1ll1_opy_() >= version.parse(bstack1111_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ᔯ")):
            bstack11l1l111l_opy_ = self.caps.get(bstack1111_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᔰ"))
        else:
            bstack11l1l111l_opy_ = self.capabilities.get(bstack1111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᔱ"))
        if bstack11l1l111l_opy_:
            bstack1l11ll111_opy_(bstack11l1l111l_opy_)
            if bstack1llll1ll1_opy_() <= version.parse(bstack1111_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᔲ")):
                self.command_executor._url = bstack1111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᔳ") + bstack11l11l11l_opy_ + bstack1111_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᔴ")
            else:
                self.command_executor._url = bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᔵ") + bstack11l1l111l_opy_ + bstack1111_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨᔶ")
            logger.debug(bstack111ll1ll1_opy_.format(bstack11l1l111l_opy_))
        else:
            logger.debug(bstack1ll1l1lll_opy_.format(bstack1111_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᔷ")))
    except Exception as e:
        logger.debug(bstack1ll1l1lll_opy_.format(e))
    bstack1lll1ll1_opy_ = self.session_id
    if bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᔸ") in bstack1lll1l1ll_opy_:
        threading.current_thread().bstack1ll1l11l1l_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1l1lll11l_opy_.bstack1ll11l111_opy_(self)
    bstack11lll1111_opy_.append(self)
    if bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᔹ") in CONFIG and bstack1111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᔺ") in CONFIG[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᔻ")][bstack1ll111ll1_opy_]:
        bstack1ll111lll_opy_ = CONFIG[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᔼ")][bstack1ll111ll1_opy_][bstack1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᔽ")]
    logger.debug(bstack1ll1lllll1_opy_.format(bstack1lll1ll1_opy_))
def bstack111111l1l_opy_(self, url):
    global bstack1ll1ll1111_opy_
    global CONFIG
    try:
        bstack1ll111lll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l111l111_opy_.format(str(err)))
    try:
        bstack1ll1ll1111_opy_(self, url)
    except Exception as e:
        try:
            bstack1l11ll1l1_opy_ = str(e)
            if any(err_msg in bstack1l11ll1l1_opy_ for err_msg in bstack1ll111l11_opy_):
                bstack1ll111lll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l111l111_opy_.format(str(err)))
        raise e
def bstack1llll11ll_opy_(item, when):
    global bstack111llll11_opy_
    try:
        bstack111llll11_opy_(item, when)
    except Exception as e:
        pass
def bstack1l11l1l11_opy_(item, call, rep):
    global bstack11111l11_opy_
    global bstack11lll1111_opy_
    name = bstack1111_opy_ (u"࠭ࠧᔾ")
    try:
        if rep.when == bstack1111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᔿ"):
            bstack1lll1ll1_opy_ = threading.current_thread().bstack1ll1l11l1l_opy_
            bstack111l111111_opy_ = item.config.getoption(bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᕀ"))
            try:
                if (str(bstack111l111111_opy_).lower() != bstack1111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᕁ")):
                    name = str(rep.nodeid)
                    bstack11l11l11_opy_ = bstack1llll1lll1_opy_(bstack1111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᕂ"), name, bstack1111_opy_ (u"ࠫࠬᕃ"), bstack1111_opy_ (u"ࠬ࠭ᕄ"), bstack1111_opy_ (u"࠭ࠧᕅ"), bstack1111_opy_ (u"ࠧࠨᕆ"))
                    os.environ[bstack1111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᕇ")] = name
                    for driver in bstack11lll1111_opy_:
                        if bstack1lll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11l11_opy_)
            except Exception as e:
                logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᕈ").format(str(e)))
            try:
                bstack111l11ll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᕉ"):
                    status = bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᕊ") if rep.outcome.lower() == bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᕋ") else bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᕌ")
                    reason = bstack1111_opy_ (u"ࠧࠨᕍ")
                    if status == bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᕎ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1111_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᕏ") if status == bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᕐ") else bstack1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᕑ")
                    data = name + bstack1111_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧᕒ") if status == bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᕓ") else name + bstack1111_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪᕔ") + reason
                    bstack1l11lll1_opy_ = bstack1llll1lll1_opy_(bstack1111_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᕕ"), bstack1111_opy_ (u"ࠩࠪᕖ"), bstack1111_opy_ (u"ࠪࠫᕗ"), bstack1111_opy_ (u"ࠫࠬᕘ"), level, data)
                    for driver in bstack11lll1111_opy_:
                        if bstack1lll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11lll1_opy_)
            except Exception as e:
                logger.debug(bstack1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᕙ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪᕚ").format(str(e)))
    bstack11111l11_opy_(item, call, rep)
notset = Notset()
def bstack111lll11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1111l11l_opy_
    if str(name).lower() == bstack1111_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᕛ"):
        return bstack1111_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᕜ")
    else:
        return bstack1111l11l_opy_(self, name, default, skip)
def bstack111l11l1_opy_(self):
    global CONFIG
    global bstack1ll11l1ll_opy_
    try:
        proxy = bstack111ll1111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1111_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᕝ")):
                proxies = bstack111llllll_opy_(proxy, bstack1l1111ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll11lll11_opy_ = proxies.popitem()
                    if bstack1111_opy_ (u"ࠥ࠾࠴࠵ࠢᕞ") in bstack1ll11lll11_opy_:
                        return bstack1ll11lll11_opy_
                    else:
                        return bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᕟ") + bstack1ll11lll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤᕠ").format(str(e)))
    return bstack1ll11l1ll_opy_(self)
def bstack1lllll11_opy_():
    return (bstack1111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᕡ") in CONFIG or bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᕢ") in CONFIG) and bstack1111ll111_opy_() and bstack1llll1ll1_opy_() >= version.parse(
        bstack111111111_opy_)
def bstack11lll111_opy_(self,
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
    global bstack1ll111lll_opy_
    global bstack1lll1l1l1_opy_
    global bstack1lll1l1ll_opy_
    CONFIG[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᕣ")] = str(bstack1lll1l1ll_opy_) + str(__version__)
    bstack1ll111ll1_opy_ = 0
    try:
        if bstack1lll1l1l1_opy_ is True:
            bstack1ll111ll1_opy_ = int(os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᕤ")))
    except:
        bstack1ll111ll1_opy_ = 0
    CONFIG[bstack1111_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᕥ")] = True
    bstack1ll11llll_opy_ = bstack1ll1ll1lll_opy_(CONFIG, bstack1ll111ll1_opy_)
    logger.debug(bstack111l1ll1_opy_.format(str(bstack1ll11llll_opy_)))
    if CONFIG.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᕦ")):
        bstack1lll1l1111_opy_(bstack1ll11llll_opy_, bstack1ll1ll1l11_opy_)
    if bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᕧ") in CONFIG and bstack1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᕨ") in CONFIG[bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕩ")][bstack1ll111ll1_opy_]:
        bstack1ll111lll_opy_ = CONFIG[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᕪ")][bstack1ll111ll1_opy_][bstack1111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᕫ")]
    import urllib
    import json
    bstack111111lll_opy_ = bstack1111_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬᕬ") + urllib.parse.quote(json.dumps(bstack1ll11llll_opy_))
    browser = self.connect(bstack111111lll_opy_)
    return browser
def bstack1l1llll111_opy_():
    global bstack1lll111l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11lll111_opy_
        bstack1lll111l1l_opy_ = True
    except Exception as e:
        pass
def bstack1111lllll1_opy_():
    global CONFIG
    global bstack11llll11_opy_
    global bstack11l11l11l_opy_
    global bstack1ll1ll1l11_opy_
    global bstack1lll1l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪᕭ")))
    bstack11llll11_opy_ = eval(os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᕮ")))
    bstack11l11l11l_opy_ = os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ᕯ"))
    bstack11l1lllll_opy_(CONFIG, bstack11llll11_opy_)
    bstack111l111ll_opy_()
    global bstack1l1ll1l11_opy_
    global bstack1ll1l1l1l_opy_
    global bstack1lll11lll_opy_
    global bstack1ll11ll111_opy_
    global bstack11llll1l1_opy_
    global bstack1ll1ll1l1_opy_
    global bstack11l1111l1_opy_
    global bstack1ll1ll1111_opy_
    global bstack1ll11l1ll_opy_
    global bstack1111l11l_opy_
    global bstack111llll11_opy_
    global bstack11111l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1ll1l11_opy_ = webdriver.Remote.__init__
        bstack1ll1l1l1l_opy_ = WebDriver.quit
        bstack11l1111l1_opy_ = WebDriver.close
        bstack1ll1ll1111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᕰ") in CONFIG or bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᕱ") in CONFIG) and bstack1111ll111_opy_():
        if bstack1llll1ll1_opy_() < version.parse(bstack111111111_opy_):
            logger.error(bstack1l1ll1l1l_opy_.format(bstack1llll1ll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1ll11l1ll_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1ll111ll11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1111l11l_opy_ = Config.getoption
        from _pytest import runner
        bstack111llll11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack111lllll_opy_)
    try:
        from pytest_bdd import reporting
        bstack11111l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪᕲ"))
    bstack1ll1ll1l11_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᕳ"), {}).get(bstack1111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᕴ"))
    bstack1lll1l1l1_opy_ = True
    bstack1ll1lll1l1_opy_(bstack1l11l11ll_opy_)
if (bstack1l11l1lll1_opy_()):
    bstack1111lllll1_opy_()
@bstack1l1l1ll1ll_opy_(class_method=False)
def bstack111l1l11ll_opy_(hook_name, event, bstack1111ll1l1l_opy_=None):
    if hook_name not in [bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᕵ"), bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᕶ"), bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᕷ"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᕸ"), bstack1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᕹ"), bstack1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᕺ"), bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᕻ"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᕼ")]:
        return
    node = store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᕽ")]
    if hook_name in [bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᕾ"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᕿ")]:
        node = store[bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᖀ")]
    elif hook_name in [bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᖁ"), bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᖂ")]:
        node = store[bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᖃ")]
    if event == bstack1111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᖄ"):
        hook_type = bstack11l1ll1ll1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack111l1l1lll_opy_ = {
            bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᖅ"): uuid,
            bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᖆ"): bstack1111111l1_opy_(),
            bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᖇ"): bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᖈ"),
            bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᖉ"): hook_type,
            bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᖊ"): hook_name
        }
        store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖋ")].append(uuid)
        bstack111l1ll1l1_opy_ = node.nodeid
        if hook_type == bstack1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖌ"):
            if not _111l11lll1_opy_.get(bstack111l1ll1l1_opy_, None):
                _111l11lll1_opy_[bstack111l1ll1l1_opy_] = {bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᖍ"): []}
            _111l11lll1_opy_[bstack111l1ll1l1_opy_][bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᖎ")].append(bstack111l1l1lll_opy_[bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖏ")])
        _111l11lll1_opy_[bstack111l1ll1l1_opy_ + bstack1111_opy_ (u"ࠫ࠲࠭ᖐ") + hook_name] = bstack111l1l1lll_opy_
        bstack1111ll1lll_opy_(node, bstack111l1l1lll_opy_, bstack1111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᖑ"))
    elif event == bstack1111_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᖒ"):
        bstack1111lll111_opy_ = node.nodeid + bstack1111_opy_ (u"ࠧ࠮ࠩᖓ") + hook_name
        _111l11lll1_opy_[bstack1111lll111_opy_][bstack1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᖔ")] = bstack1111111l1_opy_()
        bstack111l1l1ll1_opy_(_111l11lll1_opy_[bstack1111lll111_opy_][bstack1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖕ")])
        bstack1111ll1lll_opy_(node, _111l11lll1_opy_[bstack1111lll111_opy_], bstack1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᖖ"), bstack111l1ll11l_opy_=bstack1111ll1l1l_opy_)
def bstack1111llll1l_opy_():
    global bstack111l11llll_opy_
    if bstack111l1ll11_opy_():
        bstack111l11llll_opy_ = bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᖗ")
    else:
        bstack111l11llll_opy_ = bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᖘ")
@bstack1l1lll11l_opy_.bstack111ll111ll_opy_
def bstack111l1ll1ll_opy_():
    bstack1111llll1l_opy_()
    if bstack1111ll111_opy_():
        bstack11l11ll1l1_opy_(bstack111l1l11l1_opy_)
    bstack11lllllll1_opy_ = bstack1l111111ll_opy_(bstack111l1l11ll_opy_)
bstack111l1ll1ll_opy_()