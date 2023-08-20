# -*- coding: utf-8 -*-

import time
from crawlers.base_crawler import BaseCrawler
from util.http_util import req_data_retry, download_data
from base.logger import http_log
from bs4 import BeautifulSoup


class WallhavenCrawler(BaseCrawler):
    def __init__(self, max_workers: int = 3, num_consumers: int = 2):
        super(WallhavenCrawler, self).__init__(max_workers, num_consumers)
        self._url = 'https://wallhaven.cc/search?categories=111&purity=100&atleast=3840x2160&ratios=16x9&topRange=1y' \
                    '&sorting=toplist&order=desc&ai_art_filter=0&page={}'

    def _producer(self):
        current_page = 1
        try:
            while True:
                http_log.log('正在下载第{}页'.format(current_page))
                page = req_data_retry(self._url.format(str(current_page)))

                page_soup = BeautifulSoup(page, 'html.parser')
                img_list = page_soup.select('div#thumbs section.thumb-listing-page ul li a.preview')

                if len(img_list) == 0:
                    self._producer_end()
                    break
                for img_info in img_list:
                    preview_url = img_info.get('href')
                    detail_page = req_data_retry(preview_url, proxy=True)
                    if detail_page is None:
                        continue
                    preview_page_soup = BeautifulSoup(detail_page, 'html.parser')
                    img_url = preview_page_soup.select('img#wallpaper')[0].get('src')
                    self._buffer.put(img_url)

                time.sleep(3)

                current_page += 1
        except (BaseException, Exception):
            self._producer_end()

    @staticmethod
    def _process_data(item):
        download_data(item)


if __name__ == '__main__':
    crawler = WallhavenCrawler()
    crawler.start()
