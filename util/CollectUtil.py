# -*- coding: utf-8 -*-

def str_get(t_str):
    return t_str if t_str else ''


def dict_get(dict_obj=None, key: str = None):
    if dict_obj is None:
        dict_obj = {}
    try:
        return dict_obj[key]
    except KeyError:
        return None


def dict_get_str(dict_obj=None, key: str = None):
    if dict_get(dict_obj=dict_obj, key=key) is None:
        return ''

    return dict_get(dict_obj=dict_obj, key=key)


def list_index(c_list: list, c_index: int):
    try:
        return c_list[c_index]
    except IndexError:
        return None


def split_list(lst, size):
    """
    将一个列表分成指定大小的子列表

    参数：
    lst：要分割的列表
    size：子列表的大小

    返回值：
    一个由子列表组成的新列表
    """
    result = []
    for i in range(0, len(lst), size):
        result.append(lst[i:i + size])
    return result
