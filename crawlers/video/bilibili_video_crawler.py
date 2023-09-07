# -*- coding: utf-8 -*-

import os
import re
import json
from urllib.parse import unquote, urlparse
from util.http_util import req_data, download_data
from util.regular_util import match_only_one
from util.file_util import dir_exists_or_create
from util.ffmpeg_util import extract_audio, extract_video, merge_audio_video
from base.config import default_config
from crawlers.base_crawler import BaseCrawler
from base.data_processing import ToSQLProcessing

HEADER = {
    'Accept': '*/*',
    'Accept-Encoding': 'identity',
    'Accept-Language': 'zh-CN,zh;q=0.9,ru;q=0.8',
    'Cache-Control': 'no-cache',
    'Origin': 'https://www.bilibili.com',
    'Pragma': 'no-cache',
    'Range': 'bytes=0-999999999',
    'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 '
                  'Safari/537.36'
}

BASE_PATH = default_config.get_val('base_output_path')


#  参考地址:https://github.com/SocialSisterYi/bilibili-API-collect

class BilibiliVideoCrawler(BaseCrawler, ToSQLProcessing):
    def __init__(self):
        super(BilibiliVideoCrawler, self).__init__()
        self.base_url = "https://www.bilibili.com"
        self._bv_no = 'BV1Dp4y1E7ko'
        self._dir = None
        self._video_name = None
        self._audio_name = None

    def before(self):
        self._dir = os.path.join(BASE_PATH, self._bv_no)
        dir_exists_or_create(self._dir)

    def _producer(self):
        HEADER['Referer'] = f'https://www.bilibili.com/video/{self._bv_no}'
        try:
            page = req_data(f'{self.base_url}/video/{self._bv_no}', headers=HEADER)
            play_info_str = match_only_one(re.escape("<script>window.__playinfo__=") + "(.*?)" + re.escape("</script>"),
                                           page)
            play_info = json.loads(play_info_str)
            video_uri = play_info['data']['dash']['video'][1]['baseUrl']
            self._video_name = urlparse(unquote(video_uri)).path.split('/')[-1]
            self._buffer.put({
                'file_path': os.path.join(self._dir, self._video_name),
                "uri": video_uri
            })
            audio_uri = play_info['data']['dash']['audio'][0]['baseUrl']
            self._audio_name = urlparse(unquote(audio_uri)).path.split('/')[-1]
            self._buffer.put({
                'file_path': os.path.join(self._dir, self._audio_name),
                "uri": audio_uri
            })
            self._producer_end()
        except (BaseException, Exception):
            self._producer_end()

    @staticmethod
    def _process_data(item):
        download_data(item['uri'], specified_file_path=item['file_path'], headers=HEADER)

    def after(self):
        video_path = os.path.join(self._dir, self._video_name.replace('.m4s', '.mp4'))
        audio_path = os.path.join(self._dir, self._audio_name.replace('.m4s', '.mp3'))
        extract_audio(os.path.join(self._dir, self._audio_name), audio_path)
        extract_video(os.path.join(self._dir, self._video_name), video_path)
        merge_audio_video(video_path, audio_path, os.path.join(self._dir, f'{self._bv_no}.mp4'))


if __name__ == "__main__":
    crawler = BilibiliVideoCrawler()
    crawler.start()
