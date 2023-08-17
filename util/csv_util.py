# -*- coding: utf-8 -*-

import csv


def write_csv_rows(file_path: str = None, csv_header=None, data=None, mode: str = 'w', encoding: str = 'utf-8-sig'):
    if data is None:
        data = []
    with open(file_path, mode=mode, encoding=encoding, newline='') as fp:
        # 写
        writer = csv.writer(fp)
        if csv_header is not None:
            # 设置第一行标题头
            writer.writerow(csv_header)
        # 将数据写入
        writer.writerows(data)
