from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
import time
import ntptime
import urequests
import json

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)


auth = None
database = None
redis = None
storage = None
labelTab = None
firstLabelY = None
ledRadius = None
leftMargin = None
firstLedY = None
labelY_Offset = None
ledY_Offset = None

wifiCfg.autoConnect(lcdShow=True)
timeLabel = M5Label('', x=126, y=219, color=0x000, font=FONT_MONT_14, parent=None)
#dbgLabel = M5Label('', x=0, y=200, color=0x000, font=FONT_MONT_14, parent=None)
label2 = M5Label('', x=160, y=76, color=0x000, font=FONT_MONT_18, parent=None)
label3 = M5Label('', x=160, y=111, color=0x000, font=FONT_MONT_18, parent=None)
label4 = M5Label('', x=160, y=146, color=0x000, font=FONT_MONT_18, parent=None)
label5 = M5Label('', x=167, y=177, color=0x000, font=FONT_MONT_18, parent=None)
image0 = M5Img("res/quaylogo.png", x=0, y=0, parent=None)


def getQuayStatus():
  req = urequests.request( method='GET', url='https://quay.io/status')
  stats = json.loads(req.text)
  svcs = stats['data']['services']
  #dbgLabel.set_text(str(svcs))
  setIndicators(svcs['auth'], svcs['database'], svcs['redis'], svcs['storage'])

def setIndicators(auth, database, redis, storage):
  global labelTab, firstLabelY, ledRadius, leftMargin, firstLedY, labelY_Offset, ledY_Offset
  label2.set_pos(labelTab, firstLabelY)
  label2.set_text('Authentication')
  if auth == True:
    lcd.circle(leftMargin, firstLedY, ledRadius, fillcolor=0x009900)
  else:
    lcd.circle(leftMargin, firstLedY, ledRadius, fillcolor=0xcc0000)
  label3.set_pos(labelTab, (firstLabelY + labelY_Offset))
  label3.set_text('Database')
  if database == True:
    lcd.circle(leftMargin, (firstLedY + ledY_Offset), ledRadius, fillcolor=0x009900)
  else:
    lcd.circle(leftMargin, (firstLedY + ledY_Offset), ledRadius, fillcolor=0xcc0000)
  label4.set_pos(labelTab, (firstLabelY + labelY_Offset * 2))
  label4.set_text('Redis')
  if redis == True:
    lcd.circle(leftMargin, (firstLedY + ledY_Offset * 2), ledRadius, fillcolor=0x009900)
  else:
    lcd.circle(leftMargin, (firstLedY + ledY_Offset * 2), ledRadius, fillcolor=0xcc0000)
  label5.set_pos(labelTab, (firstLabelY + labelY_Offset * 3))
  label5.set_text('Storage')
  if storage == True:
    lcd.circle(leftMargin, (firstLedY + ledY_Offset * 3), ledRadius, fillcolor=0x009900)
  else:
    lcd.circle(leftMargin, (firstLedY + ledY_Offset * 3), ledRadius, fillcolor=0xcc0000)



screen.set_screen_bg_color(0xffffff)
image0.set_align(ALIGN_IN_TOP_MID, x=0, y=0, ref=screen.obj)
image0.set_img_src("res/quaylogo.png")
ledRadius = 12
leftMargin = 70
labelTab = 130
firstLabelY = 74
labelY_Offset = 32
firstLedY = 85
ledY_Offset = 32
while not (wifiCfg.wlan_sta.isconnected()):
  wait(1)
ntp = ntptime.client(host='us.pool.ntp.org', timezone=8)
while True:
  timeLabel.set_text(str(ntp.formatDatetime('-', ':')))
  getQuayStatus()
  wait(10)