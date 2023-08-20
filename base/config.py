# -*- coding: utf-8 -*-

import configparser
import os


class Config:
    def __init__(self, config_path):
        self._config_path = config_path
        self._config = configparser.ConfigParser()
        self._config.read(self._config_path)

    def get_val(self, option: str = '', is_number: bool = False, section: str = 'generic'):
        try:
            if is_number:
                return self._config.getint(section=section, option=option)
            else:
                return self._config.get(section=section, option=option)
        except configparser.NoOptionError:
            return None

    def set_val(self, option: str = '', value: str = '', section: str = 'generic'):
        self._config.set(section=section, option=option, value=value)
        with open(self._config_path, 'w') as f:
            self._config.write(f)


def get_project_root():
    # 获取当前脚本的绝对路径
    current_file = os.path.abspath(__file__)

    # 假设项目根目录是当前脚本所在目录的父目录
    project_root = os.path.dirname(os.path.dirname(current_file))

    return project_root


default_config: Config = Config(os.path.join(get_project_root(), 'config.ini'))
