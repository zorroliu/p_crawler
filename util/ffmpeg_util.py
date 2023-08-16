# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from base.logger import CustLogger, LogLevel

fg_log = CustLogger('ffmpeg')

FFMPEG_CMD = 'ffmpeg'


# 视频转m3u8格式
def video_to_m3u8(input_file, output_file,
                  level: str = '3.0', start_number: str = '0',
                  hls_time: str = '60', hls_list_size: str = '0'):
    try:
        ffmpeg_options = [
            FFMPEG_CMD,
            '-i', input_file,
            '-profile:v', 'baseline',
            '-level', level,
            '-start_number', start_number,
            '-hls_time', hls_time,
            '-hls_list_size', hls_list_size,
            '-f', 'hls',
            output_file
        ]

        subprocess.run(ffmpeg_options, check=True)
        fg_log.log(f'【{input_file}】转换成功')
    except subprocess.CalledProcessError as e:
        fg_log.log(f'【{input_file}】转换失败: {e}', level=LogLevel.ERROR)


# 视频转ts格式
def to_ts(input_file, output_file):
    # ffmpeg将MP4转换为TS的命令
    convert_command = [
        FFMPEG_CMD, '-i', input_file, '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', output_file
    ]

    try:
        subprocess.run(convert_command, check=True)
        fg_log.log(f'转换为TS成功, 已保存为【{output_file}】')
    except subprocess.CalledProcessError as e:
        fg_log.log(f'转换过程中发生错误: {e}', level=LogLevel.ERROR)


# 提取视频
def extract_video(input_file, output_video):
    video_command = [
        FFMPEG_CMD, '-i', input_file, '-y', '-c:v', 'copy', '-an', output_video
    ]

    try:
        subprocess.run(video_command, check=True)
        fg_log.log(f'视频提取成功并保存为:【{output_video}】')
    except subprocess.CalledProcessError as e:
        fg_log.log(f'视频提取错误: {e}', level=LogLevel.ERROR)


# 提取音频
def extract_audio(input_file, output_audio):
    audio_command = [
        FFMPEG_CMD, '-i', input_file, '-f', 'mp3', '-y', '-vn', output_audio
    ]

    try:
        subprocess.run(audio_command, check=True)
        fg_log.log(f'音频提取成功并保存为:【{output_audio}】')
    except subprocess.CalledProcessError as e:
        fg_log.log(f'音频提取错误: {e}', LogLevel.ERROR)


# 合并视频和音频
def merge_audio_video(video_file, audio_file, output_file):
    merge_command = [
        FFMPEG_CMD, '-i', video_file, '-i', audio_file,
        '-c:v', 'copy', '-c:a', 'aac', output_file
    ]

    try:
        subprocess.run(merge_command, check=True)
        fg_log.log(f'音频和视频合并成功, 已保存为【{output_file}】')
    except subprocess.CalledProcessError as e:
        fg_log.log(f'合并过程中发生错误: {e}', LogLevel.ERROR)


# 合并多个视频文件
def merge_video_list(input_file_list, output_file):
    output_file_name = os.path.basename(output_file)
    output_file_dir = os.path.dirname(output_file)
    concat_text_file = os.path.join(output_file_dir, os.path.splitext(output_file_name)[0] + '.txt')

    tmp_file_list = []

    with open(concat_text_file, 'w') as fw:
        for index, file in enumerate(input_file_list):
            tmp_file_name = f'{index}_{os.path.basename(file)}'
            new_tmp_file_path = os.path.join(output_file_dir, tmp_file_name)
            shutil.copy(file, new_tmp_file_path)
            tmp_file_list.append(new_tmp_file_path)
            fw.write(f'file \'{tmp_file_name}\'\n')

    merge_command = [
        FFMPEG_CMD, '-f', 'concat', '-i', concat_text_file,
        '-acodec', 'copy', '-vcodec', 'copy', '-absf', 'aac_adtstoasc', output_file
    ]

    try:
        subprocess.run(merge_command, check=True)
        fg_log.log(f'视频文件合并成功, 已保存为【{output_file}】')
    except subprocess.CalledProcessError as e:
        fg_log.log(f'合并过程中发生错误: {e}', LogLevel.ERROR)
    finally:
        os.remove(concat_text_file)
        for t_file in tmp_file_list:
            os.remove(t_file)


# 截取视频
def capture_video(input_file, start_time, duration, output_file):
    """
    :param input_file: 输入视频文件
    :param start_time: 截取的开始时间，格式可以是秒数（例如：10）或时间（例如：00:00:10）
    :param duration: 要截取的视频段的持续时间，格式同样可以是秒数或时间
    :param output_file: 输出文件
    :return:
    """
    capture_command = [
        FFMPEG_CMD, '-ss', start_time, '-i', input_file, '-t', duration,
        '-c:v', 'copy', '-c:a', 'copy', output_file
    ]
    try:
        subprocess.run(capture_command, check=True)
        fg_log.log(f'视频截取成功, 已保存为【{output_file}】')
    except subprocess.CalledProcessError as e:
        fg_log.log(f'视频截取过程中发生错误: {e}', LogLevel.ERROR)
