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
from bstack_utils.helper import bstack1l1l1l11l_opy_, bstack1111ll11l_opy_
class bstack1llll1ll11_opy_:
  working_dir = os.getcwd()
  bstack1ll11111ll_opy_ = False
  config = {}
  binary_path = bstack1l1ll1l_opy_ (u"ࠫࠬሳ")
  bstack11l1l1l1l1_opy_ = bstack1l1ll1l_opy_ (u"ࠬ࠭ሴ")
  bstack11l1lll1l1_opy_ = False
  bstack11ll11l11l_opy_ = None
  bstack11l1l11lll_opy_ = {}
  bstack11l1lll111_opy_ = 300
  bstack11l1ll1111_opy_ = False
  logger = None
  bstack11l1l111l1_opy_ = False
  bstack11ll11llll_opy_ = bstack1l1ll1l_opy_ (u"࠭ࠧስ")
  bstack11l1lll1ll_opy_ = {
    bstack1l1ll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧሶ") : 1,
    bstack1l1ll1l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩሷ") : 2,
    bstack1l1ll1l_opy_ (u"ࠩࡨࡨ࡬࡫ࠧሸ") : 3,
    bstack1l1ll1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪሹ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11ll11l1l1_opy_(self):
    bstack11ll1l111l_opy_ = bstack1l1ll1l_opy_ (u"ࠫࠬሺ")
    bstack11ll11lll1_opy_ = sys.platform
    bstack11l1ll111l_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫሻ")
    if re.match(bstack1l1ll1l_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨሼ"), bstack11ll11lll1_opy_) != None:
      bstack11ll1l111l_opy_ = bstack1l111ll111_opy_ + bstack1l1ll1l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣሽ")
      self.bstack11ll11llll_opy_ = bstack1l1ll1l_opy_ (u"ࠨ࡯ࡤࡧࠬሾ")
    elif re.match(bstack1l1ll1l_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢሿ"), bstack11ll11lll1_opy_) != None:
      bstack11ll1l111l_opy_ = bstack1l111ll111_opy_ + bstack1l1ll1l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦቀ")
      bstack11l1ll111l_opy_ = bstack1l1ll1l_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢቁ")
      self.bstack11ll11llll_opy_ = bstack1l1ll1l_opy_ (u"ࠬࡽࡩ࡯ࠩቂ")
    else:
      bstack11ll1l111l_opy_ = bstack1l111ll111_opy_ + bstack1l1ll1l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤቃ")
      self.bstack11ll11llll_opy_ = bstack1l1ll1l_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ቄ")
    return bstack11ll1l111l_opy_, bstack11l1ll111l_opy_
  def bstack11ll11111l_opy_(self):
    try:
      bstack11l1l1lll1_opy_ = [os.path.join(expanduser(bstack1l1ll1l_opy_ (u"ࠣࢀࠥቅ")), bstack1l1ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩቆ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l1l1lll1_opy_:
        if(self.bstack11l1llll11_opy_(path)):
          return path
      raise bstack1l1ll1l_opy_ (u"࡙ࠥࡳࡧ࡬ࡣࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢቇ")
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨቈ").format(e))
  def bstack11l1llll11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11l1ll11l1_opy_(self, bstack11ll1l111l_opy_, bstack11l1ll111l_opy_):
    try:
      bstack11l1llllll_opy_ = self.bstack11ll11111l_opy_()
      bstack11ll111l1l_opy_ = os.path.join(bstack11l1llllll_opy_, bstack1l1ll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨ቉"))
      bstack11ll1111l1_opy_ = os.path.join(bstack11l1llllll_opy_, bstack11l1ll111l_opy_)
      if os.path.exists(bstack11ll1111l1_opy_):
        self.logger.info(bstack1l1ll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣቊ").format(bstack11ll1111l1_opy_))
        return bstack11ll1111l1_opy_
      if os.path.exists(bstack11ll111l1l_opy_):
        self.logger.info(bstack1l1ll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧቋ").format(bstack11ll111l1l_opy_))
        return self.bstack11l1ll1l1l_opy_(bstack11ll111l1l_opy_, bstack11l1ll111l_opy_)
      self.logger.info(bstack1l1ll1l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨቌ").format(bstack11ll1l111l_opy_))
      response = bstack1111ll11l_opy_(bstack1l1ll1l_opy_ (u"ࠩࡊࡉ࡙࠭ቍ"), bstack11ll1l111l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11ll111l1l_opy_, bstack1l1ll1l_opy_ (u"ࠪࡻࡧ࠭቎")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1ll1ll1_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡣ࡫ࡱࡥࡷࡿ࡟ࡻ࡫ࡳࡣࡵࡧࡴࡩࡿࠥ቏"))
        return self.bstack11l1ll1l1l_opy_(bstack11ll111l1l_opy_, bstack11l1ll111l_opy_)
      else:
        raise(bstack11l1ll1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࡵࡷࡥࡹࡻࡳࡠࡥࡲࡨࡪࢃࠢቐ"))
    except:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥቑ"))
  def bstack11ll1l1111_opy_(self, bstack11ll1l111l_opy_, bstack11l1ll111l_opy_):
    try:
      bstack11ll1111l1_opy_ = self.bstack11l1ll11l1_opy_(bstack11ll1l111l_opy_, bstack11l1ll111l_opy_)
      bstack11l1l1llll_opy_ = self.bstack11l1l11l1l_opy_(bstack11ll1l111l_opy_, bstack11l1ll111l_opy_, bstack11ll1111l1_opy_)
      return bstack11ll1111l1_opy_, bstack11l1l1llll_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦቒ").format(e))
    return bstack11ll1111l1_opy_, False
  def bstack11l1l11l1l_opy_(self, bstack11ll1l111l_opy_, bstack11l1ll111l_opy_, bstack11ll1111l1_opy_, bstack11l1l1ll1l_opy_ = 0):
    if bstack11l1l1ll1l_opy_ > 1:
      return False
    if bstack11ll1111l1_opy_ == None or os.path.exists(bstack11ll1111l1_opy_) == False:
      self.logger.warn(bstack1l1ll1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨቓ"))
      bstack11ll1111l1_opy_ = self.bstack11l1ll11l1_opy_(bstack11ll1l111l_opy_, bstack11l1ll111l_opy_)
      self.bstack11l1l11l1l_opy_(bstack11ll1l111l_opy_, bstack11l1ll111l_opy_, bstack11ll1111l1_opy_, bstack11l1l1ll1l_opy_+1)
    bstack11ll11ll11_opy_ = bstack1l1ll1l_opy_ (u"ࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽࡡ࠵ࡣ࡭࡫ࠣࡠࡩ࠴࡜ࡥ࠭࠱ࡠࡩ࠱ࠢቔ")
    command = bstack1l1ll1l_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩቕ").format(bstack11ll1111l1_opy_)
    bstack11l1l1111l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11ll11ll11_opy_, bstack11l1l1111l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥቖ"))
      bstack11ll1111l1_opy_ = self.bstack11l1ll11l1_opy_(bstack11ll1l111l_opy_, bstack11l1ll111l_opy_)
      self.bstack11l1l11l1l_opy_(bstack11ll1l111l_opy_, bstack11l1ll111l_opy_, bstack11ll1111l1_opy_, bstack11l1l1ll1l_opy_+1)
  def bstack11l1ll1l1l_opy_(self, bstack11ll111l1l_opy_, bstack11l1ll111l_opy_):
    try:
      working_dir = os.path.dirname(bstack11ll111l1l_opy_)
      shutil.unpack_archive(bstack11ll111l1l_opy_, working_dir)
      bstack11ll1111l1_opy_ = os.path.join(working_dir, bstack11l1ll111l_opy_)
      os.chmod(bstack11ll1111l1_opy_, 0o755)
      return bstack11ll1111l1_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨ቗"))
  def bstack11l1l11l11_opy_(self):
    try:
      percy = str(self.config.get(bstack1l1ll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬቘ"), bstack1l1ll1l_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ቙"))).lower()
      if percy != bstack1l1ll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨቚ"):
        return False
      self.bstack11l1lll1l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦቛ").format(e))
  def init(self, bstack1ll11111ll_opy_, config, logger):
    self.bstack1ll11111ll_opy_ = bstack1ll11111ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1l11l11_opy_():
      return
    self.bstack11l1l11lll_opy_ = config.get(bstack1l1ll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩቜ"), {})
    try:
      bstack11ll1l111l_opy_, bstack11l1ll111l_opy_ = self.bstack11ll11l1l1_opy_()
      bstack11ll1111l1_opy_, bstack11l1l1llll_opy_ = self.bstack11ll1l1111_opy_(bstack11ll1l111l_opy_, bstack11l1ll111l_opy_)
      if bstack11l1l1llll_opy_:
        self.binary_path = bstack11ll1111l1_opy_
        thread = Thread(target=self.bstack11ll1l11l1_opy_)
        thread.start()
      else:
        self.bstack11l1l111l1_opy_ = True
        self.logger.error(bstack1l1ll1l_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣቝ").format(bstack11ll1111l1_opy_))
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ቞").format(e))
  def bstack11ll111111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1ll1l_opy_ (u"࠭࡬ࡰࡩࠪ቟"), bstack1l1ll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪበ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1ll1l_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧቡ").format(logfile))
      self.bstack11l1l1l1l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥቢ").format(e))
  def bstack11ll1l11l1_opy_(self):
    bstack11l1l1l111_opy_ = self.bstack11ll1l11ll_opy_()
    if bstack11l1l1l111_opy_ == None:
      self.bstack11l1l111l1_opy_ = True
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨባ"))
      return False
    command_args = [bstack1l1ll1l_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧቤ") if self.bstack1ll11111ll_opy_ else bstack1l1ll1l_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩብ")]
    bstack11l1ll1lll_opy_ = self.bstack11l1l1l1ll_opy_()
    if bstack11l1ll1lll_opy_ != None:
      command_args.append(bstack1l1ll1l_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧቦ").format(bstack11l1ll1lll_opy_))
    env = os.environ.copy()
    env[bstack1l1ll1l_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧቧ")] = bstack11l1l1l111_opy_
    bstack11ll111l11_opy_ = [self.binary_path]
    self.bstack11ll111111_opy_()
    self.bstack11ll11l11l_opy_ = self.bstack11l1l111ll_opy_(bstack11ll111l11_opy_ + command_args, env)
    self.logger.debug(bstack1l1ll1l_opy_ (u"ࠣࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠤቨ"))
    bstack11l1l1ll1l_opy_ = 0
    while self.bstack11ll11l11l_opy_.poll() == None:
      bstack11ll1111ll_opy_ = self.bstack11ll11ll1l_opy_()
      if bstack11ll1111ll_opy_:
        self.logger.debug(bstack1l1ll1l_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠧቩ"))
        self.bstack11l1ll1111_opy_ = True
        return True
      bstack11l1l1ll1l_opy_ += 1
      self.logger.debug(bstack1l1ll1l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡕࡩࡹࡸࡹࠡ࠯ࠣࡿࢂࠨቪ").format(bstack11l1l1ll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1ll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡌࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࢀࢃࠠࡢࡶࡷࡩࡲࡶࡴࡴࠤቫ").format(bstack11l1l1ll1l_opy_))
    self.bstack11l1l111l1_opy_ = True
    return False
  def bstack11ll11ll1l_opy_(self, bstack11l1l1ll1l_opy_ = 0):
    try:
      if bstack11l1l1ll1l_opy_ > 10:
        return False
      bstack11ll11l1ll_opy_ = os.environ.get(bstack1l1ll1l_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡘࡋࡒࡗࡇࡕࡣࡆࡊࡄࡓࡇࡖࡗࠬቬ"), bstack1l1ll1l_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠸࠷࠸࠾ࠧቭ"))
      bstack11l1llll1l_opy_ = bstack11ll11l1ll_opy_ + bstack1l111l11ll_opy_
      response = requests.get(bstack11l1llll1l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11ll1l11ll_opy_(self):
    bstack11l1lllll1_opy_ = bstack1l1ll1l_opy_ (u"ࠧࡢࡲࡳࠫቮ") if self.bstack1ll11111ll_opy_ else bstack1l1ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪቯ")
    bstack1l11llll11_opy_ = bstack1l1ll1l_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠣተ").format(self.config[bstack1l1ll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨቱ")], bstack11l1lllll1_opy_)
    uri = bstack1l1l1l11l_opy_(bstack1l11llll11_opy_)
    try:
      response = bstack1111ll11l_opy_(bstack1l1ll1l_opy_ (u"ࠫࡌࡋࡔࠨቲ"), uri, {}, {bstack1l1ll1l_opy_ (u"ࠬࡧࡵࡵࡪࠪታ"): (self.config[bstack1l1ll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨቴ")], self.config[bstack1l1ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪት")])})
      if response.status_code == 200:
        bstack11ll1l1l11_opy_ = response.json()
        if bstack1l1ll1l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢቶ") in bstack11ll1l1l11_opy_:
          return bstack11ll1l1l11_opy_[bstack1l1ll1l_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣቷ")]
        else:
          raise bstack1l1ll1l_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪቸ").format(bstack11ll1l1l11_opy_)
      else:
        raise bstack1l1ll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦቹ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨቺ").format(e))
  def bstack11l1l1l1ll_opy_(self):
    bstack11ll11l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1l_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤቻ"))
    try:
      if bstack1l1ll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨቼ") not in self.bstack11l1l11lll_opy_:
        self.bstack11l1l11lll_opy_[bstack1l1ll1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩች")] = 2
      with open(bstack11ll11l111_opy_, bstack1l1ll1l_opy_ (u"ࠩࡺࠫቾ")) as fp:
        json.dump(self.bstack11l1l11lll_opy_, fp)
      return bstack11ll11l111_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥቿ").format(e))
  def bstack11l1l111ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11ll11llll_opy_ == bstack1l1ll1l_opy_ (u"ࠫࡼ࡯࡮ࠨኀ"):
        bstack11l1l1l11l_opy_ = [bstack1l1ll1l_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭ኁ"), bstack1l1ll1l_opy_ (u"࠭࠯ࡤࠩኂ")]
        cmd = bstack11l1l1l11l_opy_ + cmd
      cmd = bstack1l1ll1l_opy_ (u"ࠧࠡࠩኃ").join(cmd)
      self.logger.debug(bstack1l1ll1l_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧኄ").format(cmd))
      with open(self.bstack11l1l1l1l1_opy_, bstack1l1ll1l_opy_ (u"ࠤࡤࠦኅ")) as bstack11l1l1ll11_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l1l1ll11_opy_, text=True, stderr=bstack11l1l1ll11_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l1l111l1_opy_ = True
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧኆ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l1ll1111_opy_:
        self.logger.info(bstack1l1ll1l_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧኇ"))
        cmd = [self.binary_path, bstack1l1ll1l_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣኈ")]
        self.bstack11l1l111ll_opy_(cmd)
        self.bstack11l1ll1111_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ኉").format(cmd, e))
  def bstack1llll11l11_opy_(self):
    if not self.bstack11l1lll1l1_opy_:
      return
    try:
      bstack11ll111lll_opy_ = 0
      while not self.bstack11l1ll1111_opy_ and bstack11ll111lll_opy_ < self.bstack11l1lll111_opy_:
        if self.bstack11l1l111l1_opy_:
          self.logger.info(bstack1l1ll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧኊ"))
          return
        time.sleep(1)
        bstack11ll111lll_opy_ += 1
      os.environ[bstack1l1ll1l_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧኋ")] = str(self.bstack11l1lll11l_opy_())
      self.logger.info(bstack1l1ll1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥኌ"))
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦኍ").format(e))
  def bstack11l1lll11l_opy_(self):
    if self.bstack1ll11111ll_opy_:
      return
    try:
      bstack11l1ll11ll_opy_ = [platform[bstack1l1ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ኎")].lower() for platform in self.config.get(bstack1l1ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ኏"), [])]
      bstack11l1l11ll1_opy_ = sys.maxsize
      bstack11l1ll1l11_opy_ = bstack1l1ll1l_opy_ (u"࠭ࠧነ")
      for browser in bstack11l1ll11ll_opy_:
        if browser in self.bstack11l1lll1ll_opy_:
          bstack11ll111ll1_opy_ = self.bstack11l1lll1ll_opy_[browser]
        if bstack11ll111ll1_opy_ < bstack11l1l11ll1_opy_:
          bstack11l1l11ll1_opy_ = bstack11ll111ll1_opy_
          bstack11l1ll1l11_opy_ = browser
      return bstack11l1ll1l11_opy_
    except Exception as e:
      self.logger.error(bstack1l1ll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣኑ").format(e))