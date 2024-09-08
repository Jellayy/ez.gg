import requests

from requests.auth import HTTPBasicAuth

from .utils import find_LCU_process, parse_cmdline_args


class Bristle:
    def __init__(self):
        lcu_process = find_LCU_process()
        process_args = parse_cmdline_args(lcu_process.cmdline())
        self._lcu_port = process_args['app-port']
        lcu_token = process_args['remoting-auth-token']
        self._lcu_auth = HTTPBasicAuth('riot', lcu_token)
    
    def get(self, endpoint: str) -> requests.Response:
        return requests.get(
            url=f'https://127.0.0.1:{self._lcu_port}/{endpoint}',
            verify=False,
            auth=self._lcu_auth
        )
