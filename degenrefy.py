#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'dminkovsky'

import os
from utils import get_mutagen_id3, get_files
# from chardet import detect

def degenrefy(file_path):
    id3 = get_mutagen_id3(file_path)
    try:
        del(id3['TCON'])
    except:
        pass
    id3.save()

if __name__ == '__main__':
    for file_path in get_files(os.getcwd()):
        degenrefy(file_path)