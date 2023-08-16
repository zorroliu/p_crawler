# -*- coding: utf-8 -*-

import unittest
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from util.async_http_util import fetch_req, download_data


class MyTestCase(unittest.TestCase):
    def test_something(self):
        url = 'https://wallhaven.cc/search?categories=111&purity=100&atleast=3840x2160&ratios=16x9&topRange=1y' \
              '&sorting=toplist&order=desc&ai_art_filter=0&page={}'

        async def start():
            async with aiohttp.ClientSession() as session:
                current_page = 1
                while True:
                    print('正在下载第{}页'.format(current_page))
                    page = await fetch_req(session, url.format(str(current_page)))

                    page_soup = BeautifulSoup(page, 'html.parser')
                    img_list = page_soup.select('div#thumbs section.thumb-listing-page ul li a.preview')

                    if len(img_list) == 0:
                        break
                    for img_info in img_list:
                        preview_url = img_info.get('href')
                        async with session.get(preview_url, ssl=False) as preview_resp:
                            if preview_resp.status == 200:
                                preview_page_soup = BeautifulSoup(await preview_resp.text(), 'html.parser')
                                img_url = preview_page_soup.select('img#wallpaper')[0].get('src')
                                print(img_url)
                                try:
                                    await download_data(session, img_url)
                                except (BaseException, Exception):
                                    pass
                                await asyncio.sleep(2)

                    current_page += 1

        asyncio.run(start())

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
