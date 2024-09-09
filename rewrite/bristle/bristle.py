import requests
import logging
import time
import ssl

from requests.auth import HTTPBasicAuth
from websockets.asyncio.client import connect

from .utils import find_LCU_process, parse_cmdline_args


MAX_LCUX_SEARCH_RETRIES = 3


class Bristle:
    def __init__(self):
        # Search for LCU Process
        self.lcu_found = False
        lcu_process = find_LCU_process()
        retry_count = 0
        while not lcu_process and retry_count < MAX_LCUX_SEARCH_RETRIES:
            logging.warning("Could not find LCUx Process, re-searching %s more time(s)...", MAX_LCUX_SEARCH_RETRIES - retry_count)
            time.sleep(0.5)
            lcu_process = find_LCU_process()
            retry_count += 1
        if lcu_process:
            logging.info("LCUx Process found")
            self.lcu_found = True
        
        if self.lcu_found:
            process_args = parse_cmdline_args(lcu_process.cmdline())
            self._lcu_port = process_args['app-port']
            self._lcu_token = process_args['remoting-auth-token']
            self._lcu_auth = HTTPBasicAuth('riot', self._lcu_token)
    
    async def connect_ws(self):
        uri = f"wss://riot:{self._lcu_token}@127.0.0.1:{self._lcu_port}"

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with connect(uri, ssl=ssl_context) as websocket:
            return websocket
    
    def get(self, endpoint: str) -> requests.Response:
        return requests.get(
            url=f'https://127.0.0.1:{self._lcu_port}/{endpoint}',
            verify=False,
            auth=self._lcu_auth
        )
