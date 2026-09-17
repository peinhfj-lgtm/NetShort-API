import secrets
import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import time
import json
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def rsa_public_encrypt_pkcs1(rsa_public_key_pem, data_bytes):
    key = RSA.import_key(rsa_public_key_pem)

    cipher = PKCS1_v1_5.new(key)

    encrypted = cipher.encrypt(data_bytes)

    return encrypted

def rsa_no_padding_decrypt(private_key_pem, encrypted_data):
    key = RSA.import_key(private_key_pem)

    cipher = PKCS1_v1_5.new(key)

    decrypted = cipher.decrypt(encrypted_data, None)

    return decrypted



class NetShortDownloadAPI:
    APP_VER = "2.0.3"
    BASE_URL = "https://appsecapi.netshort.com"
    RSA_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
***
-----END PUBLIC KEY-----'''
    RSA_PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
***
-----END PRIVATE KEY-----'''
    def __init__(self):
        self.user_agent = None
        self.user_id = None
        self.deviceCode = ''.join(random.choices('0123456789abcdef', k=8))
        self.build_agent()
        self.token = None

    def encryptRequestPayload(self, payload):
        aesKeyStr = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
        key = aesKeyStr.encode('utf-8')
        plaintext = payload.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        padded_data = pad(plaintext, AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        bodyB64 = base64.b64encode(encrypted).decode('utf-8')
        aesKeyB64 = base64.b64encode(key).decode('utf-8')
        encryptedKeyBuf = rsa_public_encrypt_pkcs1(self.RSA_PUBLIC_KEY, aesKeyB64.encode('utf-8'))
        headerKeyB64 = base64.b64encode(encryptedKeyBuf).decode('utf-8')
        return bodyB64, headerKeyB64

    def sec_request(self, endpoint, payload):
        url = self.BASE_URL + endpoint
        payload = json.dumps(payload, separators=(',', ':'))
        ts = str(int(time.time() * 1000))

        bodyB64, headerKeyB64 = self.encryptRequestPayload(payload)
        headers = {
            "Host": "appsecapi.netshort.com",
            "Canary": "v2",
            "Os": "1",
            "Version": self.APP_VER,
            "Encrypt-Key": headerKeyB64,
            "Device-Code": self.deviceCode,
            "Content-Type": "application/json",
            "Content-Language": "en_US",
            "User-Agent": self.user_agent,
            "Timestamp": ts,
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        if 'auth/login' in endpoint:
            headers["Start_type"] = "cold"
            headers["Network"] = "wifi,cold,true"
            headers["Push_switch"] = "true"

        req = requests.post(url, data=bodyB64, headers=headers)
        encrypt_key = req.headers["encrypt-key"]
        encrypted_body = req.text
        decrypted_data = self.decrypt_response_payload(encrypt_key, encrypted_body)
        last_brace = decrypted_data.rfind('}')
        if last_brace != -1:
            decrypted_data = decrypted_data[:last_brace + 1]
        return decrypted_data

    def decrypt_response_payload(self, encrypt_key, encrypted_body):
        aes_key = rsa_no_padding_decrypt(self.RSA_PRIVATE_KEY, base64.b64decode(encrypt_key))
        cipher = AES.new(base64.b64decode(aes_key.decode('utf-8')), AES.MODE_ECB)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_body.encode('utf-8'))).decode('utf-8')
        return decrypted

    def login(self):
        self.deviceCode = ''.join(random.choices('0123456789abcdef', k=8))
        payload = {
            'os': "Android",
            'appVer': self.APP_VER,
            'identity': 0,
            'model': "sdk_gphone64_x86_64",
            'deviceCode': self.deviceCode,
            'source': "visitor",
            'osVer': "12",
        }
        r_response = self.sec_request('/prod-app-api/auth/login', payload)
        json_data = json.loads(r_response)
        self.token = json_data['data']['token']
        self.user_id = json_data['data']['loginUser']['userId']

    def unlock_ad(self, book_id, episodeNo, episodeId, configId='1993944126552477698', adUnlockEpsType=1):
        payload = {
            'shortPlayEpisodeNo': episodeNo,
            'shortPlayId': book_id,
            'adUnlockEpsType': adUnlockEpsType,
            'adUnlockConfigId': configId,
            'shortPlayEpisodeId': episodeId
        }

        r_response = self.sec_request('/prod-app-api/user/shortPlay/userBase/unlock_ad_episode', payload)
        json_data = json.loads(r_response)
        if not json_data['data']:
            pass
        return json_data['data']

    def get_single_episode(self, book_id, episodeId, episodeNo):
        print(f'unlocking')
        payload = {
                    'codec': "h264",
                    'episodeId': episodeId,
                    'playClarity': "1080p",
                    'episodeType': 1,
                    'episodeNo': episodeNo,
                    'shortPlayId': str(book_id)
                }
        try:
            r_response = self.sec_request('/prod-app-api/video/shortPlay/base/episode/detail_info', payload)
            json_data = json.loads(r_response)
            return json_data
        except Exception as e:
            if type(e).__name__ == 'SSLError':
                input("⚠ Network ERROR")
                exit(1)


    def build_agent(self):
        ANDROID_MODELS = [
            "Pixel 6", "Pixel 7", "Pixel 8", "Pixel 6a",
            "Galaxy S21", "Galaxy S22", "Galaxy S23",
            "Redmi Note 11", "Redmi Note 12", "ONEPLUS A6003", "CPH2411",
        ]

        def random_android_model():
            return random.choice(ANDROID_MODELS)

        def random_chrome_version():
            major = 85 + random.randint(0, 14)  # 85-99
            build = random.randint(1000, 9000)  # 1000-8999
            return f"{major}.0.{build}.120"

        model = random_android_model()
        chrome_version = random_chrome_version()
        self.user_agent = (f"Mozilla/5.0 (Linux; Android 12; {model} Build/SP1A.210812.015; wv) "
                           f"AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_version} Mobile Safari/537.36")

    print(episode_data['shortPlayEpisodeInfos'])
    pass

