# -*- coding: utf-8 -*-

import pkgutil
from crawlers.base import BaseCrawler
import inspect

# load classes subclass of BaseCrawler
classes = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    for m_name, value in inspect.getmembers(module):
        globals()[m_name] = value
        if inspect.isclass(value) and issubclass(value, BaseCrawler) and value is not BaseCrawler \
                and not getattr(value, 'ignore', False):
            classes.append(value)
__all__ = __ALL__ = classes
