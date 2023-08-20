# -*- coding: utf-8 -*-

import os
from urllib.parse import urlparse, unquote
import asyncio
import aiofile
from base.config import default_config
from base.logger import http_log, LogLevel


async def fetch_req(session, url: str = '', headers=None, max_retry: int = 3):
    if headers is None:
        headers = {}

    retry_count = 0
    while retry_count < max_retry:
        try:
            async with session.get(url=url, ssl=False, headers=headers) as resp:
                data = None
                if resp.status == 200:
                    data = await resp.text(encoding='utf-8')
                return data
        except (BaseException, Exception) as e:
            http_log.log(f"【{url}】请求失败, 第{retry_count}次重试; Reason: {e}", LogLevel.ERROR)
            await asyncio.sleep(3)


async def download_data(session, url, headers=None, ext_file_name: str = None,
                        specified_file_path: str = None, max_retry: int = 3):
    if not specified_file_path:
        if ext_file_name:
            file_path = os.path.join(default_config.get_val('base_output_path'), ext_file_name)
        else:
            file_path = os.path.join(default_config.get_val('base_output_path'),
                                     urlparse(unquote(url)).path.split('/')[-1])
    else:
        file_path = specified_file_path

    if headers is None:
        headers = {}

    retry_count = 0
    while retry_count < max_retry:
        retry_count += 1
        try:
            async with session.get(url, ssl=False, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    async with aiofile.async_open(file_path, 'wb') as file:
                        await file.write(data)
                    break
                raise Exception(f'{url}返回状态码{resp.status_code}')
        except (BaseException, Exception) as e:
            http_log.log(f"【{url}】下载失败, 第{retry_count}次重试; Reason: {e}", LogLevel.ERROR)
            await asyncio.sleep(3)
