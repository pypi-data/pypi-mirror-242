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
from bstack_utils.helper import bstack1ll11l11_opy_, bstack1ll1111l_opy_
class bstack1llll111ll_opy_:
  working_dir = os.getcwd()
  bstack1l1ll11l1_opy_ = False
  config = {}
  binary_path = bstack1111_opy_ (u"࠭ࠧᇓ")
  bstack11ll1ll111_opy_ = bstack1111_opy_ (u"ࠧࠨᇔ")
  bstack11ll1l1l11_opy_ = False
  bstack11ll1l11ll_opy_ = None
  bstack11ll1l1ll1_opy_ = {}
  bstack11ll11lll1_opy_ = 300
  bstack11ll111l11_opy_ = False
  logger = None
  bstack11ll1lllll_opy_ = False
  bstack11ll11111l_opy_ = bstack1111_opy_ (u"ࠨࠩᇕ")
  bstack11ll11llll_opy_ = {
    bstack1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᇖ") : 1,
    bstack1111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫᇗ") : 2,
    bstack1111_opy_ (u"ࠫࡪࡪࡧࡦࠩᇘ") : 3,
    bstack1111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬᇙ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11lll1l1ll_opy_(self):
    bstack11ll1llll1_opy_ = bstack1111_opy_ (u"࠭ࠧᇚ")
    bstack11lll1lll1_opy_ = sys.platform
    bstack11ll1l11l1_opy_ = bstack1111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᇛ")
    if re.match(bstack1111_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣᇜ"), bstack11lll1lll1_opy_) != None:
      bstack11ll1llll1_opy_ = bstack1l1l111111_opy_ + bstack1111_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥᇝ")
      self.bstack11ll11111l_opy_ = bstack1111_opy_ (u"ࠪࡱࡦࡩࠧᇞ")
    elif re.match(bstack1111_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤᇟ"), bstack11lll1lll1_opy_) != None:
      bstack11ll1llll1_opy_ = bstack1l1l111111_opy_ + bstack1111_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨᇠ")
      bstack11ll1l11l1_opy_ = bstack1111_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤᇡ")
      self.bstack11ll11111l_opy_ = bstack1111_opy_ (u"ࠧࡸ࡫ࡱࠫᇢ")
    else:
      bstack11ll1llll1_opy_ = bstack1l1l111111_opy_ + bstack1111_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦᇣ")
      self.bstack11ll11111l_opy_ = bstack1111_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨᇤ")
    return bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_
  def bstack11lll1llll_opy_(self):
    try:
      bstack11llll11l1_opy_ = [os.path.join(expanduser(bstack1111_opy_ (u"ࠥࢂࠧᇥ")), bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᇦ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11llll11l1_opy_:
        if(self.bstack11ll11ll1l_opy_(path)):
          return path
      raise bstack1111_opy_ (u"࡛ࠧ࡮ࡢ࡮ࡥࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᇧ")
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣᇨ").format(e))
  def bstack11ll11ll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11ll1ll1ll_opy_(self, bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_):
    try:
      bstack11lll1l1l1_opy_ = self.bstack11lll1llll_opy_()
      bstack11lll111ll_opy_ = os.path.join(bstack11lll1l1l1_opy_, bstack1111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪᇩ"))
      bstack11ll1111l1_opy_ = os.path.join(bstack11lll1l1l1_opy_, bstack11ll1l11l1_opy_)
      if os.path.exists(bstack11ll1111l1_opy_):
        self.logger.info(bstack1111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᇪ").format(bstack11ll1111l1_opy_))
        return bstack11ll1111l1_opy_
      if os.path.exists(bstack11lll111ll_opy_):
        self.logger.info(bstack1111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢᇫ").format(bstack11lll111ll_opy_))
        return self.bstack11lll1l111_opy_(bstack11lll111ll_opy_, bstack11ll1l11l1_opy_)
      self.logger.info(bstack1111_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣᇬ").format(bstack11ll1llll1_opy_))
      response = bstack1ll1111l_opy_(bstack1111_opy_ (u"ࠫࡌࡋࡔࠨᇭ"), bstack11ll1llll1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11lll111ll_opy_, bstack1111_opy_ (u"ࠬࡽࡢࠨᇮ")) as file:
          file.write(response.content)
        self.logger.info(bstack11ll1l111l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࡥ࡭ࡳࡧࡲࡺࡡࡽ࡭ࡵࡥࡰࡢࡶ࡫ࢁࠧᇯ"))
        return self.bstack11lll1l111_opy_(bstack11lll111ll_opy_, bstack11ll1l11l1_opy_)
      else:
        raise(bstack11ll1l111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࡷࡹࡧࡴࡶࡵࡢࡧࡴࡪࡥࡾࠤᇰ"))
    except:
      self.logger.error(bstack1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᇱ"))
  def bstack11lll11l11_opy_(self, bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_):
    try:
      bstack11ll1111l1_opy_ = self.bstack11ll1ll1ll_opy_(bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_)
      bstack11ll111lll_opy_ = self.bstack11lll1l11l_opy_(bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_, bstack11ll1111l1_opy_)
      return bstack11ll1111l1_opy_, bstack11ll111lll_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨᇲ").format(e))
    return bstack11ll1111l1_opy_, False
  def bstack11lll1l11l_opy_(self, bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_, bstack11ll1111l1_opy_, bstack11ll111l1l_opy_ = 0):
    if bstack11ll111l1l_opy_ > 1:
      return False
    if bstack11ll1111l1_opy_ == None or os.path.exists(bstack11ll1111l1_opy_) == False:
      self.logger.warn(bstack1111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᇳ"))
      bstack11ll1111l1_opy_ = self.bstack11ll1ll1ll_opy_(bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_)
      self.bstack11lll1l11l_opy_(bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_, bstack11ll1111l1_opy_, bstack11ll111l1l_opy_+1)
    bstack11ll1111ll_opy_ = bstack1111_opy_ (u"ࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࡜࠰ࡥ࡯࡭ࠥࡢࡤ࠯࡞ࡧ࠯࠳ࡢࡤࠬࠤᇴ")
    command = bstack1111_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫᇵ").format(bstack11ll1111l1_opy_)
    bstack11lll11ll1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11ll1111ll_opy_, bstack11lll11ll1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧᇶ"))
      bstack11ll1111l1_opy_ = self.bstack11ll1ll1ll_opy_(bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_)
      self.bstack11lll1l11l_opy_(bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_, bstack11ll1111l1_opy_, bstack11ll111l1l_opy_+1)
  def bstack11lll1l111_opy_(self, bstack11lll111ll_opy_, bstack11ll1l11l1_opy_):
    try:
      working_dir = os.path.dirname(bstack11lll111ll_opy_)
      shutil.unpack_archive(bstack11lll111ll_opy_, working_dir)
      bstack11ll1111l1_opy_ = os.path.join(working_dir, bstack11ll1l11l1_opy_)
      os.chmod(bstack11ll1111l1_opy_, 0o755)
      return bstack11ll1111l1_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᇷ"))
  def bstack11lll1ll1l_opy_(self):
    try:
      percy = str(self.config.get(bstack1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᇸ"), bstack1111_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣᇹ"))).lower()
      if percy != bstack1111_opy_ (u"ࠥࡸࡷࡻࡥࠣᇺ"):
        return False
      self.bstack11ll1l1l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᇻ").format(e))
  def init(self, bstack1l1ll11l1_opy_, config, logger):
    self.bstack1l1ll11l1_opy_ = bstack1l1ll11l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11lll1ll1l_opy_():
      return
    self.bstack11ll1l1ll1_opy_ = config.get(bstack1111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᇼ"), {})
    try:
      bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_ = self.bstack11lll1l1ll_opy_()
      bstack11ll1111l1_opy_, bstack11ll111lll_opy_ = self.bstack11lll11l11_opy_(bstack11ll1llll1_opy_, bstack11ll1l11l1_opy_)
      if bstack11ll111lll_opy_:
        self.binary_path = bstack11ll1111l1_opy_
        thread = Thread(target=self.bstack11ll11l111_opy_)
        thread.start()
      else:
        self.bstack11ll1lllll_opy_ = True
        self.logger.error(bstack1111_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᇽ").format(bstack11ll1111l1_opy_))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᇾ").format(e))
  def bstack11ll1l1l1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1111_opy_ (u"ࠨ࡮ࡲ࡫ࠬᇿ"), bstack1111_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬሀ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1111_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢሁ").format(logfile))
      self.bstack11ll1ll111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧሂ").format(e))
  def bstack11ll11l111_opy_(self):
    bstack11llll1l11_opy_ = self.bstack11lll11111_opy_()
    if bstack11llll1l11_opy_ == None:
      self.bstack11ll1lllll_opy_ = True
      self.logger.error(bstack1111_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣሃ"))
      return False
    command_args = [bstack1111_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢሄ") if self.bstack1l1ll11l1_opy_ else bstack1111_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫህ")]
    bstack11lll1ll11_opy_ = self.bstack11lll11l1l_opy_()
    if bstack11lll1ll11_opy_ != None:
      command_args.append(bstack1111_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢሆ").format(bstack11lll1ll11_opy_))
    env = os.environ.copy()
    env[bstack1111_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢሇ")] = bstack11llll1l11_opy_
    bstack11ll111ll1_opy_ = [self.binary_path]
    self.bstack11ll1l1l1l_opy_()
    self.bstack11ll1l11ll_opy_ = self.bstack11ll11l11l_opy_(bstack11ll111ll1_opy_ + command_args, env)
    self.logger.debug(bstack1111_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦለ"))
    bstack11ll111l1l_opy_ = 0
    while self.bstack11ll1l11ll_opy_.poll() == None:
      bstack11lll1111l_opy_ = self.bstack11llll1111_opy_()
      if bstack11lll1111l_opy_:
        self.logger.debug(bstack1111_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢሉ"))
        self.bstack11ll111l11_opy_ = True
        return True
      bstack11ll111l1l_opy_ += 1
      self.logger.debug(bstack1111_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣሊ").format(bstack11ll111l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦላ").format(bstack11ll111l1l_opy_))
    self.bstack11ll1lllll_opy_ = True
    return False
  def bstack11llll1111_opy_(self, bstack11ll111l1l_opy_ = 0):
    try:
      if bstack11ll111l1l_opy_ > 10:
        return False
      bstack11llll111l_opy_ = os.environ.get(bstack1111_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧሌ"), bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩል"))
      bstack11ll1ll1l1_opy_ = bstack11llll111l_opy_ + bstack1l11llll11_opy_
      response = requests.get(bstack11ll1ll1l1_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11lll11111_opy_(self):
    bstack11ll11l1l1_opy_ = bstack1111_opy_ (u"ࠩࡤࡴࡵ࠭ሎ") if self.bstack1l1ll11l1_opy_ else bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬሏ")
    bstack1l111l1l1l_opy_ = bstack1111_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠥሐ").format(self.config[bstack1111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪሑ")], bstack11ll11l1l1_opy_)
    uri = bstack1ll11l11_opy_(bstack1l111l1l1l_opy_)
    try:
      response = bstack1ll1111l_opy_(bstack1111_opy_ (u"࠭ࡇࡆࡖࠪሒ"), uri, {}, {bstack1111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬሓ"): (self.config[bstack1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪሔ")], self.config[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬሕ")])})
      if response.status_code == 200:
        bstack11lll111l1_opy_ = response.json()
        if bstack1111_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤሖ") in bstack11lll111l1_opy_:
          return bstack11lll111l1_opy_[bstack1111_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥሗ")]
        else:
          raise bstack1111_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬመ").format(bstack11lll111l1_opy_)
      else:
        raise bstack1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨሙ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣሚ").format(e))
  def bstack11lll11l1l_opy_(self):
    bstack11llll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦማ"))
    try:
      if bstack1111_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪሜ") not in self.bstack11ll1l1ll1_opy_:
        self.bstack11ll1l1ll1_opy_[bstack1111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫም")] = 2
      with open(bstack11llll11ll_opy_, bstack1111_opy_ (u"ࠫࡼ࠭ሞ")) as fp:
        json.dump(self.bstack11ll1l1ll1_opy_, fp)
      return bstack11llll11ll_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧሟ").format(e))
  def bstack11ll11l11l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11ll11111l_opy_ == bstack1111_opy_ (u"࠭ࡷࡪࡰࠪሠ"):
        bstack11ll1l1111_opy_ = [bstack1111_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨሡ"), bstack1111_opy_ (u"ࠨ࠱ࡦࠫሢ")]
        cmd = bstack11ll1l1111_opy_ + cmd
      cmd = bstack1111_opy_ (u"ࠩࠣࠫሣ").join(cmd)
      self.logger.debug(bstack1111_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢሤ").format(cmd))
      with open(self.bstack11ll1ll111_opy_, bstack1111_opy_ (u"ࠦࡦࠨሥ")) as bstack11ll1lll11_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11ll1lll11_opy_, text=True, stderr=bstack11ll1lll11_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11ll1lllll_opy_ = True
      self.logger.error(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢሦ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11ll111l11_opy_:
        self.logger.info(bstack1111_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢሧ"))
        cmd = [self.binary_path, bstack1111_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥረ")]
        self.bstack11ll11l11l_opy_(cmd)
        self.bstack11ll111l11_opy_ = False
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣሩ").format(cmd, e))
  def bstack1ll1ll111l_opy_(self):
    if not self.bstack11ll1l1l11_opy_:
      return
    try:
      bstack11ll1lll1l_opy_ = 0
      while not self.bstack11ll111l11_opy_ and bstack11ll1lll1l_opy_ < self.bstack11ll11lll1_opy_:
        if self.bstack11ll1lllll_opy_:
          self.logger.info(bstack1111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢሪ"))
          return
        time.sleep(1)
        bstack11ll1lll1l_opy_ += 1
      os.environ[bstack1111_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩራ")] = str(self.bstack11ll1l1lll_opy_())
      self.logger.info(bstack1111_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧሬ"))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨር").format(e))
  def bstack11ll1l1lll_opy_(self):
    if self.bstack1l1ll11l1_opy_:
      return
    try:
      bstack11lll11lll_opy_ = [platform[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫሮ")].lower() for platform in self.config.get(bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪሯ"), [])]
      bstack11ll11ll11_opy_ = sys.maxsize
      bstack11ll1ll11l_opy_ = bstack1111_opy_ (u"ࠨࠩሰ")
      for browser in bstack11lll11lll_opy_:
        if browser in self.bstack11ll11llll_opy_:
          bstack11ll11l1ll_opy_ = self.bstack11ll11llll_opy_[browser]
        if bstack11ll11l1ll_opy_ < bstack11ll11ll11_opy_:
          bstack11ll11ll11_opy_ = bstack11ll11l1ll_opy_
          bstack11ll1ll11l_opy_ = browser
      return bstack11ll1ll11l_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥሱ").format(e))