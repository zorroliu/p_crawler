# -*- coding: utf-8 -*-

import re


def match_only_one(pattern, text):
    # 进行匹配
    match = re.search(pattern, text)

    if match:
        desired_content = match.group(1)
        return desired_content
    else:
        return None
