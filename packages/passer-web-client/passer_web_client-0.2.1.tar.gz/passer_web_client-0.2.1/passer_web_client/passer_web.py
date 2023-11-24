"""
@author: Daryl.Xu <xuziqiang@zyheal.com
"""
import base64
from dicomweb_client.api import DICOMwebClient
import requests

from .exceptions import PasserWebException


class PasserWebConfig:
    def __init__(self, token: str, base_url: str, user: dict = {}):
        self._token = token
        # user暂时使用dict存储
        self._user = user
        assert not base_url.endswith('/')
        self._base_url = base_url
        self._dicom_web_base_url = f'{base_url}/dicom-web'
        self.dicom_web_client = DICOMwebClient(
            url=self._dicom_web_base_url,
            headers={
                'Girder-Token': token
            }
        )
        if not user:
            self._user = self._get_user_by_token()

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
            raise PasserWebException('Failed to get user info')
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
        return PasserWebConfig(user['authToken']['token'], base_url, user)

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
            raise PasserWebException('Invalid token | 无效的token')
        return res.json()

    @property
    def token(self) -> str:
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