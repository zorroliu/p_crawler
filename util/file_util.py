# -*- coding: utf-8 -*-

import os


def dir_exists_or_create(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
