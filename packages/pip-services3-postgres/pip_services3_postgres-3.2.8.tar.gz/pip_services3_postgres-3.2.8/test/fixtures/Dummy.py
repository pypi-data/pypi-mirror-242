# -*- coding: utf-8 -*-

from pip_services3_commons.data import IStringIdentifiable


class Dummy(IStringIdentifiable):
    def __init__(self, id=None, key=None, content=None):
        self.id = id
        self.key = key
        self.content = content

