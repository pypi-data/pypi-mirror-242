"""
@author: Daryl.Xu <xuziqiang@zyheal.com
"""
import base64
from datetime import datetime, timezone

from dicomweb_client.api import DICOMwebClient
import requests

from .exceptions import PasserWebException


class PasserWebConfig:
    def __init__(self, token: str, base_url: str, user: dict = {}, 
                 token_obj: dict={}, login_id: str = None,
                 password: str = str, try_get_user: bool = True):
        self._token = token
        # user暂时使用dict存储
        self._user = user
        self._login_id = login_id
        self._password = password
        assert not base_url.endswith('/')
        self._base_url = base_url
        self._dicom_web_base_url = f'{base_url}/dicom-web'
        self.dicom_web_client = DICOMwebClient(
            url=self._dicom_web_base_url,
            headers={
                'Girder-Token': token
            }
        )
        if not user and try_get_user:
            self._user = self._get_user_by_token()
        if not token_obj:
            # 查询token的过期时间
            res = requests.get(f'{base_url}/api/v1/token/current',
                               headers={'Girder-Token': self._token})
            if res.status_code != 200:
                raise PasserWebConfig(f'Failed to get token information')
            self._token_obj = res.json()

    @staticmethod
    def get_user_by_password(login_id: str, password: str,
                             base_url: str) -> str:
        result = login_id + ':' + password
        b = base64.encodebytes(result.encode('utf-8'))
        authorization = b.decode('utf-8').strip()
        headers = {
            'Authorization': 'Basic {0}'.format(authorization),
        }

        response = requests.get(f'{base_url}/api/v1/user/authentication_get',
                                headers=headers)
        if response.status_code != 200:
            raise PasserWebException(f'Failed to get user info: {response.status_code}, {response.text}')
        return response.json()[0]

    @staticmethod
    def from_password(login_id: str, password: str,
                      base_url: str):
        """使用密码获取token，然后返回一个PasserWebConfig

        Args:
            login_id (str): The login id of passer system
            password (str):
            base_url (str): base url of passer-web, http://stable.218.com:9999

        Returns:
            PasserWebConfig:
        """
        assert not base_url.endswith('/')
        user = PasserWebConfig.get_user_by_password(
            login_id, password, base_url)
        return PasserWebConfig(user['authToken']['token'], base_url, user, 
                               login_id=login_id, password=password)

    def _get_user_by_token(self) -> dict:
        """使用token获取用户信息

        必须要保证token有效，如果token无效，DICOM的上传也不提示无权限，
        cherrypy会直接解析DICOM文件，然而它又解析不了，导致奇奇怪怪的
        错误提示，难以debug
        """
        res = requests.get(
            f'{self._base_url}/api/v1.1/user/me',
            headers={'Girder-Token': self._token}
        )
        if res.status_code != 200 or res.text == 'null':
            raise PasserWebException(f'无效的token: {self._token}\n'
                                     f'服务器的响应: {res.text}')
        return res.json()
    
    def apply_newer_token(self) -> str:
        """
        TODO 这个操作应当client来承担，config只是用于保存一些数据
        """
        if self._login_id and self._password:
            user = self.get_user_by_password(
                self._login_id, self._password, self._base_url)
            self._token = user['authToken']['token']
            self._token_obj = user['authToken']
        else:
            print('没有账号与密码，无法申请新的token')

    @property
    def token(self) -> str:
        # 检查token的时效，如果超时。则应当重新申请
        # 2023-12-21T01:28:24.595000+00:00
        token_expires = self._token_obj['expires']
        expires = datetime.fromisoformat(token_expires)
        delta = expires - datetime.now(timezone.utc)
        if delta.seconds < 3600:
            # token有效期小于1小时了，则尝试重新申请token
            self.apply_newer_token()
        elif delta.seconds < 10:
            raise PasserWebConfig(f'token 处于失效的边缘，禁止继续使用')
        return self._token

    @property
    def user(self):
        return self._user

    @property
    def base_url(self):
        return self._base_url

    @property
    def dicom_web_base_url(self):
        return self._dicom_web_base_url