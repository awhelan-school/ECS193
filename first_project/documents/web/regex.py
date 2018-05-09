#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def get_data(grammar,html):
    re_source = re.compile(grammar)
    source = re.findall(re_source,html)
    return source

