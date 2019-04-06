
import json
import requests
class Device(object):

    def __init__(self, account, device_info):
        self._account = account
        self.device_iden = device_info.get("iden")
        if not device_info.get("icon", None):
            device_info["icon"] = "system"
        for attr in ("push_token", "app_version", "fingerprint", "created", "modified",
                    "active", "nickname", "generated_nickname", "manufacturer", "icon",
                    "model", "has_sms", "key_fingerprint"):
            setattr(self, attr, device_info.get(attr))

    def _push(self, data):
        data["device_iden"] = self.device_iden
        return self._account._push(data)

class PushbulletError(Exception):
    pass

class InvalidKeyError(PushbulletError):
    pass

class PushError(PushbulletError):
    pass

class Pushbullet(object):

    DEVICES_URL = "https://api.pushbullet.com/v2/devices"
    ME_URL = "https://api.pushbullet.com/v2/users/me"
    PUSH_URL = "https://api.pushbullet.com/v2/pushes"
    EPHEMERALS_URL = "https://api.pushbullet.com/v2/ephemerals"

    def __init__(self, api_key):
        self.api_key = api_key
        self._session = requests.Session()
        self._session.auth = (self.api_key, "")
        self.refresh()
        self._encryption_key = None

    def _get_data(self, url):
        resp = self._session.get(url)
        if resp.status_code in (401, 403):
            print 'error: 01'
            raise InvalidKeyError()
        elif resp.status_code == 429:
            print 'error: 02'
            raise PushbulletError("Too Many Requests")
        elif resp.status_code != requests.codes.ok:
            print 'error: 03'
            raise PushbulletError(resp.status_code)
        return resp.json()

    def _load_user_info(self):
        self.user_info = self._get_data(self.ME_URL)

    def _load_devices(self):
        self.devices = []
        resp_dict = self._get_data(self.DEVICES_URL)
        device_list = resp_dict.get("devices", [])

        for device_info in device_list:
            if device_info.get("active"):
                d = Device(self, device_info)
                self.devices.append(d)

    def get_device(self, nickname):
        req_device = next((device for device in self.devices if device.nickname == nickname), None)
        if req_device is None:
            print 'error: 04'
            raise PushbulletError('No device found with nickname "{}"'.format(nickname))

        return req_device

    def _push(self, data):
        r = self._session.post(self.PUSH_URL, data=json.dumps(data))
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print 'error: 05'
            # raise PushError(r.text)

    def push_sms(self, device, number, message):
        data = {
            "type": "push",
            "push": {
                "type": "messaging_extension_reply",
                "package_name": "com.pushbullet.android",
                "source_user_iden": self.user_info['iden'],
                "target_device_iden": device.device_iden,
                "conversation_iden": number,
                "message": message
            }
        }

        r = self._session.post(self.EPHEMERALS_URL, data=json.dumps(data))
        if r.status_code == requests.codes.ok:
            return r.json()
        raise PushError(r.text)

    def refresh(self):
        self._load_devices()
        self._load_user_info()