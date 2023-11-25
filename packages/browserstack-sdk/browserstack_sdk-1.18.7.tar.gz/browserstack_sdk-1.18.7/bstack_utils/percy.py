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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1lllll11ll_opy_, bstack11l1l11l1_opy_
class bstack1l111ll11_opy_:
  working_dir = os.getcwd()
  bstack11l11l1ll_opy_ = False
  config = {}
  binary_path = bstack11lll1l_opy_ (u"ࠧࠨᇔ")
  bstack11ll11l11l_opy_ = bstack11lll1l_opy_ (u"ࠨࠩᇕ")
  bstack11lll1ll1l_opy_ = False
  bstack11ll1111l1_opy_ = None
  bstack11lll111ll_opy_ = {}
  bstack11ll1ll1l1_opy_ = 300
  bstack11ll1ll1ll_opy_ = False
  logger = None
  bstack11ll11l1ll_opy_ = False
  bstack11lll1111l_opy_ = bstack11lll1l_opy_ (u"ࠩࠪᇖ")
  bstack11ll11ll1l_opy_ = {
    bstack11lll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᇗ") : 1,
    bstack11lll1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᇘ") : 2,
    bstack11lll1l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᇙ") : 3,
    bstack11lll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ᇚ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11ll1ll111_opy_(self):
    bstack11ll1l11ll_opy_ = bstack11lll1l_opy_ (u"ࠧࠨᇛ")
    bstack11lll1l111_opy_ = sys.platform
    bstack11lll11111_opy_ = bstack11lll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᇜ")
    if re.match(bstack11lll1l_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤᇝ"), bstack11lll1l111_opy_) != None:
      bstack11ll1l11ll_opy_ = bstack1l11llll1l_opy_ + bstack11lll1l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦᇞ")
      self.bstack11lll1111l_opy_ = bstack11lll1l_opy_ (u"ࠫࡲࡧࡣࠨᇟ")
    elif re.match(bstack11lll1l_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥᇠ"), bstack11lll1l111_opy_) != None:
      bstack11ll1l11ll_opy_ = bstack1l11llll1l_opy_ + bstack11lll1l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢᇡ")
      bstack11lll11111_opy_ = bstack11lll1l_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥᇢ")
      self.bstack11lll1111l_opy_ = bstack11lll1l_opy_ (u"ࠨࡹ࡬ࡲࠬᇣ")
    else:
      bstack11ll1l11ll_opy_ = bstack1l11llll1l_opy_ + bstack11lll1l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧᇤ")
      self.bstack11lll1111l_opy_ = bstack11lll1l_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᇥ")
    return bstack11ll1l11ll_opy_, bstack11lll11111_opy_
  def bstack11llll1l11_opy_(self):
    try:
      bstack11ll11l111_opy_ = [os.path.join(expanduser(bstack11lll1l_opy_ (u"ࠦࢃࠨᇦ")), bstack11lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᇧ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11ll11l111_opy_:
        if(self.bstack11ll111lll_opy_(path)):
          return path
      raise bstack11lll1l_opy_ (u"ࠨࡕ࡯ࡣ࡯ࡦࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᇨ")
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤᇩ").format(e))
  def bstack11ll111lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11ll1l1lll_opy_(self, bstack11ll1l11ll_opy_, bstack11lll11111_opy_):
    try:
      bstack11ll1111ll_opy_ = self.bstack11llll1l11_opy_()
      bstack11ll1l1l1l_opy_ = os.path.join(bstack11ll1111ll_opy_, bstack11lll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫᇪ"))
      bstack11ll11111l_opy_ = os.path.join(bstack11ll1111ll_opy_, bstack11lll11111_opy_)
      if os.path.exists(bstack11ll11111l_opy_):
        self.logger.info(bstack11lll1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᇫ").format(bstack11ll11111l_opy_))
        return bstack11ll11111l_opy_
      if os.path.exists(bstack11ll1l1l1l_opy_):
        self.logger.info(bstack11lll1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣᇬ").format(bstack11ll1l1l1l_opy_))
        return self.bstack11ll111ll1_opy_(bstack11ll1l1l1l_opy_, bstack11lll11111_opy_)
      self.logger.info(bstack11lll1l_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤᇭ").format(bstack11ll1l11ll_opy_))
      response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"ࠬࡍࡅࡕࠩᇮ"), bstack11ll1l11ll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11ll1l1l1l_opy_, bstack11lll1l_opy_ (u"࠭ࡷࡣࠩᇯ")) as file:
          file.write(response.content)
        self.logger.info(bstack11ll1lllll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࡦ࡮ࡴࡡࡳࡻࡢࡾ࡮ࡶ࡟ࡱࡣࡷ࡬ࢂࠨᇰ"))
        return self.bstack11ll111ll1_opy_(bstack11ll1l1l1l_opy_, bstack11lll11111_opy_)
      else:
        raise(bstack11ll1lllll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࡸࡺࡡࡵࡷࡶࡣࡨࡵࡤࡦࡿࠥᇱ"))
    except:
      self.logger.error(bstack11lll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᇲ"))
  def bstack11llll11ll_opy_(self, bstack11ll1l11ll_opy_, bstack11lll11111_opy_):
    try:
      bstack11ll11111l_opy_ = self.bstack11ll1l1lll_opy_(bstack11ll1l11ll_opy_, bstack11lll11111_opy_)
      bstack11lll111l1_opy_ = self.bstack11lll1l1l1_opy_(bstack11ll1l11ll_opy_, bstack11lll11111_opy_, bstack11ll11111l_opy_)
      return bstack11ll11111l_opy_, bstack11lll111l1_opy_
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢᇳ").format(e))
    return bstack11ll11111l_opy_, False
  def bstack11lll1l1l1_opy_(self, bstack11ll1l11ll_opy_, bstack11lll11111_opy_, bstack11ll11111l_opy_, bstack11ll1l1111_opy_ = 0):
    if bstack11ll1l1111_opy_ > 1:
      return False
    if bstack11ll11111l_opy_ == None or os.path.exists(bstack11ll11111l_opy_) == False:
      self.logger.warn(bstack11lll1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᇴ"))
      bstack11ll11111l_opy_ = self.bstack11ll1l1lll_opy_(bstack11ll1l11ll_opy_, bstack11lll11111_opy_)
      self.bstack11lll1l1l1_opy_(bstack11ll1l11ll_opy_, bstack11lll11111_opy_, bstack11ll11111l_opy_, bstack11ll1l1111_opy_+1)
    bstack11ll11ll11_opy_ = bstack11lll1l_opy_ (u"ࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࡝࠱ࡦࡰ࡮ࠦ࡜ࡥ࠰࡟ࡨ࠰࠴࡜ࡥ࠭ࠥᇵ")
    command = bstack11lll1l_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬᇶ").format(bstack11ll11111l_opy_)
    bstack11llll1111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11ll11ll11_opy_, bstack11llll1111_opy_) != None:
      return True
    else:
      self.logger.error(bstack11lll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨᇷ"))
      bstack11ll11111l_opy_ = self.bstack11ll1l1lll_opy_(bstack11ll1l11ll_opy_, bstack11lll11111_opy_)
      self.bstack11lll1l1l1_opy_(bstack11ll1l11ll_opy_, bstack11lll11111_opy_, bstack11ll11111l_opy_, bstack11ll1l1111_opy_+1)
  def bstack11ll111ll1_opy_(self, bstack11ll1l1l1l_opy_, bstack11lll11111_opy_):
    try:
      working_dir = os.path.dirname(bstack11ll1l1l1l_opy_)
      shutil.unpack_archive(bstack11ll1l1l1l_opy_, working_dir)
      bstack11ll11111l_opy_ = os.path.join(working_dir, bstack11lll11111_opy_)
      os.chmod(bstack11ll11111l_opy_, 0o755)
      return bstack11ll11111l_opy_
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᇸ"))
  def bstack11lll1llll_opy_(self):
    try:
      percy = str(self.config.get(bstack11lll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᇹ"), bstack11lll1l_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤᇺ"))).lower()
      if percy != bstack11lll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᇻ"):
        return False
      self.bstack11lll1ll1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᇼ").format(e))
  def init(self, bstack11l11l1ll_opy_, config, logger):
    self.bstack11l11l1ll_opy_ = bstack11l11l1ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11lll1llll_opy_():
      return
    self.bstack11lll111ll_opy_ = config.get(bstack11lll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᇽ"), {})
    try:
      bstack11ll1l11ll_opy_, bstack11lll11111_opy_ = self.bstack11ll1ll111_opy_()
      bstack11ll11111l_opy_, bstack11lll111l1_opy_ = self.bstack11llll11ll_opy_(bstack11ll1l11ll_opy_, bstack11lll11111_opy_)
      if bstack11lll111l1_opy_:
        self.binary_path = bstack11ll11111l_opy_
        thread = Thread(target=self.bstack11ll1l111l_opy_)
        thread.start()
      else:
        self.bstack11ll11l1ll_opy_ = True
        self.logger.error(bstack11lll1l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᇾ").format(bstack11ll11111l_opy_))
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᇿ").format(e))
  def bstack11ll1l1ll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11lll1l_opy_ (u"ࠩ࡯ࡳ࡬࠭ሀ"), bstack11lll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭ሁ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11lll1l_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣሂ").format(logfile))
      self.bstack11ll11l11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨሃ").format(e))
  def bstack11ll1l111l_opy_(self):
    bstack11llll111l_opy_ = self.bstack11ll111l11_opy_()
    if bstack11llll111l_opy_ == None:
      self.bstack11ll11l1ll_opy_ = True
      self.logger.error(bstack11lll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤሄ"))
      return False
    command_args = [bstack11lll1l_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣህ") if self.bstack11l11l1ll_opy_ else bstack11lll1l_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬሆ")]
    bstack11ll111l1l_opy_ = self.bstack11llll11l1_opy_()
    if bstack11ll111l1l_opy_ != None:
      command_args.append(bstack11lll1l_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣሇ").format(bstack11ll111l1l_opy_))
    env = os.environ.copy()
    env[bstack11lll1l_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣለ")] = bstack11llll111l_opy_
    bstack11lll11lll_opy_ = [self.binary_path]
    self.bstack11ll1l1ll1_opy_()
    self.bstack11ll1111l1_opy_ = self.bstack11ll1llll1_opy_(bstack11lll11lll_opy_ + command_args, env)
    self.logger.debug(bstack11lll1l_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧሉ"))
    bstack11ll1l1111_opy_ = 0
    while self.bstack11ll1111l1_opy_.poll() == None:
      bstack11lll11ll1_opy_ = self.bstack11lll11l11_opy_()
      if bstack11lll11ll1_opy_:
        self.logger.debug(bstack11lll1l_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣሊ"))
        self.bstack11ll1ll1ll_opy_ = True
        return True
      bstack11ll1l1111_opy_ += 1
      self.logger.debug(bstack11lll1l_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤላ").format(bstack11ll1l1111_opy_))
      time.sleep(2)
    self.logger.error(bstack11lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧሌ").format(bstack11ll1l1111_opy_))
    self.bstack11ll11l1ll_opy_ = True
    return False
  def bstack11lll11l11_opy_(self, bstack11ll1l1111_opy_ = 0):
    try:
      if bstack11ll1l1111_opy_ > 10:
        return False
      bstack11ll11l1l1_opy_ = os.environ.get(bstack11lll1l_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨል"), bstack11lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪሎ"))
      bstack11lll1l1ll_opy_ = bstack11ll11l1l1_opy_ + bstack1l11llllll_opy_
      response = requests.get(bstack11lll1l1ll_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11ll111l11_opy_(self):
    bstack11lll1lll1_opy_ = bstack11lll1l_opy_ (u"ࠪࡥࡵࡶࠧሏ") if self.bstack11l11l1ll_opy_ else bstack11lll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ሐ")
    bstack1l111l11l1_opy_ = bstack11lll1l_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠦሑ").format(self.config[bstack11lll1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫሒ")], bstack11lll1lll1_opy_)
    uri = bstack1lllll11ll_opy_(bstack1l111l11l1_opy_)
    try:
      response = bstack11l1l11l1_opy_(bstack11lll1l_opy_ (u"ࠧࡈࡇࡗࠫሓ"), uri, {}, {bstack11lll1l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ሔ"): (self.config[bstack11lll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫሕ")], self.config[bstack11lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ሖ")])})
      if response.status_code == 200:
        bstack11ll1l1l11_opy_ = response.json()
        if bstack11lll1l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥሗ") in bstack11ll1l1l11_opy_:
          return bstack11ll1l1l11_opy_[bstack11lll1l_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦመ")]
        else:
          raise bstack11lll1l_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ሙ").format(bstack11ll1l1l11_opy_)
      else:
        raise bstack11lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢሚ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤማ").format(e))
  def bstack11llll11l1_opy_(self):
    bstack11ll1lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1l_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧሜ"))
    try:
      if bstack11lll1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫም") not in self.bstack11lll111ll_opy_:
        self.bstack11lll111ll_opy_[bstack11lll1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬሞ")] = 2
      with open(bstack11ll1lll1l_opy_, bstack11lll1l_opy_ (u"ࠬࡽࠧሟ")) as fp:
        json.dump(self.bstack11lll111ll_opy_, fp)
      return bstack11ll1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨሠ").format(e))
  def bstack11ll1llll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11lll1111l_opy_ == bstack11lll1l_opy_ (u"ࠧࡸ࡫ࡱࠫሡ"):
        bstack11ll1l11l1_opy_ = [bstack11lll1l_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩሢ"), bstack11lll1l_opy_ (u"ࠩ࠲ࡧࠬሣ")]
        cmd = bstack11ll1l11l1_opy_ + cmd
      cmd = bstack11lll1l_opy_ (u"ࠪࠤࠬሤ").join(cmd)
      self.logger.debug(bstack11lll1l_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣሥ").format(cmd))
      with open(self.bstack11ll11l11l_opy_, bstack11lll1l_opy_ (u"ࠧࡧࠢሦ")) as bstack11ll11lll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11ll11lll1_opy_, text=True, stderr=bstack11ll11lll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11ll11l1ll_opy_ = True
      self.logger.error(bstack11lll1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣሧ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11ll1ll1ll_opy_:
        self.logger.info(bstack11lll1l_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣረ"))
        cmd = [self.binary_path, bstack11lll1l_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦሩ")]
        self.bstack11ll1llll1_opy_(cmd)
        self.bstack11ll1ll1ll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤሪ").format(cmd, e))
  def bstack111l111l_opy_(self):
    if not self.bstack11lll1ll1l_opy_:
      return
    try:
      bstack11lll1ll11_opy_ = 0
      while not self.bstack11ll1ll1ll_opy_ and bstack11lll1ll11_opy_ < self.bstack11ll1ll1l1_opy_:
        if self.bstack11ll11l1ll_opy_:
          self.logger.info(bstack11lll1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣራ"))
          return
        time.sleep(1)
        bstack11lll1ll11_opy_ += 1
      os.environ[bstack11lll1l_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪሬ")] = str(self.bstack11ll1lll11_opy_())
      self.logger.info(bstack11lll1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨር"))
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢሮ").format(e))
  def bstack11ll1lll11_opy_(self):
    if self.bstack11l11l1ll_opy_:
      return
    try:
      bstack11ll1ll11l_opy_ = [platform[bstack11lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬሯ")].lower() for platform in self.config.get(bstack11lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫሰ"), [])]
      bstack11ll11llll_opy_ = sys.maxsize
      bstack11lll11l1l_opy_ = bstack11lll1l_opy_ (u"ࠩࠪሱ")
      for browser in bstack11ll1ll11l_opy_:
        if browser in self.bstack11ll11ll1l_opy_:
          bstack11lll1l11l_opy_ = self.bstack11ll11ll1l_opy_[browser]
        if bstack11lll1l11l_opy_ < bstack11ll11llll_opy_:
          bstack11ll11llll_opy_ = bstack11lll1l11l_opy_
          bstack11lll11l1l_opy_ = browser
      return bstack11lll11l1l_opy_
    except Exception as e:
      self.logger.error(bstack11lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦሲ").format(e))