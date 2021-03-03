
# https://github.com/JaidedAI/EasyOCR
"""
D:/OneDrive/图片/getcaptcha (1).jpg
"""


import requests
import base64


base_url = r'https://192.168.5.29'


def make_captcha_key():
    """"""
    res_key = requests.get(url=base_url + '/API/captcha/makecaptchakey', verify=False).json()
    captcha_key = res_key['datas']['captchaKey']
    # print(captcha_key)
    return captcha_key


def make_captcha():
    """"""
    captcha_key = make_captcha_key()
    data = {'captchaKey': captcha_key, 'clientType': 'android'}
    print(data)
    res_captcha = requests.get(url=base_url + '/API/captcha/makecaptcha', verify=False, params=data)
    if res_captcha:
        print(res_captcha)
        with open('captcha.jpg', 'wb') as f:
            f.write(res_captcha.content)
        img = base64.b64encode(res_captcha.content)
        print(img)
        return img


def get_access_token():
    """"""
    host = r'https://aip.baidubce.com/oauth/2.0/token'
    client_id = 'zSxnLlO475KcRpeMriGLASVD'
    client_secret = 'OaTP14WB40TzvueKWuhI9FG43b7u1oP0'
    data = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    response = requests.get(url=host, params=data)
    if response:
        res_access_token = response.json()
        access_token = res_access_token['access_token']
        return access_token


def general_basic():
    """"""
    url = r'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    # access_token = get_access_token()
    access_token = "24.e84eede37a6685bc593cae677f513970.2592000.1587881246.282335-19107930"
    img = make_captcha()
    data = {"image": img}
    params = {'access_token': access_token}
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(url=url, headers=headers, params=params, data=data)
    if response:
        # print(response.json())
        captcha_value = response.json()['words_result'][0]
        print(captcha_value)
        return captcha_value


def accurate_basic():
    """"""
    accurate_url = r'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'
    access_token = "24.e84eede37a6685bc593cae677f513970.2592000.1587881246.282335-19107930"
    img = make_captcha()
    data = {"image": img}
    params = {'access_token': access_token}
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(url=accurate_url, headers=headers, params=params, data=data)
    if response:
        print(response.json())


if __name__ == '__main__':
    # make_captcha_key()
    # make_captcha()
    # print(get_access_token())
    # general_basic()
    accurate_basic()
