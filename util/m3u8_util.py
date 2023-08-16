# -*- coding: utf-8 -*-

import m3u8


def get_ts_list_from_file(m3u8_file):
    with open(m3u8_file, "r") as file:
        m3u8_content = file.read()

    m3u8_obj = m3u8.loads(m3u8_content)

    if m3u8_obj.is_variant:
        print("This is a variant playlist, not a media playlist.")
        return

    if not m3u8_obj.segments:
        print("No segments found in the M3U8 file.")
        return

    return [segment.uri for segment in m3u8_obj.segments]


def get_ts_list_from_uri(m3u8_url, headers=None, verify_ssl=True):
    if headers is None:
        headers = {}
    m3u8_obj = m3u8.load(m3u8_url, headers=headers, verify_ssl=verify_ssl)

    if m3u8_obj.is_variant:
        print("This is a variant playlist, not a media playlist.")
        return

    if not m3u8_obj.segments:
        print("No segments found in the M3U8 file.")
        return

    return [segment.uri for segment in m3u8_obj.segments]
