import json
from typing import List
import requests
import os
import shutil
import zipfile
import pydicom
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .passer_web import PasserWebConfig


class PasserWebException(Exception):
    def __init__(self, msg=''):
        super().__init__(f'passer-web -> {msg}')


class PasserWebClient:
    def __init__(self, passer_web: PasserWebConfig):
        self.config = passer_web

    @classmethod
    def from_password(cls, login_id: str, password: str, base_url: str):
        """使用密码创建客户端对象

        Args:
            login_id (str): 登录名
            password (str): 密码
            base_url (str): 服务器地址

        Returns:
            _type_: _description_
        """
        config = PasserWebConfig.from_password(login_id, password, base_url)
        return cls(config)
    
    @classmethod
    def from_token(cls, token, base_url: str, user: dict={}):
        """使用token创建客户端对象

        Args:
            token (_type_): token令牌
            base_url (str): 服务器地址
            user (dict, optional): 用户对象. Defaults to {}.

        Returns:
            _type_: _description_
        """
        config = PasserWebConfig(token, base_url, user)
        return cls(config)

    def _get_url_token(self):
        return self.config.base_url, self.config.token

    def get_collection(self, text='', limit=100, offset=0, sort='', sortdir=1):
        """获取数据集列表
            text(str): 搜索数据集相关文字
            limit(number):  结果数量限制
            offset(number): 获取数据集开始位置
            sort(str):  结果排序标识
            sortdir(number):  1(正序)/-1(反序)
        """
        params = {
                "limit": limit,
                "offset": offset,
                "sortdir": sortdir
            }
        if text:
            params['text'] = text
        if sort:
            params['sort'] = sort
        return self.get(
            '/api/v1/collection',
            params=params
        ).json()
    
    def get_study(self, collection_id: str, study_instance_uid: str):
        """获取study
            collection_id(str): study所在数据集ID
            study_instance_uid(str):  studyInstanceUID
        """
        return self.get(
                f'/api/v1.1/dicom/study/{study_instance_uid}?collection_id={collection_id}',
                params={}
            ).json()

    def get_enabled_task_type(self, collection_id: str):
        """获取可用任务类型
            collection_id(str): 数据集ID
        """
        return self.get(
                f'/api/v1.1/collection/{collection_id}/enabled_task_type',
                params={}
            ).json()

    def get_enabled_organization(self, collection_id: str):
        """获取可用组织机构
            collection_id(str): 数据集ID
        """
        return self.get(
                f'/api/v1.1/collection/{collection_id}/enabled_organization',
                params={}
            ).json()

    def create_task(self, task_type: str, task_params: dict) -> dict:
        endpoint = f'/api/v1/task'
        params = {
            'type_': task_type
        }
        res = self.post(endpoint, params=params, json=task_params)
        return res.json()

    def create_task_pipeline(self, task_params: dict) -> dict:
        """创建一个任务
        Args:
            task_params(object): 任务相关参数
            example: 
            {
                "comment":"",
                "type":"liver_worker2.zyheal.surgical",
                "organization":"zyheal",
                "collection":"64a2282a33e85c6f32b39706",
                "data_type":"study",
                "data_id":"1.2.840.113564.345049151876.8956.638167395925423188.3234",
                "parameters":{
                    "data":{
                        "main":{
                            "StudyInstanceUID":"1.2.840.113564.345049151876.8956.638167395925423188.3234",
                            "type":"dicom.study"
                        },
                        "venous":{
                            "type":"dicom.series",
                            "SeriesInstanceUID":"1.3.46.670589.11.78251.5.0.8312650871319207276885709780726875151",
                            "StudyInstanceUID":"1.2.840.113564.345049151876.8956.638167395925423188.3234"
                        },
                        ...
                    },
                    "options":{
                        "seg_mode":"auto",
                        "reslice":true,
                        "range_begin":22,
                        "comment":"testtest"
                    }
                }
            }
        Returns:
            dict: 返回task对象
            example: 
            {
                "id": "20a86f58-f9f5-45b0-aa3b-33979db04f78",
                "creator": "60ee9e1f5c80370bee8c87a9",
                "type": "liver_worker2.zyheal.visualization_ct",
                "collection": "61970d2dd4015823bc12562f",
                "data_type": "study",
                "data_id": "1.2.840.113619.2.248.114374074066724.31333.1678232334073.2",
                "current_stage": "auto_segmentation",
                "_id": "20a86f58-f9f5-45b0-aa3b-33979db04f78",
                "type_": "liver_worker2.zyheal.visualization_ct",
                "PatientID": "AW1028887959.34.1678232334",
                "patient_name_ground": "陆梦涛",
                "StudyID": null,
                "StudyDate": "2023-03-03",
                "parameters": {
                    ...
                },
                "comment": "",
                "status": "failed",
                "exception": "RuntimeError('Killed\\n')",
                "create_date": "2023-08-04T07:46:31.780+00:00",
                "start_date": null,
                "update_date": "2023-08-04T07:57:20.783+00:00",
                "stages": {
                    ...
                }
            },
        """
        endpoint = f'/api/v1.1/task/pipeline'
        params = {}
        res = self.post(endpoint, params=params, json=task_params)
        return res.json()


    def download_task_file(self, task_id: str, relative_path: str, target_path: str):
        """从Passer下载文件

        Args:
            task_id (str): uid
            relative_path (str): passer存储的相对路径
            target_path (str): 目标位置
        """
        # raise Exception('请编写新的文件下载接口，从/api/v1.1/task/file下载文件')
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        url = f'{base_url}/api/v1.1/task/{task_id}/file?path={relative_path}'
        
        res = requests.get(url, headers=header)
        self._assert_200(res)
        _dir = os.path.dirname(target_path)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        f = open(target_path, 'wb')
        f.write(res.content)
        f.close()


    def download_task_folder(self, task_id: str, relative_path: str, target_path: str):
        """从Passer下载文件夹压缩包, 然后解压

        Args:
            task_id (str): uid
            relative_path (str): passer存储的相对路径
            target_path (str): 目标位置
            passer_web (PasserWebConfig): passer web config
        """
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        # 下载文件夹压缩包
        url = f'{base_url}/api/v1.1/task/{task_id}/folder?path={relative_path}'
        res = requests.get(url, headers=header)
        self._assert_200(res)
        # 保存目录不存在则需要创建
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        tmp_zip_path = target_path + '.zip'
        with open(tmp_zip_path, 'wb') as f:
            f.write(res.content)
        # 解压
        target_dir = os.path.dirname(target_path)
        relative_basename = os.path.basename(relative_path)
        with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        os.remove(tmp_zip_path) # 删除压缩包
        extract_path = os.path.join(target_dir, relative_basename) # 解压后的文件夹
        if extract_path != target_path:
            # 如果下载的文件夹名称和保存的名称不一样就要对解压的文件夹进行重命名
            shutil.rmtree(target_path)
            os.rename(extract_path, target_path)
        print(f'文件夹下载完成, 路径: {target_path}')


    def upload_task_file(self, task_id: str, file: str, relative_path: str) -> dict:
        """上传任务文件,文件大于5M时分片

        Args:
            task_id (str): [description]
            file (str): [description]
            relative_path (str): [description]
        """
        def upload_directly():
            params = {
                'path': relative_path,
                'token': token
            }
            url = f'{base_url}/api/v1.1/task/{task_id}/file'
            data = MultipartEncoder(fields={
                'file': (f.name, f, 'application/octet-stream')
            })
            res = requests.post(url, data=data, params=params,
                        headers={'Content-Type': data.content_type})
            self._assert_200(res)
            return res.json()
        max_chunk_size = 5*1024*1024
        f = open(file, 'rb')
        file_size = os.path.getsize(file)
        base_url, token = self._get_url_token()
        # 判断是否分片
        if (file_size > max_chunk_size):
            init_upload_url = f'{base_url}/api/v1.1/task/{task_id}/init_upload'
            init_params = {
                'path': relative_path,
                'size': file_size,
                'override': 'true',
                'token': token
            }
            init_upload_res = requests.post(init_upload_url, params=init_params)
            # 如果分片上传失败，尝试直接上传
            if init_upload_res.status_code != 200:
                if file_size < 10*1024*1024:
                    print(f'初始化分片失败，尝试直接上传, 错误：{init_upload_res.text}')
                    return upload_directly()
                else:
                    self._assert_200(init_upload_res, '文件过大，且分片时出错：')

            upload_id = init_upload_res.json().get('_id')

            offset = 0
            upload_finished = False
            upload_chunk_url = f'{base_url}/api/v1.1/task/{task_id}/chunk'
            # 开始分片上传
            while not upload_finished:
                header = {
                    'Content-Type': 'application/octet-stream'
                }
                chunk_params = {
                    'upload_id': upload_id,
                    'offset': offset,
                    'token': token
                }
                
                if (offset + max_chunk_size > file_size):
                    max_chunk_size = file_size - offset
                chunk_res:dict = requests.post(upload_chunk_url, data=f.read(max_chunk_size), params=chunk_params, headers=header).json()
                offset += max_chunk_size
                if offset >= file_size :
                    upload_finished = True
            
            # 验证是否上传完成
            if chunk_res.get('downloadUrl') is None:
                raise RuntimeError('文件分片上传失败')
            else:
                print(f'{f.name}分片上传成功')
            return chunk_res 
        # 不分片
        else:
            return upload_directly()


    def upload_dcm_file(self, collection_id: str, file: str) -> dict:
        """上传DCM文件

        Args:
            collection_id (str): collection_id
            file (str): full file path
        """
        base_url, token = self._get_url_token()
        url = f'{base_url}/api/v1.1/dicom/instance?collectionId={collection_id}'
        with open(file, 'rb') as dcm_data:
            res = requests.post(url, data=dcm_data,
                        headers={
                            'Girder-Token': token,
                            'Content-Type': 'application/octet-stream'
                        })
            self._assert_200(res)
        return res.json()

    def apply_for_read_only_token(self, token_type, duration=60):
        """使用api key申请一个只读token, 
        Args:
            token_type: token的类型目前只有passer.read_only
            duration: token有效期,最大365,默认60
        Returns:
            dict: 返回一个有只读权限的token
            example: {
                "expires": "2023-05-29T06:29:22.679+00:00",
                "scope": [
                    "core.data.read"
                ],
                "token": "nsvkcVLMYJsXPJi9zsx4yIb6xgsegeol9gbqN2H6nx2j0GQ3jbic6puB2tM2f4aa"
            }
        """
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        apply_url = f'{base_url}/api/v1.1/token/?type={token_type}?duration={duration}'
        res = requests.post(apply_url, headers=header)
        self._assert_200(res,'申请只读token失败:')
        read_only_token:dict = res.json()['authToken']
        return read_only_token


    def get_collection_collaborator(self, collection: str, roles: list=["admin", "annotator", "planner", "customer", "reviewer"]):
        '''获取某个数据集的角色用户列表, 例如: 获取qj数据集的所有角色为管理员和标注员的用户
            Args:
                collection(str): 数据集id
                roles(list): 需要获取数据集的角色列表, 目前有五种角色["admin", "annotator", "planner", "customer", "reviewer"]
            Returns:
                list: 返回具有这个角色权限的用户列表
        '''
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        url = f'{base_url}/api/v1.1/collection/{collection}/collaborator'
        res = requests.get(url, headers=header)
        self._assert_200(res, '获取数据集协作者失败:')
        result_list = []
        all_collaborator: list = res.json()['data']
        for user_obj in all_collaborator:
            role_set:set = set(user_obj['roles'])
            flag:bool = not set(roles).isdisjoint(role_set) # 判断是否有交集，有则说明这个用户是对应的角色
            if flag:
                result_list.append(user_obj)
        if len(result_list) == 0:
            print(f'Warning: 获取数据集{collection}角色列表{roles}为空，注意核对')
        return result_list


    def send_notification(self, content: str, collection: str, receiver_list: list):
        """向ground发送通知, 
            Args:
                content (str): 通知内容
                collection(str): 数据集的id
                receiver_list(list[dict]): 接收者的列表,元素是包含id, lastname等用户信息的用户字典
            Returns:
                None
        """
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        url = f'{base_url}/api/v1.1/notification'
        # 遍历通知的接收者列表
        for receiver in receiver_list:
            user_id = receiver['id']
            user_name = receiver['firstName']
            notification_data = {
                "content": content,
                "collection_id": collection,
                "receiver_id": user_id,
                "type": "task:general", 
                "comment": "passer-web-client",
                }
            res = requests.post(url, headers= header, json= notification_data)
            if res.status_code != 200:
                print(f'Warning: 给{user_name}通知发送失败, 原因{res.text}')
            else:
                print(f'通知"{content}"已发送，接收人{user_name}')
        return


    def send_notification_by_roles(self, content: str, collection: str, roles: list):
        """向ground发送通知, 指定角色
            Args:
                content (str): 通知内容
                collection(str): 数据集的id
                roles(list): 需要获取数据集的角色列表, 目前有五种角色["admin", "annotator", "planner", "customer", "reviewer"]
            Returns:
                None
        """
        receiver_list = self.get_collection_collaborator(collection, roles)
        self.send_notification(content, collection, receiver_list)


    def upload_dicom_to_dicom_web(self, dcm_path_list:list, study_instance_uid: str):
        """
            上传图像到dicom-web
            Args:
                dcm_path_list (list): dcm文件路径列表
                study_instance_uid (str): 研究实例编号
            Returns:
                None
        """
        success = 0
        failed = 0
        for dcm_path in dcm_path_list:
            if not os.path.exists(dcm_path):
                print(f"Warning:上传dicom时{dcm_path}不存在")
                failed += 1
                continue
            datasets = []
            ds = pydicom.dcmread(dcm_path)
            datasets.append(ds)
            try:
                self.config.dicom_web_client.store_instances(datasets, study_instance_uid) #数据大小超过10MB会出错
                success += 1
            except Exception as e:
                failed += 1
                print(f'{dcm_path}上传失败,未知原因: {e}')
        print(f'上传dicom完成, 成功:{success}, 失败:{failed}')


    def tagging_series(self, series_instance_uid: str, tags: list):
        """给序列打标
        Args:
            series_instance_uid (str): uid
            tags (str): 标签列表, 截止ground1.8版本支持的tag有:
            [
                "liver.other.plain",
                "liver.other.venous",
                "liver.other.arterial",
                "liver.other.delay",
                "liver.other.dwi",
                "liver.other.distinct",
                "liver.other.quant",
                "liver.other.t2",
                "liver.other.m_dixon_all"
            ]
        Returns:
            bool: [是否打标成功]
        """
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        
        # 发送打标（修改series信息）的put请求, 有权限认证，需为数据集的管理员
        tagging_url = f'{base_url}/api/v1.1/dicom/series/{series_instance_uid}'
        payload = {
                "tag": tags
            }
        tagging_response =  requests.put(tagging_url, headers= header, json= payload)
        self._assert_200(tagging_response, '打标失败:')
        print(f'{series_instance_uid}打标成功,{tags}')
        return


    def get_tagged_series(self, study_instance_uid: str, tags: list)->list:
        """获取一个study下已经打标的序列
        Args:
            study_instance_uid (str): 研究实例编号
            tags (str): 标签列表, 截止ground1.8版本支持的tag有:
            [
                "liver.other.plain",
                "liver.other.venous",
                "liver.other.arterial",
                "liver.other.delay",
                "liver.other.dwi",
                "liver.other.distinct",
                "liver.other.quant",
                "liver.other.t2",
                "liver.other.m_dixon_all"
            ]
        Returns:
            dict: 返回series对象
            example: 
            [
                {
                    "contentCreateDate": "2021-10-13 11:33:54.0",
                    "comment": null,
                    "tag": [
                        "liver.other.venous"
                    ],
                    "SeriesDescription": "VmDIXON-W",
                    "SeriesNumber": "1302",
                    "SeriesInstanceUID": "1.3.46.670589.11.42546.5.0.11836.2021101311335471000",
                    "StudyInstanceUID": "1.2.194.0.108707908.20211013110540.1570.10100.3333783",
                    "Modality": "MR"
                },
            ]
        """
        res_series_list = []
        for tag in tags:
            # tag_str = ','.join(tag) # 支持一个序列打多个tag的情况，但目前未用到
            base_url, token = self._get_url_token()
            header = {
                'Cookie': f'girderToken={token}'
                }
            series_url = f'{base_url}/api/v1.1/dicom/study/{study_instance_uid}/series?tag={tag}'
            series_res = requests.get(series_url, headers=header)
            self._assert_200(series_res, '获取打标的序列失败:')
            series_list:list = series_res.json()
            series_obj: dict = {}
            if len(series_list) == 0:
                msg = f'Warning: study下没有tag为{tag}的序列'
            elif len(series_list) >1:
                msg = f'Warning: study下有多个标签为{tag}的序列, 当前取第一个'
                series_obj = series_list[0]
            else:
                msg = f'找到标签为{tag}的唯一序列'
                series_obj = series_list[0]
            print(msg)
            res_series_list.append(series_obj)
        return res_series_list

    def get_series(self, study_instance_uid: str)->list:
        """获取一个study的所有序列
        Args:
            study_instance_uid (str): 研究实例编号
        Returns:
            dict: 返回series对象
            example: 
            [
                {
                    "contentCreateDate": "2021-10-13 11:33:54.0",
                    "comment": null,
                    "tag": [
                        "liver.other.venous"
                    ],
                    "SeriesDescription": "VmDIXON-W",
                    "SeriesNumber": "1302",
                    "SeriesInstanceUID": "1.3.46.670589.11.42546.5.0.11836.2021101311335471000",
                    "StudyInstanceUID": "1.2.194.0.108707908.20211013110540.1570.10100.3333783",
                    "Modality": "MR"
                },
                ...
            ]
        """
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        series_url = f'{base_url}/api/v1.1/dicom/study/{study_instance_uid}/series'
        series_res = requests.get(series_url, headers=header)
        self._assert_200(series_res, '获取序列列表失败:')
        series_list: list = series_res.json()
        series_obj: dict = {}
        if len(series_list) == 0:
            msg = f'Warning: study下没有序列'
            return []
        else:
            return series_list


    def _get_latest_series(self, series: List[dict]):
        """Sort by ContentDate(00080023) and ContentTime(00080033)

        Args:
            series (List[dict]): Series list

        Returns:
            [type]: [description]
        """
        sort_flag = 'content_date_time'
        # 判断每个序列中是否有时间字段
        for i in series:
            # 如果没有content date或者 content time字段就要使用series date/time来进行排序
            if i.get('00080023') is None or i.get('00080033') is None:
                # 判断是否有series date/time 字段, 没有则报错
                if i.get('00080021') is None or i.get('00080031') is None:
                    raise RuntimeError(f"{i['0020000E']['Value'][0]}序列没有SeriesDate/SeriesTime字段，请检查序列")
                else:
                    sort_flag = 'series_data_time'
        
        if sort_flag == 'content_date_time':
            series.sort(key=lambda x: x['00080023']['Value'][0] + x['00080033']['Value'][0])
        elif sort_flag == 'series_data_time':
            series.sort(key=lambda x: x['00080021']['Value'][0] + x['00080031']['Value'][0])

        return series[-1]


    def get_latest_seg(self, study_instance_uid: str,seg_name: str) -> pydicom.Dataset:
        """按照名称获取一个seg(有多个同名seg取最新的)
        Args:
            study_instance_uid(str): 研究实例编号
            seg_name (str): Segmentation name, actually the DIOCM tag SeriesDescription
        Returns:
            pydicom.Dataset: [description]
        """
        # 下载手动分割后的结果，下载最新的分割结果
        client = self.config.dicom_web_client
        res = client.search_for_series(study_instance_uid,
                                       search_filters={
                                           'SeriesDescription': seg_name,
                                           'Modality': 'SEG',
                                       },
                                       fields=['ContentDate', 'ContentTime', 'SeriesDate', 'SeriesTime'])
        if len(res) == 0:
            #如果没找到抛FileNotFoundError异常，便于捕获未找到seg的错误
            raise FileNotFoundError(f'Segmentation {seg_name} not found!')
        # TODO how to sure the client's time is correct?
        if len(res) > 0:
            # 按照 ContentDate和ContentTime进行排序
            series = self._get_latest_series(res)
        else:
            series = res[0]
        series_instance_uid = series['0020000E']['Value'][0]

        dcms = client.retrieve_series(study_instance_uid, series_instance_uid)
        # 一个SEG序列只有一个DICOM文件
        assert len(dcms) == 1
        dcm: pydicom.Dataset = dcms[0]
        return dcm


    def get_scene(self, task_id:str, scene_name='default'):
        """获取一个任务的场景文件(glance)
        Args:
            task_id(str): 任务id
            save_path (str): 保存的路径
            scene_name (str): Segmentation name, actually the DIOCM tag SeriesDescription
        Returns:
            content: [byte]
        """
        base_url, token = self._get_url_token()
        url = f'{base_url}/api/v1.1/task/pipeline/{task_id}/scene?name={scene_name}'
        header = {
            'girder-token': token
        }
        res = requests.get(url, headers=header)
        self._assert_200(res, "获取场景文件失败：")
        return res.content

    def get_pipeline_list(self, collection_id:str, status:str, type='', offset=0, limit=9999, study_instance_uid='', patient_id='', start_date='',end_date=''):
        """获取pipeline列表
        Args:
            type (str): 任务类型
            collection_id(str): collection_id
            status(str): 任务状态
            example:
                created, running, failed, success, checked, rejected, intervention
            offset(int): 返回结果在全部pipeline的偏移
            limit(int): 返回结果最大数量
            study_instance_uid (str): studyInstanceUID 
            patient_id(str): patient_id
            start_date(str): 
            end_date(str): 
        """
        params={
            "type": type,
            "collection": collection_id,
            "status": status,
            "offset": offset,
            "limit": limit,
            "study": study_instance_uid, 
            "patient_id": patient_id,
            "start_date": start_date,
            "end_date": end_date
        }
        base_url, token = self._get_url_token()
        url = f'{base_url}/api/v1.1/task/pipeline'
        header = {
            'girder-token': token
        }
        res = requests.get(url, params=params, headers=header)
        pipelines = res.json()["data"]
        self._assert_200(res, "获取任务列表失败：")
        return pipelines

    def get_series_info(self, series_instance_uid: str):
        """获取一个series的信息, 包含标签tag、起始结束层range等信息
        Args:
            series_instance_uid(str): 序列uid
        Returns:
            series_obj: [dict]
        """
        base_url, token = self._get_url_token()
        header = {
            'Cookie': f'girderToken={token}'
            }
        series_url = f'{base_url}/api/v1.1/dicom/series/{series_instance_uid}'
        series_res = requests.get(series_url, headers=header)
        self._assert_200(series_res, '获取序列失败:')
        series_obj: dict = series_res.json()

        return series_obj


    @staticmethod
    def _assert_200(res: requests.Response, additional_msg:str= ''):
        if res.status_code != 200:
            raise PasserWebException(
                f'status_code: {res.status_code},{additional_msg}{res.text}'
            )

    def get(self, endpoint: str, params={}, headers={}) -> requests.Response:
        """Send a GET request to passer-web.
        发送GET方法请求到passer-web
        为了简便起见，强制要求返回状态码为200
        https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/200

        Args:
            endpoint (str): endpoint of the passer-web, eg: /api/v1/task_type/enabled .
            params (dict, optional): query parameters. Defaults to {}.
            headers (dict, optional): headers. Defaults to {}.

        Returns:
            requests.Response: the response from passer-web
        """
        assert endpoint.startswith('/')
        base_url, token = self._get_url_token()
        url = f'{base_url}{endpoint}'
        params['token'] = token
        headers['User-Agent'] = 'requests.passer_web_client'

        res = requests.get(url, params=params, headers=headers)
        self._assert_200(res)
        return res

    def post(self, endpoint, params={}, json={}, headers={}) -> requests.Response:
        """Send a POST request to passer-web.
        发送POST方法请求到passer-web

        Args:
            endpoint ([type]): endpoint of the passer-web, eg: /api/v1/task .
            params ([type], optional): query parameters. Defaults to {}.
            json (dict, optional): json object as request body. Defaults to {}.
            headers ([type], optional): headers. Defaults to None.

        Returns:
            requests.Response: the response from passer-web
        """
        assert endpoint.startswith('/')
        base_url, token = self._get_url_token()
        url = f'{base_url}{endpoint}'
        params['token'] = token
        headers['User-Agent'] = 'requests.passer_web_client'

        res = requests.post(url, params=params, json=json, headers=headers)
        self._assert_200(res)
        return res
