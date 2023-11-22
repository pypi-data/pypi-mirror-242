import http
import json
import os.path
import uuid
import requests
from minio import Minio
from minio.error import S3Error
from progress import Progress


# ADMIN_HOST = "http://dev06.ucd.qzm.stonewise.cn:30022"


# ADMIN_HOST = "localhost:8080"


class PandoraBox:
    def __init__(self, username, password, admin_host):
        self.admin_host = admin_host
        if username == "":
            print("Login failed, param username is empty")
            return
        if password == "":
            print("Login failed, param password is empty")
            return
        info = json.dumps({
            'username': username,
            'password': password
        })
        resp = self._login_req(info)
        if resp.status_code == http.HTTPStatus.BAD_REQUEST:
            if resp.text == "":
                return
            print(f"Login failed, err msg:{resp.json().get('msg')}")
            return
        if resp.status_code == http.HTTPStatus.OK:
            if resp.text == "":
                return
            code = resp.json().get("code")
            if code != 0:
                print(f"Login failed, err msg:{resp.json().get('msg')}")
                return
            self.key = resp.json()['gateway_info']['access_key']
            self.secret = resp.json()['gateway_info']['access_secret']
            self.bucket = resp.json()['gateway_info']['bucket']
            self.gateway = resp.json()['gateway_info']['gateway']
        self.client = Minio(
            self.gateway,
            access_key=self.key,
            secret_key=self.secret,
            secure=False,
        )
        self.user = username
        self.is_login = True
        print("Login succeeded")
        return

    def model_init(self, model_name, description, library, data_set, task):
        if not self.is_login:
            print("User is not login")
            return
        if model_name == "":
            print("Param model_name is empty")
            return
        info = json.dumps({
            'model_name': model_name,
            'description': description,
            'library': library,
            'data_set': data_set,
            'task': task,
            'creator': self.user,
        })
        resp = self._new_model_req(info)
        print(resp.text)

    def my_models(self):
        if not self.is_login:
            print("User is not login")
            return
        resp = self._get_user_model_list_req()
        if resp.status_code != http.HTTPStatus.OK:
            print(resp.status_code)
            return
        print(resp.json().get("data"))
        return resp.json().get("data")

    def get_model(self, model_name, tag, destination_path):
        if not self.is_login:
            print("User is not login")
            return
        if tag == "":
            print("Param tag is empty")
            return
        if model_name == "":
            print("Param model_name is empty")
            return
        if os.path.isfile(destination_path):
            print("Param destination_path must be a folder")
            return
        if not os.path.exists(destination_path):
            print("Destination_path is not exist")
            return
        resp = self._get_tag_storage_path_req(model_name, tag)
        if resp.status_code == http.HTTPStatus.BAD_REQUEST:
            print(resp.text)
            return
        blob_path = resp.json().get("blob_path")
        if os.path.isdir(destination_path):
            objects = self.client.list_objects(
                self.bucket, recursive=True, prefix=blob_path,
            )
            for obj in objects:
                parts = obj.object_name.split('/')
                if len(parts) > 4:
                    full_path = '/'.join(parts[3:])
                else:
                    full_path = ''
                err = self._download(obj.object_name, os.path.join(destination_path, full_path))
                if err != "":
                    return err

            print("Files download successfully.")
        return

    def version_list(self, model_name):
        if not self.is_login:
            print("User is not login")
            return
        resp = self._get_model_version_list_req(model_name)
        if resp.status_code != http.HTTPStatus.OK:
            print(resp.status_code)
            return
        print(resp.json().get("version_list"))
        return resp.json().get("version_list")

    def register_model(self, model_name, tag, local_path):
        if not self.is_login:
            print("User is not login")
            return
        if model_name == "":
            print("Param model_name is empty")
            return
        if local_path == "":
            print("Param local_path is empty")
            return
        if tag == "":
            print("Param tag is empty")
            return
        blob_path = ""
        guid = str(uuid.uuid4())
        resp = self._get_model_id_req(model_name)
        if resp.status_code == http.HTTPStatus.BAD_REQUEST:
            print(resp.json().get("msg"))
            return
        if resp.status_code != http.HTTPStatus.OK:
            print(resp.status_code)
            return
        if os.path.isfile(local_path):
            folder_name = os.path.basename(os.path.dirname(local_path))
            file_name = os.path.basename(local_path)
            destination_path = "/models/{model_name}/{guid}/{folder_name}/{file_name}".format(model_name=model_name,
                                                                                              guid=guid,
                                                                                              folder_name=folder_name,
                                                                                              file_name=file_name)
            err = self._upload(local_path, destination_path)
            if err != "":
                return
            blob_path = destination_path
            print("File uploaded successfully.")
        elif os.path.isdir(local_path):
            allfiles = _allfiles(local_path)
            for file in allfiles:
                master_folder_name = os.path.basename(os.path.dirname(local_path))
                file_path = file.split(master_folder_name + '/')[1]
                destination_path = os.path.join('models', model_name, guid, file_path)
                source_path = os.path.join(local_path, file)
                err = self._upload(source_path, destination_path)
                if err != "":
                    return
            blob_path = "/models/{model_name}/{guid}/".format(model_name=model_name, guid=guid)
            print("Files uploaded successfully.")
        else:
            print("Please input right path")

        info = json.dumps({
            'model_name': model_name,
            'tag': tag,
            'blob_path': blob_path,
            'guid': "{guid}".format(guid=guid),
        })
        address = self._add_model_version_req(info)
        if address.status_code == http.HTTPStatus.BAD_REQUEST:
            print(address.json().get("msg"))
            return
        if resp.status_code != http.HTTPStatus.OK:
            print(resp.status_code)
            return

    def _upload(self, local_path, destination):
        try:
            self.client.fput_object(
                self.bucket,
                destination,
                local_path,
                progress=Progress(),  # 在回调中调用线程对象的run方法
            )
            print("File uploaded successfully.")
            return ""
        except S3Error as err:
            print("Error: ", err)
            return err

    def _download(self, source, destination):
        try:
            # Download data of an object.
            self.client.fget_object(
                self.bucket,
                source,
                destination,
                progress=Progress(),  # 在回调中调用线程对象的run方法
            )
            return ""
        except S3Error as err:
            print("Error: ", err)
            return err

    # def _delete_model_version_req(self, model_name, model_version):
    #     base_url = "http://{host}/api/v1/model/version/{model_name}/{model_version}" \
    #         .format(host=ADMIN_HOST, model_name=model_name, model_version=model_version)
    #     resp = requests.delete(url=base_url)
    #     return resp
    #
    # def _delete_model_tag_req(self, model_name, model_tag):
    #     base_url = "http://{host}/api/v1/model/tag/{model_name}/{model_tag}" \
    #         .format(host=ADMIN_HOST, model_name=model_name, model_tag=model_tag)
    #     resp = requests.delete(url=base_url)
    #     return resp
    #
    # def _delete_model_req(self, model_name):
    #     base_url = "http://{host}/api/v1/model/{model_name}" \
    #         .format(host=ADMIN_HOST, model_name=model_name)
    #     resp = requests.delete(url=base_url)
    #     return resp

    def _get_model_id_req(self, model_name):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/{model_name}/id" \
            .format(host=self.admin_host, model_name=model_name)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_model_info_req(self, model_name):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/{model_name}/info" \
            .format(host=self.admin_host, model_name=model_name)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_tag_storage_path_req(self, model_name, model_tag):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/tag/{model_name}/{model_tag}/storage" \
            .format(host=self.admin_host, model_name=model_name, model_tag=model_tag)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_version_storage_path_req(self, model_name, model_version):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/version/{model_name}/{model_version}/storage" \
            .format(host=self.admin_host, model_name=model_name, model_version=model_version)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_model_version_list_req(self, model_name):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/{model_name}/version/list" \
            .format(host=self.admin_host, model_name=model_name)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_user_model_list_req(self):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/{username}/model/list" \
            .format(host=self.admin_host, username=self.user)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _add_model_version_req(self, json_info):
        headers = {'Content-Type': 'application/json', 'username': self.user}
        base_url = "{host}/api/v1/model/version/add".format(host=self.admin_host)
        resp = requests.post(url=base_url, data=json_info, headers=headers)
        return resp

    def _new_model_req(self, json_info):
        headers = {'Content-Type': 'application/json', 'username': self.user}
        base_url = "{host}/api/v1/model/init".format(host=self.admin_host)
        resp = requests.post(url=base_url, data=json_info, headers=headers)
        return resp

    def _login_req(self, json_info):
        headers = {'Content-Type': 'application/json'}
        base_url = "{host}/api/v1/login".format(host=self.admin_host)
        resp = requests.post(url=base_url, data=json_info, headers=headers)
        return resp

    def get_login_status(self):
        return self.is_login


def _allfiles(folder):
    filepath_list = []
    for root, folder_names, file_names in os.walk(folder):
        for file_name in file_names:
            file_path = root + os.sep + file_name
            filepath_list.append(file_path)
            print(file_path)
    # file_path = sorted(file_path, key=str.lower)
    return filepath_list
