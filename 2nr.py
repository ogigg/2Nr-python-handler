from uiautomator import device as d
import re
import time
from re import sub
from adb.client import Client as AdbClient


def deleteNr():
  d(resourceId="pl.rs.sip.softphone:id/btnEditOptions").click()
  d(text="Usuń").click()
  d(text="OK").click()

def createNr():
  d(text="Wybierz ten numer").click()
  d(text="Zapisz ten numer").click()

def getPhoneNrAsString():
  phoneNrString=d(resourceId="pl.rs.sip.softphone:id/tvMyNumber").info['text']
  phoneNrumbers=re.findall('\d+', str(phoneNrString))
  phoneNr=str(phoneNrumbers[0])+str(phoneNrumbers[1])+str(phoneNrumbers[2])
  return phoneNr

def getMessage():
  d(text="Wiadomości").click()
  d(text="taobao")[0].click()
  msg=(d(resourceId="pl.rs.sip.softphone:id/txtMessage").info['text'])
  code=re.findall('\d+', str(msg))
  return str(code[0])

def restartApk():
    d.press.home()
    device.shell("pm clear pl.rs.sip.softphone")
    device.shell("monkey -p pl.rs.sip.softphone -c android.intent.category.LAUNCHER 1")
    if d(text='Wykryto nakładkę ekranową').exists:
        print('Wykryto nakładkę ekranową')
        d.press.home()
        device.shell("pm clear pl.rs.sip.softphone")
        device.shell("monkey -p pl.rs.sip.softphone -c android.intent.category.LAUNCHER 1")
    d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
    time.sleep(1)  
    d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
    time.sleep(1)  
    d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
    time.sleep(1)  
    d(text="Autostart").wait.exists(timeout=10)
    d.press.back()
    d(text="OK").click()
    d(text="Pomiń prezentację").click()
    d(text="Akceptuję").click()
    time.sleep(1)
    d.press.back()
    print("Aplikacja uruchomiona")


client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device=devices[0]

#print(d.dump())

restartApk()
nrDone=False
while nrDone==False:
    nrOK=False
    while nrOK==False:
        if (d(text="Problem").exists) or (d(text="Losuj").exists):
            print("Problem/Losuj")
            d(resourceId="pl.rs.sip.softphone:id/btnGetNumber").click()
            print("Kliknalem refresh")
            time.sleep(2)
            nrOK=False
        else:
            print("Jest Nr")
            nrOK=True
    createNr()
    time.sleep(2)
    if(d(resourceId="android:id/button1").exists):
        print("Wystapil problem")
        print("Restartuje apke")
        restartApk()
        nrDone=False
    else:
        print("Wsystko sie udao")
        nrDone=True

tel=getPhoneNrAsString()
print(tel)
#
# getMessage()
