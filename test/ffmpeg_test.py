# -*- coding: utf-8 -*-

import os
import unittest
from util.ffmpeg_util import capture_video, merge_video_list, to_ts
from util.ffprobe_util import get_video_wh


class FfmpegTestCase(unittest.TestCase):
    def test_merge_video(self):
        base_dir = 'C:\\Users\\86130\\Desktop\\video\\ggk'
        tmp_ts_dir = 'C:\\Users\\86130\\Desktop\\video\\ggk_tmp'
        ts_list = []
        for file in os.listdir(base_dir):
            ts_file_path = os.path.join(tmp_ts_dir, file.replace('.mp4', '.ts'))
            ts_list.append(ts_file_path)
            to_ts(os.path.join(base_dir, file), ts_file_path)
        merge_video_list(ts_list, os.path.join(tmp_ts_dir, 'ggk.mp4'))

        self.assertEqual(True, True)

    def test_capture_video(self):
        input_file = 'C:\\Users\\86130\\Desktop\\video\\ggk_tmp\\ggk.mp4'
        output_file_path = 'C:\\Users\\86130\\Desktop\\video\\ggk_tmp\\ggk_1.mp4'
        capture_video(input_file, '00:00:30', '10', output_file_path)

        self.assertEqual(True, True)

    def test_del_video(self):
        base_dir = 'C:\\Users\\86130\\Desktop\\video\\ggk'
        for file in os.listdir(base_dir):
            file_path = os.path.join(base_dir, file)
            wh = get_video_wh(file_path)
            if wh[0] == '1080' and wh[1] == '1920':
                continue
            os.remove(file_path)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
