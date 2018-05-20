#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def get_text(grammar,html):
    re_source = re.compile(grammar)
    source = re.findall(re_source,html)
    return source

def get_data(grammar,html):
    re_source = re.compile(grammar)
    source = re.search(re_source,html)
    if source:
        source = source.group(1)
        if len(source) < 5:
            source = "Noun"
    else:
        source = str(source)
    return source