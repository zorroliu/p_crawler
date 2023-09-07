# -*- coding: utf-8 -*-

import os
import time
import requests
import urllib3
from urllib.parse import urlparse, unquote
from enum import Enum
from base.config import default_config
from base.logger import http_log, LogLevel

# 隐藏不安全请求的警告
urllib3.disable_warnings()

HEADER_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'


def get_proxies_ip():
    try:
        resp = requests.get(default_config.get_val('proxy_addr'))
        if resp.status_code == 200:
            return resp.text

        return None
    except (BaseException, Exception):
        return None


def req_data(url: str = None, encoding: str = 'utf-8', params: dict = None, json: dict = None,
             method: HttpMethod = HttpMethod.GET, proxy: bool = False, headers=None, verify: bool = False):
    try:
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
            }
        ip = None
        if proxy:
            ip = get_proxies_ip()
        if ip is not None:
            proxies = {
                'http': 'http://{}'.format(ip)
            }
            if method == HttpMethod.GET:
                resp = requests.get(url=url, proxies=proxies, verify=verify, headers=headers)
            else:
                resp = requests.post(url=url,
                                     headers=headers,
                                     data=params,
                                     json=json,
                                     proxies=proxies,
                                     verify=verify)
        else:
            if method == HttpMethod.GET:
                resp = requests.get(url=url, verify=verify, headers=headers)
            else:
                resp = requests.post(url=url,
                                     headers=headers,
                                     data=params,
                                     json=json,
                                     verify=verify)
        http_log.log(f"【{url}】请求成功; 返回状态码: {resp.status_code}")
        if resp.status_code != 200:
            return None

        resp.encoding = encoding
        return resp.text
    except (BaseException, Exception) as e:
        http_log.log(f"【{url}】请求失败; Reason: {e}", LogLevel.ERROR)
        return None


def req_data_retry(url: str = None, encoding: str = 'utf-8', params: dict = None, json: dict = None,
                   method: HttpMethod = HttpMethod.GET, proxy: bool = False, headers=None, verify: bool = False,
                   retry: bool = True, retry_num: int = 3):
    if retry:
        retry_index = 1
        resp = None
        while retry_index < retry_num:
            resp = req_data(url, encoding, params, json, method, proxy, headers, verify)
            retry_index += 1
            if resp is None:
                time.sleep(5)
                continue
            break
        return resp
    else:
        return req_data(url, encoding, params, json, method, proxy, headers, verify)


def download_data(url, headers=None, ext_file_name: str = None, specified_file_path: str = None, max_retry: int = 3):
    retry_count = 0

    if headers is None:
        headers = {}

    if specified_file_path:
        file_path = specified_file_path
    else:
        if ext_file_name:
            file_path = os.path.join(default_config.get_val('base_output_path'), ext_file_name)
        else:
            file_path = os.path.join(default_config.get_val('base_output_path'),
                                     urlparse(unquote(url)).path.split('/')[-1])

    while retry_count < max_retry:
        retry_count += 1
        try:
            resp = requests.get(url, headers=headers, stream=True, verify=False)
            http_log.log(f'【{url}】请求成功; 返回状态码: {resp.status_code}; 文件地址: {file_path}')
            if resp.status_code == 200 or resp.status_code == 206:
                with open(file_path, 'wb') as f:
                    for content in resp.iter_content(chunk_size=1024):
                        f.write(content)
                break
            raise Exception(f'{url}返回状态码{resp.status_code}')
        except (BaseException, Exception) as e:
            http_log.log(f"【{url}】下载失败, 第{retry_count}次重试; Reason: {e}", LogLevel.ERROR)
            time.sleep(3)
