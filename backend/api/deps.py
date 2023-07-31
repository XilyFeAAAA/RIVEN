#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from lcu import lcu


class LcuValid(Exception):
    pass


def get_current_lcu():
    if not lcu.valid:
        raise LcuValid()
    else:
        return lcu
