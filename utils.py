#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'dminkovsky'


import mutagen.id3
import os

def get_mutagen_id3(file_path):
    return mutagen.id3.ID3(file_path)

def get_files(path, recurse=False):
    """
    Get files at the given path, maybe recurse
    """
    for child in os.listdir(path):
        child = os.path.join(path, child)
        if os.path.isdir(child) and recurse:
            for nested_child in get_files(child, True):
                yield nested_child
        elif child.lower().endswith('.mp3'):
            yield child