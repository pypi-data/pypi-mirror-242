import requests

from mediaApiClient.stream_models import ClientStreamResponseV2


class ClientStreamControllerV2:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_stream_for_content(self, content_id, account_id, manifest=None, use_https=None, get_meta_info=None):
        url = f"{self.base_url}/api/v2/stream/contents/{content_id}"
        params = {
            "accountId": account_id
        }

        if manifest is not None:
            params["manifest"] = manifest
        else:
            params["manifest"] = "all"
        if use_https is not None:
            params["useHttps"] = str(use_https).lower()
        else:
            params["useHttps"] = "true"
        if get_meta_info is not None:
            params["getMetaInfo"] = str(get_meta_info).lower()
        else:
            params["getMetaInfo"] = "false"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return ClientStreamResponseV2(**response.json())
        else:
            raise Exception(f"Request failed with status code: {response.status_code} {response.text}")
