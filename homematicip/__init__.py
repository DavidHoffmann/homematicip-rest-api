# coding=utf-8
import platform
import locale
import logging
import hashlib

from .home import *
from .device import *
from .auth import *
from .group import *
from .securityEvent import *

import requests

clientCharacteristics = {"clientCharacteristics":
    {
        "apiVersion": "10",
        "applicationIdentifier": "homematicip-python",
        "applicationVersion": "1.0",
        "deviceManufacturer": "none",
        "deviceType": "Computer",
        "language": locale.getdefaultlocale()[0],
        "osType": platform.system(),
        "osVersion": platform.release(),
    },
    "id": None
}

auth_token = ""
clientauth_token =""
urlREST = ""
urlWebSocket = ""


def set_auth_token(token):
    global auth_token
    auth_token = token


def get_auth_token():
    global auth_token
    return auth_token

def get_clientauth_token():
    global clientauth_token
    return clientauth_token


def get_clientCharacteristics():
    return clientCharacteristics


def init(accesspoint_id, lookup=True):
    global urlREST
    global clientCharacteristics
    global urlWebSocket
    global clientauth_token
    accesspoint_id = accesspoint_id.replace('-', '').upper()
    clientCharacteristics["id"] = accesspoint_id

    clientauth_token=hashlib.sha512(str(accesspoint_id+"jiLpVitHvWnIGD1yo7MA").encode('utf-8')).hexdigest().upper()

    if lookup:
        while True:
            try:
                result = requests.post("https://lookup.homematic.com:48335/getHost", json=clientCharacteristics,timeout=3)
                js = json.loads(result.text)
                urlREST = js["urlREST"]
                urlWebSocket = js["urlWebSocket"]
                break
            except:
                pass
    else:
        urlREST = "https://ps1.homematic.com:6969"
        urlWebSocket = "wss://ps1.homematic.com:8888"


def get_urlREST():
    return urlREST


def get_urlWebSocket():
    return urlWebSocket

#adding a new "trace" log level
TRACE_LEVEL_NUM = 5 
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
def trace(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws) 
logging.Logger.trace = trace