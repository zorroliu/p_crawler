# -*- coding: utf-8 -*-

import subprocess

FFPROBE = 'ffprobe'


# 获取视频的分辨率
def get_video_wh(input_file):
    resolution_command = [
        FFPROBE, '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height', '-of', 'csv=p=0', input_file
    ]

    try:
        result = subprocess.run(resolution_command, capture_output=True, text=True)
        output = result.stdout
        return output.replace('\n', '').split(',')
    except subprocess.CalledProcessError:
        return None, None
